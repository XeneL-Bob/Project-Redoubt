# Project Redoubt — Infrastructure as Code

## Purpose

Phase 11 converts Project Redoubt security architecture into declarative Infrastructure as Code and enforceable Policy as Code.

The infrastructure in this directory is a reference architecture.

It is designed for:

- architecture validation
- security policy testing
- CI validation
- misconfiguration simulation
- control traceability
- portfolio evidence

It is not intended to be deployed into a production AWS account without additional production engineering and review.

## Reference Architecture

The reference environment maps Project Redoubt trust zones into cloud infrastructure:

- Edge
- Application
- Data
- Management
- Recovery
- Telemetry

OpenTofu defines the desired infrastructure state.

OPA policies will evaluate the OpenTofu plan before deployment authority is granted.

## Security Principle

The Phase 11 control path is:

    Infrastructure Change
            |
            v
        OpenTofu
            |
            v
         Plan JSON
            |
            v
        OPA Policies
        /          \
      DENY         ALLOW
       |             |
       v             v
    Reject        Approved
    Change        Architecture

Infrastructure configuration is therefore treated as a security-sensitive artifact rather than an unaudited administrative action.
