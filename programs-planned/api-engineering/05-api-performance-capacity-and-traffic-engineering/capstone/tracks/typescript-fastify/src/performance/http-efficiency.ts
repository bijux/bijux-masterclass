const ETAG_RE = /^(W\/)?"[\x21\x23-\x7E\x80-\xFF]*"$/;

export class RangeNotSatisfiable extends Error {
  constructor(readonly completeLength: bigint) {
    super(`bytes */${completeLength.toString()}`);
  }
}

export function parseEtagList(value: string): string[] | "*" {
  const stripped = value.trim();
  if (stripped === "*") return "*";
  if (!stripped) throw new Error("empty entity-tag list");
  const tags = stripped.split(",").map((part) => part.trim());
  if (tags.some((tag) => !ETAG_RE.test(tag))) throw new Error("malformed entity tag");
  return tags;
}

function opaque(tag: string): string {
  return tag.startsWith("W/") ? tag.slice(2) : tag;
}

export function weakMatch(left: string, right: string): boolean {
  if (!ETAG_RE.test(left) || !ETAG_RE.test(right)) {
    throw new Error("malformed entity tag");
  }
  return opaque(left) === opaque(right);
}

export function strongMatch(left: string, right: string): boolean {
  if (left.startsWith("W/") || right.startsWith("W/")) return false;
  if (!ETAG_RE.test(left) || !ETAG_RE.test(right)) {
    throw new Error("malformed entity tag");
  }
  return left === right;
}

export function ifNoneMatchMatches(value: string, currentEtag: string): boolean {
  const tags = parseEtagList(value);
  return tags === "*" || tags.some((tag) => weakMatch(tag, currentEtag));
}

export function ifRangeAllowsRange(value: string, currentEtag: string): boolean {
  const stripped = value.trim();
  if (!stripped.startsWith('"') && !stripped.startsWith('W/"')) return false;
  return strongMatch(stripped, currentEtag);
}

export interface RangeSelection {
  start: bigint;
  endExclusive: bigint;
  completeLength: bigint;
  length: bigint;
  contentRange: string;
}

function decimalBigint(value: string, label: string): bigint {
  if (!/^[0-9]+$/.test(value)) throw new Error(`malformed ${label}`);
  return BigInt(value);
}

export function parseSingleRange(
  value: string,
  completeLength: bigint,
): RangeSelection {
  if (completeLength < 0n) throw new Error("complete length must be non-negative");
  if (!value.startsWith("bytes=")) throw new Error("only bytes ranges are supported");
  const spec = value.slice(6).trim();
  if (spec.includes(",")) throw new Error("multiple ranges are not supported");
  const dash = spec.indexOf("-");
  if (dash < 0) throw new Error("malformed byte range");
  const first = spec.slice(0, dash).trim();
  const last = spec.slice(dash + 1).trim();
  if (completeLength === 0n) throw new RangeNotSatisfiable(completeLength);

  let start: bigint;
  let endExclusive: bigint;
  if (first === "") {
    const suffix = decimalBigint(last, "suffix range");
    if (suffix <= 0n) throw new RangeNotSatisfiable(completeLength);
    const length = suffix < completeLength ? suffix : completeLength;
    start = completeLength - length;
    endExclusive = completeLength;
  } else {
    start = decimalBigint(first, "range start");
    if (start >= completeLength) throw new RangeNotSatisfiable(completeLength);
    if (last === "") {
      endExclusive = completeLength;
    } else {
      const inclusiveEnd = decimalBigint(last, "range end");
      if (inclusiveEnd < start) throw new RangeNotSatisfiable(completeLength);
      const proposed = inclusiveEnd + 1n;
      endExclusive = proposed < completeLength ? proposed : completeLength;
    }
  }
  return {
    start,
    endExclusive,
    completeLength,
    length: endExclusive - start,
    contentRange:
      `bytes ${start.toString()}-${(endExclusive - 1n).toString()}/` +
      completeLength.toString(),
  };
}

export function chooseContentEncoding(input: {
  acceptEncoding: string;
  mediaType: string;
  bodyLength: number;
  minimumSize?: number;
  rangeRequested?: boolean;
}): "gzip" | "identity" {
  const minimum = input.minimumSize ?? 1024;
  if (input.bodyLength < 0 || minimum < 0) throw new Error("invalid length");
  if (input.rangeRequested) return "identity";
  const media = input.mediaType.toLowerCase();
  const compressible =
    media.startsWith("application/json") ||
    media.startsWith("application/problem+json") ||
    media.startsWith("application/xml") ||
    media.startsWith("text/");
  if (!compressible || input.bodyLength < minimum) return "identity";
  const accepted = new Set(
    input.acceptEncoding.split(",").map((part) => part.split(";", 1)[0]?.trim().toLowerCase()),
  );
  return accepted.has("gzip") || accepted.has("*") ? "gzip" : "identity";
}

export function estimatedApplicationBufferBytes(
  activeStreams: bigint,
  chunkSize: bigint,
  buffersPerStream: bigint,
): bigint {
  if (activeStreams < 0n || chunkSize < 0n || buffersPerStream < 0n) {
    throw new Error("buffer inputs must be non-negative");
  }
  return activeStreams * chunkSize * buffersPerStream;
}
