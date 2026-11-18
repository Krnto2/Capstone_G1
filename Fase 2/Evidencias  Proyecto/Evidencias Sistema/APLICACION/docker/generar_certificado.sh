#!/bin/sh
set -e
NOMBRE="${1:-sirema.local}"
IP="${2:-127.0.0.1}"
DIR="$(dirname "$0")/certs"
mkdir -p "$DIR"
openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
  -keyout "$DIR/sirema.key" -out "$DIR/sirema.crt" \
  -subj "/C=CL/O=Octava Compania Bomberos Talcahuano/CN=$NOMBRE" \
  -addext "subjectAltName=DNS:$NOMBRE,DNS:localhost,IP:$IP,IP:127.0.0.1"
echo "Certificado creado en $DIR. Instale sirema.crt en los celulares y computadores de la compañía."
