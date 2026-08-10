COMPOSE=docker compose --env-file .env -f compose.yaml

.PHONY: validate build up ps logs policy-test segmentation-test detection-test adversary-test incident-recovery-test privileged-access-test privileged-detection-test supply-chain-test deployment-test test down reset

validate:
	$(COMPOSE) config -q

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --build

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f --tail=100

policy-test:
	./tests/policy-test.sh

segmentation-test:
	./tests/segmentation-test.sh

detection-test:
	./tests/detection-test.sh

adversary-test:
	python3 adversary/runner.py

incident-recovery-test:
	./tests/incident-recovery-test.sh

privileged-access-test:
	./tests/privileged-access-test.sh

privileged-detection-test:
	python3 tests/privileged-detection-test.py
	./tests/privileged-detection-live.sh

deployment-test:
	python3 tests/deployment-detection-test.py
	./tests/deployment-gate-test.sh
	./tests/deployment-detection-live.sh

supply-chain-test:
	./tests/supply-chain-security-test.sh
	python3 tests/supply-chain-detection-test.py
	./tests/supply-chain-detection-live.sh
	python3 tests/deployment-detection-test.py
	./tests/deployment-gate-test.sh
	./tests/deployment-detection-live.sh
	python3 adversary/supply-chain-runner.py

test:
	./tests/smoke.sh
	./tests/segmentation-test.sh
	./tests/detection-test.sh
	python3 adversary/runner.py
	./tests/incident-recovery-test.sh
	./tests/privileged-access-test.sh
	python3 tests/privileged-detection-test.py
	./tests/privileged-detection-live.sh
	./tests/supply-chain-security-test.sh
	python3 tests/supply-chain-detection-test.py
	./tests/supply-chain-detection-live.sh
	python3 tests/deployment-detection-test.py
	./tests/deployment-gate-test.sh
	./tests/deployment-detection-live.sh
	python3 adversary/supply-chain-runner.py

down:
	$(COMPOSE) down

reset:
	$(COMPOSE) down -v --remove-orphans
