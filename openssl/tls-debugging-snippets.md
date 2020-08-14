# OpenSSL: TLS Debugging Snippets
This TIL provides several useful snippets for debugging TLS connections using the OpenSSL toolkit.

## Client
```
openssl x509 -text -noout -in /etc/pki_service/client/certificates/server.pem
```

## Server
```
openssl s_client -connect localhost:8080 -debug
```
```
openssl verify -CAfile /etc/pki_service/ca/cacerts.pem -untrusted server.pem server.pem
```
```
curl https://some-api-endpoint -d '{"jsonKey": "jsonValue"}'  --cacert /etc/pki_service/ca/cacerts.pem -v --key /etc/pki_service/client/keys/client-key.pem --cert /etc/pki_service/client/certificates/client.pem -H "Content-Type: application/json"
```

### Certificate Authority (CA)
```
openssl crl2pkcs7 -nocrl -certfile server-cacerts.pem | openssl pkcs7 -print_certs -text -noout
```
