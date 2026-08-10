package restech.authz_test

import data.restech.authz.decision

test_employee_can_read_employee_api if {
    result := decision with input as {
        "subject": {
            "username": "alice.employee",
            "roles": ["employee"]
        },
        "resource": "employee-api",
        "action": "read",
        "context": {
            "device_trusted": true
        }
    }

    result.allow
}

test_employee_cannot_read_finance_api if {
    result := decision with input as {
        "subject": {
            "username": "alice.employee",
            "roles": ["employee"]
        },
        "resource": "finance-api",
        "action": "read",
        "context": {
            "device_trusted": true
        }
    }

    not result.allow
}

test_finance_user_requires_trusted_device if {
    result := decision with input as {
        "subject": {
            "username": "carol.finance",
            "roles": ["employee", "finance-reader"]
        },
        "resource": "finance-api",
        "action": "read",
        "context": {
            "device_trusted": false
        }
    }

    not result.allow
}

test_finance_user_allowed_from_trusted_device if {
    result := decision with input as {
        "subject": {
            "username": "carol.finance",
            "roles": ["employee", "finance-reader"]
        },
        "resource": "finance-api",
        "action": "read",
        "context": {
            "device_trusted": true
        }
    }

    result.allow
}

test_contractor_denied_employee_api if {
    result := decision with input as {
        "subject": {
            "username": "erin.contractor",
            "roles": ["contractor"]
        },
        "resource": "employee-api",
        "action": "read",
        "context": {
            "device_trusted": true
        }
    }

    not result.allow
}
