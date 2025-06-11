#!/bin/sh
CLIENT_HELLO_FILTER="tls.handshake.extensions_server_name == $2 && tls.handshake.type == 1"
TCP_STREAM_ID=$(tshark -r $1 \
    -Y "$CLIENT_HELLO_FILTER" \
    -T fields -e tcp.stream | head -1)
echo $TCP_STREAM_ID
SERVER_HELLO_FILTER="tcp.stream == $TCP_STREAM_ID && tls.handshake.type == 2"
FINISHED_FILTER="tcp.stream == $TCP_STREAM_ID && tls.handshake.type == 20"
CERT_FILTER="tcp.stream==$TCP_STREAM_ID && tls.handshake.type==11"
echo "Client TLS version"
tshark -r $1 \
    -Y "$CLIENT_HELLO_FILTER" \
    -V | grep 'Extension: supported_versions'
echo "Server TLS version"
tshark -r $1 \
    -Y "$SERVER_HELLO_FILTER" \
    -V | grep 'Extension: supported_versions'
echo "Cipher Suites Supported by Server"
tshark -r $1 \
    -Y "$SERVER_HELLO_FILTER" \
    -V | grep "Cipher Suite"
t1=$(tshark -r $1 -Y "$CLIENT_HELLO_FILTER" \
     -T fields -e frame.time_relative | head -1)
t2=$(tshark -r $1 -Y "$FINISHED_FILTER" \
     -T fields -e frame.time_relative | head -1)
echo "Handshake time: $(echo "$t2 - $t1" | bc -l) sec"

tshark -r "$1" \
  -Y "$CERT_FILTER" \
  -T fields -e tls.handshake.certificate \
  | head -1 > cert.der

tr -d '[:space:]' < cert.der | xxd -r -p > cert_new.der

openssl x509 -inform der -in cert_new.der -out cert.pem

openssl x509 -in cert.pem -noout -text
