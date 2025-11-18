.PHONY: integration

integration:
	docker compose -f docker-compose.test.yml up -d --build
	./scripts/wait_for_api.sh http://localhost:5000
	pytest -v tests_integration
	docker compose -f docker-compose.test.yml down
