import http2 from 'node:http2';

export function responseHeaders(status: number, contentType = 'application/json'): http2.OutgoingHttpHeaders {
  return {
    ':status': status,
    'content-type': contentType,
  };
}
