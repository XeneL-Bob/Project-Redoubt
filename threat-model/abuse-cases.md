# ResTech — Security Abuse Cases

## 1. Purpose

Abuse cases describe ways legitimate functionality could be intentionally or maliciously misused.

---

## AC-001 — Employee Attempts Finance Access

### Actor

Compromised employee account.

### Action

Attempts to access the Finance Application or Finance API without a Finance role.

### Expected Result

```text
DENY
+
LOG
+
Possible alert
```

### Related Risks

- R-001
- R-005

---

## AC-002 — Developer Attempts Direct Production Database Access

### Actor

Developer.

### Action

Attempts direct network access to a production database.

### Expected Result

```text
NETWORK DENY
```

Development access must not imply production database access.

### Related Risks

- R-003
- R-004

---

## AC-003 — Compromised Workload Requests Unrelated Secret

### Actor

`svc.employee-portal`

### Action

Requests Finance database credentials.

### Expected Result

```text
DENY
+
AUDIT
```

### Related Risks

- R-007
- R-011

---

## AC-004 — Administrator Uses Standard Identity for Privileged Action

### Action

A normal employee identity attempts access to a privileged administration interface.

### Expected Result

Denied because privileged identity separation is required.

### Related Risk

- R-002

---

## AC-005 — Contractor Retains Access After Contract Expiry

### Expected Result

Identity automatically expires or access is revoked.

### Related Risk

- R-010

---

## AC-006 — Application Attempts Lateral Movement

### Scenario

A compromised customer-facing application attempts connections to:

- HR database
- Finance database
- security management
- identity administration

### Expected Result

Unauthorised paths are denied by workload policy and segmentation.

### Related Risk

- R-011

---

## AC-007 — Attacker Deletes Security Logs

### Actor

Compromised administrator.

### Objective

Remove evidence of malicious activity.

### Expected Result

- restricted log administration
- tamper-resistant storage
- administrative action logged elsewhere

### Related Risk

- R-008

---

## AC-008 — Attacker Deletes Backups

### Objective

Prevent recovery before destructive activity.

### Expected Result

Production compromise must not provide unrestricted deletion rights over protected recovery copies.

### Related Risk

- R-009

---

## AC-009 — CI/CD Pipeline Attempts Unapproved Production Deployment

### Expected Result

Deployment is rejected without the required policy or approval condition.

### Related Risk

- R-006

---

## AC-010 — Researcher Bulk Downloads Sensitive Research

### Actor

Legitimate researcher account.

### Concern

The action may be technically authorised but behaviourally unusual.

### Expected Result

- access logged
- unusual retrieval detectable
- investigation possible

### Related Risk

- R-012

---

## 2. Abuse-Case Principle

Successful authentication is not sufficient.

Project Redoubt must evaluate:

```text
WHO
+
WHAT DEVICE
+
WHAT WORKLOAD
+
WHAT RESOURCE
+
WHAT ACTION
+
WHAT CONTEXT
```
