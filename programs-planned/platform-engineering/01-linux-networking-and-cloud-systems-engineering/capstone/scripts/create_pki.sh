#!/usr/bin/env bash
set -euo pipefail

out=${1:-pki}
mkdir -p "$out"
umask 077

cat > "$out/ca.cnf" <<'EOF'
[req]
distinguished_name = dn
prompt = no
x509_extensions = ca_ext
[dn]
CN = Atlas Course Fixture CA
[ca_ext]
basicConstraints = critical,CA:TRUE,pathlen:0
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always
EOF

cat > "$out/atlas.cnf" <<'EOF'
[req]
distinguished_name = dn
prompt = no
req_extensions = req_ext
[dn]
CN = atlas.test
[req_ext]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
subjectKeyIdentifier = hash
[server_ext]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
[alt_names]
DNS.1 = atlas.test
DNS.2 = localhost
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

openssl req -x509 -newkey rsa:3072 -sha256 -nodes -days 3650 \
  -config "$out/ca.cnf" -keyout "$out/ca.key" -out "$out/ca.crt"
openssl req -new -newkey rsa:3072 -nodes -config "$out/atlas.cnf" \
  -keyout "$out/atlas.key" -out "$out/atlas.csr"
openssl x509 -req -in "$out/atlas.csr" -CA "$out/ca.crt" \
  -CAkey "$out/ca.key" -CAcreateserial -days 825 -sha256 \
  -extensions server_ext -extfile "$out/atlas.cnf" -out "$out/atlas.crt"
chmod 0600 "$out"/*.key
chmod 0644 "$out"/*.crt "$out"/*.cnf
rm -f "$out/atlas.csr" "$out/ca.srl"
