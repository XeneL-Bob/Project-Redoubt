# ResTech — Management Plane Architecture

## 1. Purpose

The management plane controls the systems that control other systems.

It is therefore treated as one of the highest-value security boundaries.

---

## 2. Management Assets

Includes:

- identity administration
- network administration
- cloud administration
- hypervisor administration
- security administration
- secrets administration
- backup administration
- CI/CD administration

---

## 3. Management Access

Preferred model:

```text
Administrator
      │
      ▼
Dedicated Admin Identity
      │
      ▼
Strong Authentication
      │
      ▼
Approved Admin Workstation
      │
      ▼
Management Network
      │
      ▼
Administrative Interface
```

---

## 4. Denied Model

```text
Normal Employee Laptop
       │
       X
       │
       ▼
Critical Administration
```

---

## 5. Administrative Separation

Project Redoubt distinguishes:

```text
Infrastructure Administration
Security Administration
Identity Administration
Backup Administration
Application Administration
```

No single administrative role should automatically control all domains.

---

## 6. Backup Separation

A production infrastructure administrator should not automatically have unrestricted backup deletion rights.

This reduces the likelihood that one compromised privileged identity can destroy both:

```text
Production
+
Recovery
```

---

## 7. Security Platform Administration

Security analysts may investigate events without automatically possessing security-platform administrative privileges.

Example:

```text
security-analyst
≠
security-admin
```

---

## 8. Administrative Telemetry

Every critical administrative action should identify:

- administrator
- authentication event
- source device
- target system
- action
- result
- timestamp

---

## 9. Related Attack Paths

- AP-002 Compromised Administrator
- AP-005 Ransomware
- AP-008 Security Platform Compromise
