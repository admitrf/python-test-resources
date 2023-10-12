.PHONY: build
build:
	docker compose build
	docker compose create

.PHONY: stop
stop:
	docker compose stop

.PHONY: run
run: stop
	docker compose start

.PHONY: clean
clean: stop
	docker compose down
