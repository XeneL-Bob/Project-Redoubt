# ResTech — Attack Surface

## 1. Purpose

The attack surface represents systems, interfaces and identities through which an attacker may interact with ResTech.

---

## 2. External Attack Surface

### Internet-Facing Applications

Examples:

- Customer Portal
- public APIs
- reverse proxy
- authentication endpoints

Potential threats:

- vulnerable application components
- authentication attacks
- injection
- session theft
- API abuse
- denial of service

---

## 3. Identity Attack Surface

Includes:

- login portals
- MFA workflows
- password reset
- session tokens
- privileged identities
- service identities
- contractor identities

Potential threats:

- phishing
- credential theft
- MFA fatigue or misuse
- token theft
- excessive privilege
- dormant accounts
- account manipulation

---

## 4. Endpoint Attack Surface

Includes:

- employee laptops
- developer workstations
- administrator workstations
- contractor devices
- executive devices

Potential threats:

- malicious files
- browser exploitation
- credential theft
- malware execution
- local privilege escalation
- persistence

---

## 5. Application Attack Surface

Includes:

- Employee Portal
- Finance Application
- Customer Portal
- Research Platform
- Admin Console
- internal APIs

Potential threats:

- broken authorisation
- application exploitation
- injection
- insecure API access
- exposed credentials
- excessive workload permissions

---

## 6. Network Attack Surface

Includes:

- firewall rules
- internal network services
- remote access
- management interfaces
- application-to-database communication
- cloud network paths

Primary concern:

```text
Compromise of one zone
        ↓
Unnecessary reachability
        ↓
Discovery
        ↓
Lateral Movement
        ↓
Crown Jewel
```

---

## 7. Development Attack Surface

Includes:

- source repositories
- developer identities
- CI/CD
- build agents
- dependencies
- package sources
- container registry
- deployment credentials

Potential consequence:

```text
Development Compromise
        ↓
Trusted Build Process
        ↓
Malicious Artifact
        ↓
Production
```

---

## 8. Secrets Attack Surface

Includes:

- API credentials
- service credentials
- private keys
- signing keys
- database passwords
- CI/CD secrets

Secrets must not become a shortcut around the intended authorisation architecture.

---

## 9. Security-System Attack Surface

Includes:

- SIEM
- endpoint monitoring
- IDS
- log storage
- vulnerability scanner
- incident-response systems

Attackers may target security infrastructure to:

- delete evidence
- suppress alerts
- disable sensors
- manipulate configuration

---

## 10. Backup Attack Surface

Includes:

- backup service identities
- storage
- administrative interfaces
- recovery credentials
- backup configuration

Backup systems must be considered attacker targets rather than passive infrastructure.

---

## 11. Attack-Surface Priorities

Highest priority attack surfaces are:

1. Identity
2. Privileged administration
3. Internet-facing applications
4. Application-to-database access
5. CI/CD
6. Secrets management
7. Security monitoring
8. Backup administration
