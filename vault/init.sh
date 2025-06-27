#!/bin/sh

export VAULT_ADDR=http://vault:8200
export VAULT_TOKEN=root

# Injecter des secrets d'exemple
vault kv put secret/keycloak admin=admin password=admin client_id=djassa-client client_secret=LwGYdmRwqeiCcSs6RYihcWAYxHdGwiV4 public_key=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjDMVi+jjCKWLzz+w78FfOiL4BP+J0xIZv64Wx/1YKI2qPEMB8Z4wQT6ZyMUPOu/lD6HSEy1xFJ/e6sUp2EioWehjCAYpL8Cb/m/h4KD0BAmDHdGAdhRWgaML5ravu/GV0feGDY6ndrl+/0Q5aGf0CcLpdTyFfluwIvB0BZZ6HKlm0h2TnWDIEsbfeOfS71vCeaZnHHe5/WJiQEvsmiBNBHJKHKZI3Hi6LtEiZmyM+dcNh6bIFObz6sMQQ76KIs1fdcDL6uMP8qwx3Y7OsUzV0qCKOQzhUaOg8Kzh3+QNZQ9Fn543KN614/b6dI/BvBuFKAJjK6ijmEIedUTnBM3oXwIDAQAB
vault kv put secret/postgres username=postgres password=password

echo "✅ Secrets injectés dans Vault"
