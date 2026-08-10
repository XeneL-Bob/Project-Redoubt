# ResTech — Network Segmentation Architecture

## 1. Purpose

Network segmentation reduces attacker reachability and limits lateral movement.

Segmentation supports Zero Trust but does not replace identity or authorisation.

---

## 2. Security Zones

Project Redoubt defines the following logical zones:

```text
ZONE-01 Edge / DMZ
ZONE-02 Corporate Users
ZONE-03 Applications
ZONE-04 Databases
ZONE-05 Development
ZONE-06 Management
ZONE-07 Security
ZONE-08 Backup / Recovery
ZONE-09 Attack Simulation
ZONE-10 Guest
```

---

## 3. Zone Architecture

```text
                 INTERNET
                    │
                    ▼
             [ EDGE / DMZ ]
                    │
                    ▼
             [ APPLICATION ]
                    │
                    ▼
              [ DATABASE ]


[ CORPORATE ]       [ DEVELOPMENT ]
     │                    │
     └────────┬───────────┘
              │
         controlled
          pathways


[ MANAGEMENT ]       [ SECURITY ]
       │                  │
       └──── restricted ──┘


[ BACKUP / RECOVERY ]
       │
 isolated administration


[ ATTACK LAB ]
       │
 explicitly contained
```

---

## 4. Default Network Policy

```text
Inter-zone traffic:
DENY by default
```

Explicit flows must be documented.

---

## 5. Example Allowed Flows

| Source | Destination | Purpose |
|---|---|---|
| Internet | Reverse Proxy | Public application access |
| Reverse Proxy | Customer Portal | Application request |
| Customer Portal | Customer DB | Authorised workload query |
| Finance App | Finance DB | Finance application query |
| Users | Identity Provider | Authentication |
| Systems | SIEM | Telemetry |
| Admin Workstation | Management Plane | Administration |
| CI/CD | Approved Production Endpoint | Deployment |

---

## 6. Explicitly Denied Flows

```text
Corporate User → Production Database

Guest → Internal Application

Contractor → Management Network

Development Workstation → Finance Database

Application Zone → Management Network

Attack Lab → Production Network

Normal User → Backup Administration
```

---

## 7. Database Isolation

Databases should normally accept requests from authorised application workloads rather than normal user endpoints.

Preferred:

```text
User
 ↓
Application
 ↓
Workload Identity
 ↓
Database
```

Denied:

```text
User
──────────────>
Database
```

---

## 8. Management Network

Management interfaces must be isolated from the standard corporate-user network.

Administration should originate from approved administration paths.

---

## 9. Attack Lab Isolation

The adversary-simulation environment must have no uncontrolled route into production-like environments.

All connections used for testing must be explicitly defined.

---

## 10. Related Risks

- R-003 Lateral Movement
- R-004 Customer Data Exfiltration
- R-009 Backup Destruction
- R-011 Compromised Application Workload
