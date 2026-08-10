package restech.authz

default allow := false

has_role(role) if {
    input.subject.roles[_] == role
}

allow if {
    input.resource == "employee-api"
    input.action == "read"
    has_role("employee")
}

allow if {
    input.resource == "finance-api"
    input.action == "read"
    has_role("finance-reader")
    input.context.device_trusted == true
}

reason := "allowed" if {
    allow
}

reason := "policy_denied" if {
    not allow
}

decision := {
    "allow": allow,
    "reason": reason,
    "subject": input.subject.username,
    "resource": input.resource,
    "action": input.action
}
