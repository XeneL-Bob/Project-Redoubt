REFERENCE=environments/reference-aws

.PHONY: fmt validate policy-test real-plan-test security-gate test

fmt:
	tofu fmt -check -recursive .

validate:
	cd $(REFERENCE) && tofu init -backend=false -input=false -lockfile=readonly
	cd $(REFERENCE) && tofu validate

policy-test:
	python3 tests/policy-test.py

real-plan-test:
	python3 tests/real-plan-test.py

security-gate:
	./tests/ci-gate-test.sh

test: security-gate
