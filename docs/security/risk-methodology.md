# ResTech — Cybersecurity Risk Methodology

## 1. Purpose

This document defines the risk-assessment methodology used within Project Redoubt.

The methodology provides a repeatable way to evaluate cybersecurity risks affecting the fictional ResTech enterprise.

The objective is to support architecture prioritisation rather than provide a formal regulatory risk certification.

---

## 2. Risk Model

Project Redoubt uses the following simplified risk model:

```text
Threat
   +
Vulnerability / Exposure
   ↓
Likelihood
   +
Business Impact
   ↓
Inherent Risk
   ↓
Security Controls
   ↓
Residual Risk
```

Risk is assessed using:

```text
Risk Score = Likelihood × Impact
```

Both Likelihood and Impact are rated from 1 to 5.

The resulting score ranges from 1 to 25.

---

## 3. Likelihood Scale

| Score | Rating | Description |
|---:|---|---|
| 1 | Rare | Highly unlikely under expected conditions |
| 2 | Unlikely | Possible but requires unusual circumstances |
| 3 | Possible | Credible scenario that may occur |
| 4 | Likely | Expected to occur without sufficient controls |
| 5 | Almost Certain | Highly probable or routinely observed threat scenario |

Likelihood considers:

- attack surface
- exposure
- attacker capability
- accessibility
- control maturity
- credential exposure
- common attack techniques
- organisational complexity

---

## 4. Impact Scale

| Score | Rating | Description |
|---:|---|---|
| 1 | Insignificant | Minimal business effect |
| 2 | Minor | Limited operational disruption |
| 3 | Moderate | Material operational or financial impact |
| 4 | Major | Significant organisational impact |
| 5 | Severe | Enterprise-wide, legal, safety, financial or strategic impact |

Impact considers:

- confidentiality
- integrity
- availability
- customer harm
- financial loss
- operational disruption
- intellectual-property loss
- regulatory consequences
- recovery difficulty
- attacker privilege gained

---

## 5. Risk Rating

| Score | Rating |
|---:|---|
| 1–4 | Low |
| 5–9 | Moderate |
| 10–16 | High |
| 17–25 | Critical |

Example:

```text
Likelihood: 4
Impact:     5

Risk = 4 × 5
Risk = 20

Rating = Critical
```

---

## 6. Inherent Risk

Inherent risk represents the risk level before the planned Project Redoubt security architecture is applied.

Example:

```text
Threat:
Stolen administrator credentials

Likelihood:
4 — Likely

Impact:
5 — Severe

Inherent Risk:
20 — Critical
```

Inherent risk helps identify where security investment should be prioritised.

---

## 7. Planned Controls

Controls are grouped into four functional categories.

### Preventive Controls

Designed to reduce the probability of successful compromise.

Examples:

- MFA
- least privilege
- segmentation
- hardened configuration
- application allow-listing
- secure software controls

### Detective Controls

Designed to identify suspicious or malicious behaviour.

Examples:

- SIEM detections
- endpoint telemetry
- network monitoring
- authentication anomaly detection
- policy-denial monitoring

### Responsive Controls

Designed to contain or remove an active threat.

Examples:

- session revocation
- account disablement
- endpoint isolation
- network blocking
- credential rotation

### Recovery Controls

Designed to restore trusted operation.

Examples:

- immutable backups
- configuration restoration
- identity recovery procedures
- redeployment from trusted infrastructure definitions

---

## 8. Residual Risk

Residual risk is the estimated risk remaining after planned controls have been implemented successfully.

During early Project Redoubt phases, residual scores represent **target residual risk**, not validated control effectiveness.

Actual residual risk can only be confirmed once:

- controls are implemented
- controls are tested
- attack scenarios are executed
- detection capability is measured
- recovery procedures are validated

This distinction prevents Project Redoubt from claiming security effectiveness before evidence exists.

---

## 9. Risk Treatment

Each risk receives one of the following treatment approaches:

| Treatment | Meaning |
|---|---|
| Mitigate | Reduce likelihood or impact through controls |
| Avoid | Remove the activity or exposure creating the risk |
| Transfer | Transfer part of the risk to another party |
| Accept | Explicitly retain the residual risk |

Project Redoubt will primarily demonstrate risk mitigation.

---

## 10. Risk Ownership

Every significant risk should eventually have:

- a risk owner
- affected assets
- relevant threats
- planned controls
- target residual risk
- validation method

For the fictional ResTech environment, ownership is assigned by functional role rather than real individuals.

Example roles include:

- Chief Information Security Officer
- Security Architecture
- Infrastructure Engineering
- Application Engineering
- Data Owner
- Identity and Access Management
- Security Operations

---

## 11. Risk Validation

A risk is not considered effectively mitigated solely because a control exists.

Controls should eventually be validated through:

```text
Configuration Review
        ↓
Automated Security Test
        ↓
Adversary Simulation
        ↓
Telemetry Validation
        ↓
Incident Response Validation
        ↓
Residual Risk Reassessment
```

This validation process will become a major component of later Project Redoubt phases.

---

## 12. Risk Register Fields

The Project Redoubt risk register records:

- Risk ID
- Risk statement
- Affected crown jewels
- Threat source
- Likelihood
- Impact
- Inherent risk score
- Inherent risk rating
- Planned controls
- Target residual likelihood
- Target residual impact
- Target residual score
- Target residual rating
- Risk treatment
- Validation method

---

## 13. Risk Statement Format

Risk statements use the structure:

> There is a risk that **[threat event]**, because of **[exposure or weakness]**, resulting in **[business or security impact]**.

Example:

> There is a risk that a compromised privileged identity could be used to gain broad administrative control because privileged credentials provide access to multiple critical systems, resulting in enterprise-wide compromise.

This structure keeps risks connected to both technical cause and business consequence.
