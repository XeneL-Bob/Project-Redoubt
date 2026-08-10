package restech.admin

default allow := false

has_role(role) if {
    input.subject.roles[_] == role
}

admin_context_valid if {
    input.context.admin_device_trusted == true
    input.context.elevation_active == true
}

allow if {
    input.resource == "infrastructure-management"
    input.action == "read"
    has_role("infrastructure-admin")
    admin_context_valid
}

allow if {
    input.resource == "infrastructure-management"
    input.action == "restart-service"
    has_role("infrastructure-admin")
    admin_context_valid
}

allow if {
    input.resource == "security-management"
    input.action == "read"
    has_role("security-admin")
    admin_context_valid
}

allow if {
    input.resource == "security-management"
    input.action == "update-detection"
    has_role("security-admin")
    admin_context_valid
}

reason := "allowed" if {
    allow
}

reason := "privileged_policy_denied" if {
    not allow
}

decision := {
    "allow": allow,
    "reason": reason,
    "subject": input.subject.username,
    "resource": input.resource,
    "action": input.action
}
