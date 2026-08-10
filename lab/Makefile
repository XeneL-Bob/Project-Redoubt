COMPOSE=docker compose --env-file .env -f compose.yaml

.PHONY: validate build up ps logs policy-test segmentation-test detection-test test down reset

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

test:
	./tests/smoke.sh
	./tests/segmentation-test.sh
	./tests/detection-test.sh

down:
	$(COMPOSE) down

reset:
	$(COMPOSE) down -v --remove-orphans
