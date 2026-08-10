COMPOSE=docker compose --env-file .env -f compose.yaml

.PHONY: validate build up ps logs policy-test segmentation-test detection-test test down reset adversary-test incident-recovery-test

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

test:
	./tests/smoke.sh
	./tests/segmentation-test.sh
	./tests/detection-test.sh
	python3 adversary/runner.py
	./tests/incident-recovery-test.sh

down:
	$(COMPOSE) down

reset:
	$(COMPOSE) down -v --remove-orphans
