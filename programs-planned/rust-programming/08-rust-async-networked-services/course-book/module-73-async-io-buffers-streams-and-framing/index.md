# Module 73: Async I/O, Buffers, Streams, and Framing

**Course 8, day 3 · Module 73 of 80**

**73/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?

## Why this comes now

A runtime can schedule tasks correctly while an application still corrupts its network protocol. TCP presents an ordered byte stream, not a sequence of application messages. One read may return part of a length prefix, exactly one frame, or several frames. A write may complete only a prefix. Readiness says that an operation may make progress; it does not promise that the entire requested transfer will complete.

Module 71 gave you the polling contract. Module 72 gave every task an owner. This module places I/O inside those futures and makes the buffering contract explicit. It is the point where many demos become unsafe products: they allocate from an untrusted length before checking it, assume `read` fills a buffer, treat `0` bytes as “try again,” lose bytes after decoding one frame, or cancel a write midway and reuse the connection as if no prefix escaped.

The central discipline is layered:

```text
readiness → byte transfer → buffer state → frame extraction → protocol parsing
```

Each layer has a different error model and cancellation consequence.

## What you will be able to do

- distinguish readiness from transfer completion;
- handle partial reads and partial writes without message-boundary assumptions;
- explain the contracts of `AsyncRead`, `AsyncWrite`, `AsyncBufRead`, `Stream`, and `Sink`;
- use `Bytes` and `BytesMut` to separate shared immutable payloads from mutable receive buffers;
- design a decoder that preserves incomplete input and extracts multiple complete frames;
- check length arithmetic and configured maxima before reserve or allocation;
- distinguish clean EOF from truncated EOF;
- define canonical frame encoding independent of network chunking;
- test a codec at every split point and under frame coalescing;
- analyze cancellation during read and write operations.

## Core model

### Readiness is permission to try

An async socket integrates with the runtime’s I/O driver. When an operation cannot make progress, its future registers interest and returns `Pending`. When the OS reports readiness, the task is woken and tries the syscall again.

Readiness does not promise:

- the requested number of bytes;
- one complete frame;
- that another task has not consumed readiness first;
- that the peer remains connected;
- that a write will not return a partial count;
- that the next syscall cannot still report `WouldBlock`.

Treat readiness as “retry may be useful.” The actual transfer result remains authoritative.

### `read` is a byte operation

For a byte stream, a successful read of `n > 0` appends `n` bytes. A successful read of `0` means EOF for TCP: the peer’s sending side has closed and no more bytes will arrive. It is not a temporary lack of data. A pending read represents temporary lack of progress; the future does not resolve to zero merely because the peer is quiet.

If a decoder has no buffered partial frame when EOF arrives, the protocol may treat that as a clean connection close. If bytes remain that cannot form a complete frame, the stream is truncated and should produce a causal framing error.

### `write` is also partial

A successful `write` may accept fewer bytes than requested. `write_all` loops until the slice is exhausted or an error occurs. That convenience does not create transactional semantics. If cancellation or error occurs after a prefix is written, the peer may observe a malformed partial frame. Many protocols should close the connection rather than attempt to continue after an interrupted frame write.

One connection should have one serialized writer unless the protocol includes an explicit multiplexing and frame-assembly layer. Two tasks independently calling `write_all` on the same stream can interleave application frames even if each task’s local slice order is preserved.

### Buffer state is protocol state

A receive buffer has three conceptual regions:

```text
consumed bytes | complete undecoded bytes | incomplete trailing bytes
```

A decoder should remove only complete frames. Incomplete bytes remain for the next read. When several frames are already present, the decoder should return them one at a time without waiting for more I/O.

`BytesMut` is useful for mutable accumulation and splitting. A decoded payload can become `Bytes`, an immutable reference-counted view, without copying the underlying allocation in common operations. This is a cost model, not a license to retain unlimited input. Keeping a tiny `Bytes` slice may keep a much larger allocation alive, so lifetime and retention still need limits.

### Length-prefixed framing

A simple bounded frame can use:

```text
4-byte unsigned big-endian payload length
payload bytes
```

The decoder algorithm is:

1. If fewer than four bytes are buffered, return “need more data.”
2. Read the prefix without consuming it.
3. Convert to `usize` using checked conversion where target width matters.
4. Reject lengths above the configured maximum.
5. Compute `4 + length` with checked addition.
6. If fewer than that total are buffered, reserve only a bounded additional amount and return “need more data.”
7. Advance past the prefix and split exactly the payload.
8. Leave any following frames in the buffer.

Never call `reserve(length)` before the maximum and arithmetic checks. A hostile peer controls the prefix.

### Decoder and encoder responsibilities

A `tokio_util::codec::Decoder` transforms bytes already present in a mutable buffer into zero or one item per call. `FramedRead` or `Framed` drives reads and repeatedly invokes the decoder. `Encoder` appends a complete item representation to an output buffer.

Keep responsibilities separate:

| Layer | Owns |
|---|---|
| codec | frame boundary, maximum size, exact byte representation, truncated EOF |
| protocol parser | command grammar, field validation, version-specific syntax |
| connection state machine | whether the command is legal now |
| application | domain meaning and commit |

A codec should not know that `SUBMIT` is legal only after `HELLO`. The state machine should not manually index raw byte prefixes.

### `decode_eof` is a separate contract

At EOF, a decoder gets one final chance to emit a complete buffered frame. After complete frames are exhausted:

- an empty buffer is clean EOF;
- a nonempty buffer is truncated framing;
- a protocol-specific delimiter codec may apply another documented rule.

Do not silently discard leftover bytes. They are evidence of a peer failure, transport truncation, or local bug.

### Streams and sinks express repeated async values

`Stream` is conceptually an asynchronous sequence of items. Polling yields:

```text
Ready(Some(item))  one item
Ready(None)        terminal end
Pending            no item now; wake later
```

`Sink` separates readiness to accept an item, starting the send, flushing buffered output, and closing. These phases matter for backpressure and cancellation. A convenience `send(item).await` typically combines readiness, start, and flush semantics defined by the sink extension method, but the underlying protocol still has buffered state.

When a `Framed` transport implements both stream and sink, splitting it can give separate read and write owners. That helps lifecycle separation, but one owner must still coordinate shutdown and close order.

### Cancellation safety is operation-specific

A cancellation ledger for framing distinguishes:

| Operation | If dropped while pending |
|---|---|
| read into internal buffer | bytes already read remain in the buffer owned by the surrounding framed transport if that transport survives |
| `next()` on a stream | generally no decoded item is removed until ready, but verify the specific stream contract |
| `send(frame)` | output may have been partly buffered or written; continuing safely depends on sink ownership and protocol |
| `flush()` | previously started frames may remain buffered or partly written |
| `close()` | peer-observable shutdown may be incomplete |

The question is not “is async I/O cancellation safe?” It is “what state does this particular future own, and what side effects may already have occurred?”

### Chunking must not affect meaning

A frame codec should satisfy a chunk-invariance property:

> For the same encoded byte sequence, feeding bytes in any partition produces the same sequence of decoded frames and the same final buffer state.

Test every split point for small cases. Also test byte-at-a-time delivery, all-at-once delivery, several coalesced frames, empty frames if allowed, maximum frame, maximum-plus-one rejection, and truncated prefixes and payloads.

### Canonical encoding matters

If a protocol has one canonical encoder, equal logical messages produce equal bytes. Canonical output simplifies tests, hashing, captures, compatibility, and debugging. Reject multiple encodings that mean the same thing unless the protocol explicitly needs them.

For text inside binary frames, state the text encoding and normalization policy. A length prefix counts bytes, not Unicode scalar values or displayed characters.

## Use the idea in a complete program

A bounded codec can be concise because its invariants are explicit:

```rust
use bytes::{Buf, BufMut, Bytes, BytesMut};
use std::io;
use tokio_util::codec::{Decoder, Encoder};

#[derive(Debug, Clone)]
pub struct LengthCodec {
    max_payload: usize,
}

impl LengthCodec {
    pub fn new(max_payload: usize) -> Self {
        Self { max_payload }
    }
}

impl Decoder for LengthCodec {
    type Item = Bytes;
    type Error = io::Error;

    fn decode(&mut self, src: &mut BytesMut) -> io::Result<Option<Bytes>> {
        const PREFIX: usize = 4;
        if src.len() < PREFIX {
            return Ok(None);
        }

        let length = u32::from_be_bytes(src[..PREFIX].try_into().expect("prefix length"));
        let length = usize::try_from(length)
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "length does not fit usize"))?;
        if length > self.max_payload {
            return Err(io::Error::new(io::ErrorKind::InvalidData, "frame exceeds maximum"));
        }
        let total = PREFIX.checked_add(length)
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "frame length overflow"))?;
        if src.len() < total {
            src.reserve(total - src.len());
            return Ok(None);
        }

        src.advance(PREFIX);
        Ok(Some(src.split_to(length).freeze()))
    }

    fn decode_eof(&mut self, src: &mut BytesMut) -> io::Result<Option<Bytes>> {
        if let Some(frame) = self.decode(src)? {
            return Ok(Some(frame));
        }
        if src.is_empty() {
            Ok(None)
        } else {
            Err(io::Error::new(io::ErrorKind::UnexpectedEof, "truncated frame"))
        }
    }
}

impl Encoder<Bytes> for LengthCodec {
    type Error = io::Error;

    fn encode(&mut self, item: Bytes, dst: &mut BytesMut) -> io::Result<()> {
        if item.len() > self.max_payload || item.len() > u32::MAX as usize {
            return Err(io::Error::new(io::ErrorKind::InvalidInput, "frame exceeds maximum"));
        }
        dst.reserve(4 + item.len());
        dst.put_u32(item.len() as u32);
        dst.extend_from_slice(&item);
        Ok(())
    }
}
```

The `expect` is justified by a local invariant: the slice length was checked as exactly four. Production code may avoid it for policy consistency, but it is not derived from hostile data after the length check. The codec still needs tests for multiple frames, all partitions, EOF, and output limits.

## Practice sequence

1. Trace a stream where the prefix arrives in three reads and the payload in four.
2. Trace two frames arriving in one read.
3. Repair a decoder that consumes the prefix before confirming the full payload.
4. Repair a decoder that reserves from an unchecked length.
5. Implement `decode_eof` with clean and truncated cases.
6. Write split-point and coalescing tests.
7. Analyze cancellation during frame write and choose a connection-close policy.
8. Transfer the codec into JobWire without adding protocol semantics to it.

## Ready to continue

Continue only when you can explain:

- why one read is not one message;
- why zero bytes differs from `Pending`;
- which bytes remain after an incomplete decode;
- when length checks happen relative to allocation;
- how clean and truncated EOF differ;
- why cancelling a write may require closing the connection;
- why chunking must not change decoded meaning.

## Primary Rust references

- Tokio `AsyncRead`, `AsyncWrite`, and I/O utility documentation;
- `bytes::{Bytes, BytesMut, Buf, BufMut}` documentation;
- `tokio_util::codec::{Decoder, Encoder, Framed}` documentation;
- `futures_util::{StreamExt, SinkExt}` documentation.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Bounded Length Codec](../../labs/module-03-bounded-length-codec/README.md), and add the third [JobWire increment](../capstone.md#increment-3-establish-bounded-framing). Then continue to [Module 74](../module-74-tcp-udp-dns-and-connection-lifecycles/index.md).
