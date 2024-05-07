---
blogpost: true
date: May 07, 2024
author: Jens W. Klein
location: Austria
category: Kafka, OpenSSL
language: en
---

# Fun with OpenSSL: Create new keys for Apache Kafka

So it happens we are using the [Bitnami Kafka Helm Chart](https://github.com/bitnami/charts/tree/main/bitnami/kafka).
After 365 days the auto generated certificates are outdated and Kafka refuses to run.

## How it happened

The Helm chart (mentioned above) generates the keys automagically on initial installation.
The keys are stored in a secret and mounted to the Kafka pods.
All works fine, unitl the keys expire.

Now we need to create new keys and update the secret.
The Helm chart does not provide a way to update the keys (AFAIK).

## Create new keys

My OpenSSL-foo is intermediate. So don't expect too much, probably there are improvements possible.

However, I found my way to create new keys.

The overall process is:
- create a Certificate Authority (CA) with a key and a certificate.
- create three Certificate Signing Request (CSR) for the three Kafka brokers using the same private key, which is created with the first signing request.
- sign the three CSR with the CA.

Afterwards we have
- new CA key (not needed for the brokers)
- CA certificate
- private key for the brokers
- three new signed certificates and a new key for the brokers.


## Preparations

First we need to create four configuration files for the CA/signing and the CSR (one for each broker).

### CA and signing configuration

Replace the uppcased word in section `ca_distinguished_name` with your values.

Name the file

```ini
HOME            = .
RANDFILE        = $ENV::HOME/.rnd

####################################################################
[ ca ]
default_ca    = CA_default      # The default ca section

[ CA_default ]

default_days     = 365          # How long to certify for
default_crl_days = 30           # How long before next CRL
default_md       = sha256       # Use public key default MD
preserve         = no           # Keep passed DN ordering

x509_extensions = ca_extensions # The extensions to add to the cert

email_in_dn     = no            # Don't concat the email in the DN
copy_extensions = copy          # Required to copy SANs from CSR to cert

base_dir      = .
certificate   = $base_dir/cacert.pem   # The CA certifcate
private_key   = $base_dir/cakey.pem   # The CA private key
new_certs_dir = $base_dir              # Location for new certs after signing
database      = $base_dir/index.txt    # Database index file
serial        = $base_dir/serial.txt   # The current serial number

unique_subject = no  # Set to 'no' to allow creation of
                     # several certificates with same subject.

####################################################################
[ req ]
default_bits       = 4096
default_keyfile    = cakey.pem
distinguished_name = ca_distinguished_name
x509_extensions    = ca_extensions
string_mask        = utf8only

####################################################################
[ ca_distinguished_name ]
countryName         = Country Name (2 letter code)
countryName_default = DE
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = STATE
localityName                = Locality Name (eg, city)
localityName_default        = CITY
organizationName            = Organization Name (eg, company)
organizationName_default    = ORGANIZATION
organizationalUnitName         = Organizational Unit (eg, division)
organizationalUnitName_default = ORGUNIT
commonName         = Common Name (e.g. server FQDN or YOUR name)
commonName_default = Kafka CA
emailAddress         = Email Address
emailAddress_default = john.doe@example.com

####################################################################
[ ca_extensions ]

subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always, issuer
basicConstraints       = critical, CA:true
keyUsage               = keyCertSign, cRLSign

####################################################################
[ signing_policy ]
countryName            = optional
stateOrProvinceName    = optional
localityName           = optional
organizationName       = optional
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

####################################################################
[ signing_req ]
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
basicConstraints       = CA:FALSE
keyUsage               = digitalSignature, keyEncipherment
```

For the Certificate Signing Request (CSR) we need three configuration files.
- `openssl-csr-0.cnf`
- `openssl-csr-1.cnf`
- `openssl-csr-2.cnf`

The only difference is the `commonName` in the `server_distinguished_name` section and the `DNS` in the `alternate_names` section.
`kafka-0` needs to be replaced by `kafka-1` and `kafka-2` in the other files.

In each file replace the uppcased word in section `ca_distinguished_name` with your values, as already done in the CA configuration file.

### CSR configuration

```ini
HOME            = .
RANDFILE        = $ENV::HOME/.rnd

####################################################################
[ req ]
default_bits       = 4096
default_keyfile    = kafka.key
distinguished_name = server_distinguished_name
req_extensions     = server_req_extensions
string_mask        = utf8only

####################################################################
[ server_distinguished_name ]
countryName         = Country Name (2 letter code)
countryName_default = DE
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = STATE
localityName                = Locality Name (eg, city)
localityName_default        = CITY
organizationName            = Organization Name (eg, company)
organizationName_default    = ORGANIZATION
organizationalUnitName         = Organizational Unit (eg, division)
organizationalUnitName_default = ORGUNIT

commonName         = Common Name (e.g. server FQDN or YOUR name)
commonName_default = kafka-0.kafka-headless

emailAddress         = Email Address
emailAddress_default = john.doe@example.com
####################################################################
[ server_req_extensions ]

subjectKeyIdentifier = hash
basicConstraints     = CA:FALSE
keyUsage             = digitalSignature, keyEncipherment
subjectAltName       = @alternate_names
nsComment            = "OpenSSL Generated Certificate"

####################################################################
[ alternate_names ]

DNS.1 = kafka-0.kafka-headless.argo.svc.cluster.local
DNS.2 = kafka.argo.svc.cluster.local
DNS.3 = kafka-0.kafka-headless.argo.svc.cluster.local
DNS.4 = kafka.argo
DNS.5 = kafka-0.kafka-headless
DNS.6 = kafka
```

### Index and Serial files

Create files for index and serial like so:

```bash
touch index.txt
echo "01" > serial.txt
```

## Create the CA

Create the CA key and certificate.

```bash
openssl req -new -x509 -config openssl-ca.cnf -days 365 -newkey rsa:4096 -sha256 -noenc -out cacert.pem -outform PEM
```

This creates a
- `cakey.pem` - the private Key of the CA
- `cacert.pem` - the certificate of the CA for deployment

## Create the broker keys

### CSR and private key

With the first CSR we also create the private key for the brokers.

```bash
openssl req -new -config openssl-csr-0.cnf -newkey rsa:4096 -sha256 -noenc -out kafka-0.csr -outform PEM
```

This creates a
- `kafka.key` - the private key for the brokers
- `kafka-0.csr` - the first Certificate Signing Request for the CA

Then we create two more CSR for the other brokers using the same key.

```bash
openssl req -new -config openssl-csr-1.cnf -key kafka.key -out kafka-1.csr -outform PEM
openssl req -new -config openssl-csr-2.cnf -key kafka.key -out kafka-2.csr -outform PEM
```

This creates a
- `kafka-1.csr` - the second Certificate Signing Request for the CA
- `kafka-2.csr` - the third Certificate Signing Request for the CA

### Sign the CSR

Now we sign the CSR with the CA.
This creates the actual certificates for the brokers.

```bash
openssl ca -config openssl-ca.cnf -policy signing_policy -extensions signing_req -out kafka-0.pem -infiles kafka-0.csr
openssl ca -config openssl-ca.cnf -policy signing_policy -extensions signing_req -out kafka-1.pem -infiles kafka-1.csr
openssl ca -config openssl-ca.cnf -policy signing_policy -extensions signing_req -out kafka-2.pem -infiles kafka-2.csr
```

## Update the secret

There are three secrets in the Kafka namespace:
- `kafka-0-tls`
- `kafka-1-tls`
- `kafka-2-tls`

Any of these have three entries:
1. `ca.crt`
1. `tls.crt`
1. `tls.key`

Now we need to update all these values.

- `ca.crt` is the `cacert.pem` from the CA
- `tls.key` is the `kafka.key`
- `tls.crt` is the `kafka-0.pem`, `kafka-1.pem`, `kafka-2.pem` respectively

I did this using the Portainer UI, but you can also use `kubectl` to update the secrets.
