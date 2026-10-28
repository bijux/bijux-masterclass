import type dgram from 'node:dgram';
export function peerKey(peer: dgram.RemoteInfo): string { return `${peer.family}:${peer.address}:${peer.port}`; }
