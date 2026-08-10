# ResTech — MITRE ATT&CK Mapping

## 1. Purpose

Project Redoubt uses MITRE ATT&CK to relate architectural threat scenarios to recognised adversary behaviours.

ATT&CK is used as a threat-informed reference, not as a compliance checklist.

---

## 2. Initial Access

| Technique | ID | Project Redoubt Scenario |
|---|---|---|
| Phishing | T1566 | Employee credential or endpoint compromise |
| Exploit Public-Facing Application | T1190 | Customer Portal or exposed API compromise |
| Valid Accounts | T1078 | Use of stolen employee, contractor or administrator account |

---

## 3. Execution

| Technique | ID | Scenario |
|---|---|---|
| Command and Scripting Interpreter | T1059 | Command execution following endpoint or workload compromise |

---

## 4. Persistence and Privilege

| Technique | ID | Scenario |
|---|---|---|
| Valid Accounts | T1078 | Maintain access through legitimate credentials |
| Account Manipulation | T1098 | Modify account or privilege configuration |

---

## 5. Credential Access

| Technique | ID | Scenario |
|---|---|---|
| OS Credential Dumping | T1003 | Credential theft from compromised endpoint |
| Unsecured Credentials | T1552 | Secrets exposed in files, configuration or repositories |

---

## 6. Discovery

| Technique | ID | Scenario |
|---|---|---|
| Network Service Discovery | T1046 | Discover reachable enterprise services |
| Account Discovery | T1087 | Identify users and privileged accounts |
| Permission Groups Discovery | T1069 | Identify privileged groups |

---

## 7. Lateral Movement

| Technique | ID | Scenario |
|---|---|---|
| Remote Services | T1021 | Movement between reachable systems |
| Valid Accounts | T1078 | Reuse compromised credentials across systems |

---

## 8. Collection and Exfiltration

Potential behaviours include:

- collecting customer information
- collecting research
- collecting finance information
- moving information outside authorised boundaries

These behaviours will receive more specific sub-technique mapping when attack simulations are implemented.

---

## 9. Impact

| Technique | ID | Scenario |
|---|---|---|
| Data Encrypted for Impact | T1486 | Ransomware encrypts ResTech information |
| Inhibit System Recovery | T1490 | Attacker attempts to prevent recovery |

---

## 10. Attack-Path Mapping

### AP-001 — Phished Employee

```text
T1566 Phishing
        ↓
T1078 Valid Accounts
        ↓
T1087 Account Discovery
        ↓
T1046 Network Service Discovery
        ↓
T1021 Remote Services
```

---

### AP-003 — Public Application Compromise

```text
T1190 Exploit Public-Facing Application
        ↓
T1059 Command and Scripting Interpreter
        ↓
T1552 Unsecured Credentials
        ↓
T1046 Network Service Discovery
```

---

### AP-005 — Ransomware

```text
Initial Access
      ↓
Credential Access
      ↓
T1078 Valid Accounts
      ↓
Lateral Movement
      ↓
T1490 Inhibit System Recovery
      ↓
T1486 Data Encrypted for Impact
```

---

## 11. ATT&CK Usage in Project Redoubt

Later phases will connect:

```text
ATT&CK Technique
       ↓
Preventive Control
       ↓
Detection
       ↓
Telemetry Source
       ↓
Attack Simulation
       ↓
Observed Result
```

This will allow Project Redoubt to demonstrate not merely that controls exist, but that specific attacker behaviours can be constrained or detected.
