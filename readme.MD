# Djassa Microservices Project 🧩

> **Djassa** est une architecture microservices complète construite autour de **FastAPI**, avec une sécurité gérée par **Keycloak**, un maillage de services via **Consul**, et un reverse proxy **Traefik**. Le projet inclut un middleware d’authentification centralisé (`auth-proxy`) et des services modulaires pour l'utilisateur, l'authentification, etc.

---

## 📦 Architecture

- **Gateway** : Traefik (reverse proxy)
- **Authentification** : Keycloak + `auth-proxy` (middleware JWT)
- **Service Discovery** : Consul
- **Gestion de secrets** : Vault
- **Microservices** : FastAPI (`users`, `products`, etc.)
- **Communication** : HTTP avec injection des claims via middleware
- **Orchestration** : Docker Compose

---

## 📁 Structure du projet

```

djassa/
├── auth-proxy/         # Middleware d’authentification JWT (FastAPI)
├── users/              # Microservice User
├── traefik/            # Configuration Traefik
├── consul/             # Configuration Consul
├── vault/              # Configuration HashiCorp Vault
├── docker-compose.yml  # Stack complète
└── .env                # Variables d’environnement

````

---

## 🚀 Lancer le projet

### Prérequis

- Docker + Docker Compose
- Ports ouverts : `80`, `8500`, `8200`, etc.

### Commandes

```bash
# Cloner le projet
git clone https://github.com/ThierryMoi/djassa.git
cd djassa

# Lancer l’ensemble des services
docker compose up --build
````

📝 Accès utiles :

* Traefik dashboard : [http://localhost:8080](http://localhost:8080)
* Keycloak : [http://localhost:8081](http://localhost:8081)
* Consul : [http://localhost:8500](http://localhost:8500)
* Vault : [http://localhost:8200](http://localhost:8200)

---

## 🔐 Authentification

* Keycloak gère l’émission des tokens
* `auth-proxy` valide les JWT via la clé publique de Keycloak
* Le middleware redirige vers les services si l’utilisateur est authentifié et autorisé
* Les claims (`sub`, `roles`, etc.) sont injectés dans les headers HTTP pour les services en aval

---

## 🧠 Fonctionnalités avancées

* ✅ Validation locale des tokens JWT
* ✅ Injection des rôles dans les headers
* ✅ Service discovery dynamique via Consul
* ✅ Intégration possible avec Vault pour les secrets DB
* 🛠️ Prêt pour extension avec Consul Mesh, OpenTelemetry, etc.

---

## ✅ TODO

* [x] Middleware d'authentification
* [x] Intégration Keycloak
* [x] Configuration de Consul et Vault
* [ ] Intégration de Consul Mesh (WIP)
* [ ] CI/CD GitHub Actions
* [ ] Observabilité (Prometheus/Grafana)

---

## 📄 Licence

MIT © ThierryMoi
[GitHub Repository](https://github.com/ThierryMoi/djassa)

---

## 🤝 Contributions

Les contributions sont les bienvenues !
Forkez le repo, créez une branche, proposez un PR 🧪
