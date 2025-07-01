#!/bin/bash

cd "$(dirname "$0")" || exit 1 # Position inside the script directory

source ../../.env # I would have liked not to import the whole env... But i need the domain from it

generate_and_sign_cert() {
  local SERVICE_NAME=$1
  local CN=$2

  local SERVICE_DIR="./$SERVICE_NAME"
  mkdir -p "$SERVICE_DIR"

  echo "Generating private key for $SERVICE_NAME..."
  openssl genpkey -algorithm RSA -out "$SERVICE_DIR/$SERVICE_NAME.key" \
    -pkeyopt rsa_keygen_bits:"$CA_SUBDOMAINS_KEY_SIZE" -quiet

  echo "Generating CSR for $SERVICE_NAME..."
  openssl req -new -key "$SERVICE_DIR/$SERVICE_NAME.key" -out "$SERVICE_DIR/$SERVICE_NAME.csr" \
    -subj "/C=$CA_COUNTRY/ST=$CA_STATE/L=$CA_LOCALITY/O=$CA_ORGANIZATION/OU=$CA_ORGANIZATIONAL_UNIT/CN=$CN/emailAddress=$CA_EMAIL"

  echo "Signing CSR for $SERVICE_NAME..."
  openssl x509 -req -in "$SERVICE_DIR/$SERVICE_NAME.csr" -CA "$CA_CERT_LOCATION" -CAkey "$CA_KEY_LOCATION" -CAcreateserial \
    -out "$SERVICE_DIR/$SERVICE_NAME.crt" -days "$CA_DURATION_ROOT" -passin env:CA_PASSPHRASE
}
generate_cert_with_sans2() {
  NAME="$1"
  DOMAIN1="$2"
  DOMAIN2="$3"

  SERVICE_DIR="./$NAME"
  mkdir -p "$SERVICE_DIR"

  echo "Generating private key for $NAME..."
  openssl genpkey -algorithm RSA -out "$SERVICE_DIR/$NAME.key" \
    -pkeyopt rsa_keygen_bits:"$CA_SUBDOMAINS_KEY_SIZE" -quiet

  echo "Generating CSR for $NAME with SANs: $DOMAIN1, $DOMAIN2..."
  openssl req -new -key "$SERVICE_DIR/$NAME.key" -out "$SERVICE_DIR/$NAME.csr" \
    -subj "/C=$CA_COUNTRY/ST=$CA_STATE/L=$CA_LOCALITY/O=$CA_ORGANIZATION/OU=$CA_ORGANIZATIONAL_UNIT/CN=$DOMAIN1/emailAddress=$CA_EMAIL" \
    -reqexts SAN \
    -config <(cat /etc/ssl/openssl.cnf \
      <(printf '[SAN]\nsubjectAltName=DNS:%s,DNS:%s\n' "$DOMAIN1" "$DOMAIN2"))

  echo "Signing CSR for $NAME..."
  openssl x509 -req -in "$SERVICE_DIR/$NAME.csr" -CA "$CA_CERT_LOCATION" -CAkey "$CA_KEY_LOCATION" -CAcreateserial \
    -out "$SERVICE_DIR/$NAME.crt" -days "$CA_DURATION_ROOT" -passin env:CA_PASSPHRASE \
    -extensions SAN -extfile <(cat /etc/ssl/openssl.cnf \
      <(printf '[SAN]\nsubjectAltName=DNS:%s,DNS:%s\n' "$DOMAIN1" "$DOMAIN2"))
}

generate_cert_with_sans3() {
  NAME="$1"
  DOMAIN1="$2"
  DOMAIN2="$3"
  DOMAIN3="$4"

  SERVICE_DIR="./$NAME"
  mkdir -p "$SERVICE_DIR"

  echo "Generating private key for $NAME..."
  openssl genpkey -algorithm RSA -out "$SERVICE_DIR/$NAME.key" \
    -pkeyopt rsa_keygen_bits:"$CA_SUBDOMAINS_KEY_SIZE" -quiet

  echo "Generating CSR for $NAME with SANs: $DOMAIN1, $DOMAIN2, $DOMAIN3..."
  openssl req -new -key "$SERVICE_DIR/$NAME.key" -out "$SERVICE_DIR/$NAME.csr" \
    -subj "/C=$CA_COUNTRY/ST=$CA_STATE/L=$CA_LOCALITY/O=$CA_ORGANIZATION/OU=$CA_ORGANIZATIONAL_UNIT/CN=$DOMAIN1/emailAddress=$CA_EMAIL" \
    -reqexts SAN \
    -config <(cat /etc/ssl/openssl.cnf \
      <(printf '[SAN]\nsubjectAltName=DNS:%s,DNS:%s,DNS:%s\n' "$DOMAIN1" "$DOMAIN2" "$DOMAIN3"))

  echo "Signing CSR for $NAME..."
  openssl x509 -req -in "$SERVICE_DIR/$NAME.csr" -CA "$CA_CERT_LOCATION" -CAkey "$CA_KEY_LOCATION" -CAcreateserial \
    -out "$SERVICE_DIR/$NAME.crt" -days "$CA_DURATION_ROOT" -passin env:CA_PASSPHRASE \
    -extensions SAN -extfile <(cat /etc/ssl/openssl.cnf \
      <(printf '[SAN]\nsubjectAltName=DNS:%s,DNS:%s,DNS:%s\n' "$DOMAIN1" "$DOMAIN2" "$DOMAIN3"))
}

printf "\n\n\n------------------------------------\n\n\n"
if [[ "$CA_KEY_GENERATION" == "y" ]]; then
  printf "\nProceeding with key generation. You can disable it via the .env in the volumes/CA folder\n"
  mkdir -p "root"
  echo "Generating CA key..."
  openssl genpkey -algorithm RSA -out "$CA_KEY_LOCATION" -aes256 \
    -pkeyopt rsa_keygen_bits:"$CA_KEY_SIZE" -quiet \
    -pass env:CA_PASSPHRASE

  echo "Generating CA root certificate..."
  openssl req -key "$CA_KEY_LOCATION" -new -x509 -out "$CA_CERT_LOCATION" -days "$CA_DURATION_ROOT" \
    -subj "/C=$CA_COUNTRY/ST=$CA_STATE/L=$CA_LOCALITY/O=$CA_ORGANIZATION/OU=$CA_ORGANIZATIONAL_UNIT/CN=$CA_COMMONNAME/emailAddress=$CA_EMAIL" \
    -passin env:CA_PASSPHRASE

  generate_and_sign_cert "$OAUTH2PROXY_NAME" "$OAUTH2PROXY_NAME.$CLIENT_TEST_DOMAIN"
  generate_and_sign_cert "$RESOURCESERVER_NAME" "$RESOURCESERVER_NAME.$CLIENT_TEST_DOMAIN"
  generate_and_sign_cert "$KEYCLOAK_NAME" "$KEYCLOAK_NAME.$CLIENT_TEST_DOMAIN"

  generate_cert_with_sans2 "$KEYCLOAK_NAME-proxy" "$OAUTH2PROXY_NAME.$CLIENT_TEST_DOMAIN" "$RESOURCESERVER_NAME.$CLIENT_TEST_DOMAIN"
  generate_cert_with_sans2 "$RESOURCESERVER_NAME-proxy" "$OAUTH2PROXY_NAME.$CLIENT_TEST_DOMAIN" "$KEYCLOAK_NAME.$CLIENT_TEST_DOMAIN"
  generate_cert_with_sans2 "$OAUTH2PROXY_NAME-proxy" "$RESOURCESERVER_NAME.$CLIENT_TEST_DOMAIN" "$KEYCLOAK_NAME.$CLIENT_TEST_DOMAIN"

  generate_cert_with_sans3 "$BURP_NAME" "$RESOURCESERVER_NAME.$CLIENT_TEST_DOMAIN" "$KEYCLOAK_NAME.$CLIENT_TEST_DOMAIN" "$OAUTH2PROXY_NAME.$CLIENT_TEST_DOMAIN"

  echo "Creating the keystore needed for keycloak..."
  openssl pkcs12 -export -in "$KEYCLOAK_NAME"/"$KEYCLOAK_NAME".crt -inkey "$KEYCLOAK_NAME"/"$KEYCLOAK_NAME".key -out "$KEYCLOAK_NAME"/"$KEYCLOAK_NAME".p12 -name "$KEYCLOAK_CA_KEYSTORE_ALIAS" -passout pass:"$KEYCLOAK_CA_KEYSTORE_PASSWORD"


  printf "\n\n\n------------------------------------\n\n\n"
  echo "All keys and certificates generated."
else
  echo "Skipping key and certificate generation. Set KEY_GENERATION=y to enable it."
fi
printf "\n\n\n------------------------------------\n\n\n"