#!/bin/sh

echo "openssl.sh recibe argumentos:"
echo "servicio --> $1"
echo "carpeta usuario --> $2"
echo "Se genera ./$2/tra.$1.xml para el web service $1"


CERT="_cert.crt"    # El certificado X.509 obtenido de AFIP Seg. Inf.
PRIV="_priv.key"    # La clave privada del certificado CERT

emp=cda
CERTIFICATE="$emp$CERT"
PRIVATE_KEY="$emp$PRIV"

echo "Certificado ./certif/$CERTIFICATE"
echo "Clave priv. ./certif/$PRIVATE_KEY"

echo "Se codifica tra.$1.xml.cms a partir de tra.$1.xml"
openssl smime \
        -sign \
        -signer ./certif/$CERTIFICATE \
        -inkey  ./certif/$PRIVATE_KEY \
        -in     ./$2/tra.$1.xml \
        -out    ./$2/tra.$1.xml.cms \
        -outform DER \
        -nodetach

echo "Se codifica ./$2/tra.$1.xml.cms.base64 a ./$2/partir de tra.$1.xml.cms"
openssl base64 \
        -in  ./$2/tra.$1.xml.cms \
        -out ./$2/tra.$1.xml.cms.base64
