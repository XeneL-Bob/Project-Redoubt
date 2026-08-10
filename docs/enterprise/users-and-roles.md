# ResTech — Users and Roles

## 1. Purpose

This document defines representative user populations, identities, roles and access requirements within the ResTech environment.

---

## 2. User Types

| User Type | Description |
|---|---|
| Employee | Standard permanent employee |
| Developer | Software engineering employee |
| Researcher | Research and development employee |
| Finance User | Finance department employee |
| HR User | Human Resources employee |
| Security Analyst | Security monitoring employee |
| IT Administrator | Infrastructure administrator |
| Security Administrator | Security platform administrator |
| Executive | Senior business leadership |
| Contractor | External temporary worker |
| Service Account | Non-human system identity |
| Application Workload | Application or API identity |

---

## 3. Example User Accounts

All identities are fictional and exist only within the Aegis-Fabric laboratory.

| Username | Department | Purpose |
|---|---|---|
| alice.employee | Corporate | Standard employee |
| bob.developer | Engineering | Developer |
| carol.finance | Finance | Finance employee |
| david.research | Research and Development | Researcher |
| emma.hr | Human Resources | HR employee |
| frank.security | Cybersecurity | Security analyst |
| grace.it | Information Technology | Infrastructure administrator |
| henry.executive | Executive | Executive |
| erin.contractor | External | Contractor |
| admin.infrastructure | Information Technology | Privileged infrastructure administrator |
| admin.security | Cybersecurity | Privileged security administrator |

---

## 4. User Groups

```text
Employees
Developers
Researchers
Finance
Human-Resources
Security-Analysts
IT-Administrators
Security-Administrators
Executives
Contractors
```

---

## 5. Application Roles

```text
employee-user
developer
researcher
finance-reader
finance-approver
finance-admin
hr-user
security-analyst
security-admin
infrastructure-admin
application-admin
```

---

## 6. Privilege Model

ResTech separates normal user identities from highly privileged administrative identities.

For example:

```text
grace.it
```

is used for:

- email
- collaboration
- documentation
- normal corporate applications

Whereas:

```text
admin.infrastructure
```

is used for:

- server administration
- infrastructure management
- privileged systems

Administrative credentials must not be used for routine productivity tasks.

---

## 7. Contractor Restrictions

Contractors should:

- receive time-limited access
- receive only project-specific permissions
- be blocked from privileged systems
- be blocked from Finance systems unless explicitly authorised
- be blocked from HR systems
- be monitored separately where appropriate
- lose access when contracts expire

---

## 8. Example Role Permissions

### Employee

Allowed:

```text
Employee Portal
Corporate directory
Internal documentation
Approved collaboration systems
```

Denied:

```text
Production databases
Finance administration
Security management
Identity administration
Infrastructure management
```

### Developer

Allowed:

```text
Source repositories
Development environment
CI/CD development functions
Developer documentation
Test applications
```

Conditional:

```text
Production logs
Deployment systems
Production troubleshooting
```

Denied by default:

```text
Direct production database administration
Identity administration
Finance information
HR records
```

### Finance User

Allowed:

```text
Finance application
Invoice information
Approved financial records
```

Denied:

```text
Security management
Infrastructure administration
HR administration
Developer infrastructure
```

### Security Analyst

Allowed:

```text
SIEM
Security alerts
Endpoint telemetry
Network telemetry
Security investigation tools
```

Denied by default:

```text
Modify payroll
Modify HR records
Modify business applications
```

### Infrastructure Administrator

Allowed:

```text
Server administration
Network administration
Cloud administration
Infrastructure management
```

Restricted:

```text
Security logs
Finance information
HR records
Customer data
```

Infrastructure administration does not automatically provide access to business information.

### Security Administrator

Allowed:

```text
SIEM configuration
Security policy management
Security platform administration
Incident-response tooling
```

Restricted:

```text
Finance records
Payroll
HR records
Business application data
```

---

## 9. Service and Workload Identities

Applications must use unique identities.

Examples:

```text
svc.employee-portal
svc.finance-api
svc.admin-api
svc.logging-agent
svc.backup-service
svc.cicd-runner
```

Each identity should have access only to resources required by its function.

For example:

```text
svc.finance-api
```

may access:

```text
Finance Database
```

but must not automatically access:

```text
HR Database
Security management infrastructure
Identity administration
Research Database
```

---

## 10. Access Control Principles

- Default deny
- Least privilege
- Explicit authorisation
- Separation of privileged and standard identities
- Unique identities for users and workloads
- Time-limited contractor access
- Regular access reviews
- Privileged activity logging
