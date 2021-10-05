cd C:\Users\FABIO\OneDrive\Documentos\GitHub\boticarios_v2\private
openssl x509 -in client-cert.pem -out ssl-cert.crt
openssl x509 -in server-ca.pem -out ca-cert.crt
openssl rsa -in client-key.pem -out ssl-key.key
pause