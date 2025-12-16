uv_install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

install: # this only installs the packages from the uv.lock
	uv sync --all-packages

upgrade_packages: # this upgrades the packages and installs them
	uv lock --upgrade
	uv sync --all-packages



# Server commands
server: # start FastAPI server
	uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

chat: # start Streamlit chat app
	uv run streamlit run streamlit-chat/main.py

# executing pre-commit multiple times as sometimes one execution is not enough to format everything correctly
formatting:
	for i in 1 2 3 4 5; do uv run pre-commit run --all-files && break; done
	make type_check

# dev_server:
# 	uv run fastapi dev src/gserver/gserver/__main__.py

# server:
# 	uv run -m gserver

# gpsp:
# 	uv run -m gpsp

# uvicorn_server:
# 	uv run uvicorn gserver.__main__:app --host 0.0.0.0 --port 8000

# Usage examples:
# app:
# 	uv run streamlit run src/gapp/gapp/main.py

# Does not open new tab on streamlit restart
# app_headless:
# 	streamlit run src/gapp/gapp/main.py --server.headless true







# Alembic
# alembic_init:
# 	uv run alembic revision --autogenerate -m "initial migration"

# alembic_migration_generate:
# 	@[ -z "$(description)" ] && { \
# 	    echo "Error: description variable is required."; \
# 	    echo "Usage: make alembic_migration_generate description=\"description of change\""; \
# 	    exit 1; \
# 	} || true
# 	uv run alembic $(ALEMBIC_CONFIG) revision --autogenerate -m "$(description)"

# alembic_migration_apply:
# 	uv run alembic upgrade head

# alembic_downgrade:
# 	uv run alembic downgrade -1

# Local postgres for alembic:
# local_postgres:
# 	bash -c '\
# 	set -euo pipefail; \
# 	CERTS_DIR=$$(pwd)/pg_ssl_certs; \
# 	CONTAINER_NAME=chatbot-postgres-ssl; \
# 	VOLUME_NAME=chatbot-postgres-data; \
# 	mkdir -p $$CERTS_DIR; \
# 	if [ ! -f "$$CERTS_DIR/server.crt" ]; then \
# 	  echo "🔐 Generating self-signed SSL certs..."; \
# 	  openssl req -new -x509 -days 365 \
# 	    -nodes -text \
# 	    -out $$CERTS_DIR/server.crt \
# 	    -keyout $$CERTS_DIR/server.key \
# 	    -subj "/CN=localhost"; \
# 	  chmod 600 $$CERTS_DIR/server.key; \
# 	fi; \
# 	docker volume create $$VOLUME_NAME >/dev/null; \
# 	docker rm -f $$CONTAINER_NAME 2>/dev/null || true; \
# 	docker run --name $$CONTAINER_NAME \
# 	  -e POSTGRES_USER=devuser \
# 	  -e POSTGRES_PASSWORD=devpass \
# 	  -e POSTGRES_DB=postgres \
# 	  -v $$CERTS_DIR:/var/lib/postgresql/certs:ro \
# 	  -v $$VOLUME_NAME:/var/lib/postgresql/data \
# 	  -p 5433:5432 \
# 	  -d postgres:15 \
# 	  -c ssl=on \
# 	  -c ssl_cert_file=/var/lib/postgresql/certs/server.crt \
# 	  -c ssl_key_file=/var/lib/postgresql/certs/server.key; \
# 	echo "✅ Postgres with SSL + persistent volume is running!"; \
# 	echo; \
# 	echo "Use these connection settings:"; \
# 	echo "  Host: 127.0.0.1"; \
# 	echo "  Port: 5433"; \
# 	echo "  User: devuser"; \
# 	echo "  Password: devpass"; \
# 	echo "  Database: postgres"'
# Fully reset it → deletes container AND volume
# reset_local_postgres:
# 	@set -euo pipefail; \
# 	CONTAINER_NAME=chatbot-postgres-ssl; \
# 	VOLUME_NAME=chatbot-postgres-data; \
# 	docker rm -f $$CONTAINER_NAME || true; \
# 	docker volume rm $$VOLUME_NAME || true; \
# 	$(MAKE) local_postgres

type_check:
	uv run ty check .

# Testing:
#
# TEST_PATH (default: .)
#   - Specifies the path to the tests or codebase you want to test.
#
# TEST_TYPE (default: all)
#   - Determines which tests to run based on pytest markers.
#   - Options:
#       - all: Runs all tests marked as unit, integration_deterministic, or integration_indeterministic.
#       - unit: Runs tests marked as unit tests only.
#       - integration_deterministic: Runs tests marked as deterministic integration tests only.
#       - integration_indeterministic: Runs tests marked as indeterministic integration tests only.
#
# MULTIPROCESS (default: 15)
#   - Configures the number of processes for parallel test execution.
#   - Options:
#       - An integer (e.g., 4): Number of processes to use.
#       - "auto": Pytest-xdist decides the optimal number of processes.
#       - "false" or "0": Disables multiprocessing entirely.
#   - The reason 15 is the default is that it has been tested to work nicely with GH
#   actions in our case.  If we set it to auto, we get n=1, because there is one CPU
#   available on GH actions. Our tests are not CPU-bound though, so still even though
#   there are multiple processes spawned, while only having 1 CPU, we experience a
#   speed up. Threading is not a good, viable option in pytest.
#
# Usage Examples:
#   - Run all tests with default settings, tolerating up to 3 failures:
#       make testing
#
#   - Run tests with up to 5 tolerated failures:
#       make testing
#
#   - Run unit tests only, no multiprocessing, tolerate up to 2 failures:
#       make testing TEST_TYPE=unit MULTIPROCESS=false
#
#	- Run deterministic integration tests:
#       make testing_integration_deterministic
#
#   - Run indeterministic integration tests with 3 tolerated failures:
#       make testing_integration_indeterministic

# $(eval TEST_PATH ?= .)
# $(eval TEST_TYPE ?= all)

# # Default worker count per test type - used for optimal CI - multiple workers in CI are expensive
# ifeq ($(TEST_TYPE),unit)
#     $(eval MULTIPROCESS ?= 3)
# else ifeq ($(TEST_TYPE),integration_deterministic)
#     $(eval MULTIPROCESS ?= 7)
# else ifeq ($(TEST_TYPE),testing_integration_indeterministic_with_flaky_analysis)
#     $(eval MULTIPROCESS ?= 50)
# else
#     $(eval MULTIPROCESS ?= 50)
# endif

# # Determine parallel flag
# ifneq ($(filter $(MULTIPROCESS),false 0),)
#     PARALLEL_FLAG :=
# else
#     PARALLEL_FLAG := -n $(MULTIPROCESS)
# endif
# ifeq ($(TEST_TYPE),all)
#     PYTEST_MARKERS :=
# else
#     PYTEST_MARKERS := -m $(TEST_TYPE)
# endif
# # only generate coverage for unit tests
# ifeq ($(TEST_TYPE),unit)
#   COV_FLAGS := --cov=$(TEST_PATH) --cov-report=html --cov-report=term
# else
#   COV_FLAGS :=
# endif

# testing:
# 	@uv run pytest $(PARALLEL_FLAG) $(PYTEST_MARKERS) $(TEST_PATH) \
# 	  $(COV_FLAGS) \
# 	  --html=outputs/pytest_report.html \
# 	  -v --tb=short

# testing_unit:
# 	$(MAKE) testing TEST_TYPE=unit

# testing_integration_deterministic:
# 	$(MAKE) testing TEST_TYPE=integration_deterministic

# testing_integration_indeterministic:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic --multiprocess $(MULTIPROCESS) $(if $(SCENARIO_TYPE),--test-args '-k $(SCENARIO_TYPE)',)

# testing_integration_indeterministic_nettium:
# 	$(MAKE) testing_integration_indeterministic SCENARIO_TYPE=integration_nettium

# testing_integration_indeterministic_yolo:
# 	$(MAKE) testing_integration_indeterministic SCENARIO_TYPE=integration_yolo

# testing_integration_indeterministic_gpsp:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic --multiprocess $(MULTIPROCESS) --test-path 'src/gpsp'

# testing_integration:
# 	$(MAKE) testing_integration_deterministic && $(MAKE) testing_integration_indeterministic_with_flaky_analysis

# testing_ginpipe_docker:
# 	unset GINPIPE_RUN_SCHEDULE_IN_MINUTES && \
# 	GINPIPE_EXPORTERS='["SummaryExporter"]' \
# 	docker compose up --build ginpipe

# testing_gserver_docker:
# 	# Docker smoke test
# 	@set -e; \
# 	trap 'EXIT_CODE=$$?; \
# 		if [ $$EXIT_CODE -ne 0 ]; then \
# 			echo "🔴 Test failed. Showing backend logs:"; \
# 			docker logs backend; \
# 		fi; \
# 		docker rm -f backend; \
# 		exit $$EXIT_CODE' EXIT; \
# 	docker compose up --build backend -d --wait; \
# 	docker cp src/gserver/tests backend:/usr/src/app/tests; \
# 	docker exec backend uv run --no-project pytest -k test_nettium_endpoint_works_e2e

# # Run a specific test scenario for a specific language multiple times
# # Usage:
# # 	make testing_multi_run PYTEST_ARGS="-k deposit_4-m999" RUNS=10
# RUNS          ?= 1
# testing_multi_run:
# 	@echo "Running tests x$(RUNS) with log level $(LOGURU_LEVEL)"
# 	@uv run scripts/test_runner_utils.py testing_multi_run --repeat-count $(RUNS) --test-args '$(PYTEST_ARGS)'
# 	@echo "Test summary report generated at: outputs/testing_multi_run_report.html"

# # Run integration indeterministic tests with flakiness analysis
# # This command:
# # 1. Runs all integration indeterministic tests
# # 2. For any failed tests, reruns them using testing_multi_run command
# # 3. Fails if success rate for any rerun test is below specified threshold
# #
# # Parameters:
# #   MULTIPROCESS: Number of processes (default: 50)
# #   RERUN_COUNT: Number of reruns for failed tests (default: 20)
# #   MIN_SUCCESS_RATE: Minimum success rate percentage (default: 95)
# $(eval MULTIPROCESS ?= 50)
# $(eval RERUN_COUNT ?= 20)
# $(eval MIN_SUCCESS_RATE ?= 95)
# testing_integration_indeterministic_with_flaky_analysis:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic_with_flaky_analysis --multiprocess $(MULTIPROCESS) --rerun-count $(RERUN_COUNT) --min-success-rate $(MIN_SUCCESS_RATE)

# testing_integration_indeterministic_nettium_with_flaky_analysis:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic_with_flaky_analysis --multiprocess $(MULTIPROCESS) --rerun-count $(RERUN_COUNT) --min-success-rate $(MIN_SUCCESS_RATE) --test-args '-k integration_nettium'

# testing_integration_indeterministic_yolo_with_flaky_analysis:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic_with_flaky_analysis --multiprocess $(MULTIPROCESS) --rerun-count $(RERUN_COUNT) --min-success-rate $(MIN_SUCCESS_RATE) --test-args '-k integration_yolo'

# testing_integration_indeterministic_gpsp_with_flaky_analysis:
# 	@uv run scripts/test_runner_utils.py testing_integration_indeterministic_with_flaky_analysis --multiprocess $(MULTIPROCESS) --rerun-count $(RERUN_COUNT) --min-success-rate $(MIN_SUCCESS_RATE) --test-path 'src/gpsp'

# yolo_frontend_local:
# 	@echo "Frontend server starting at http://localhost:8080"
# 	@echo "Available widgets:"
# 	@echo "  - dev0: http://localhost:8080/index.html?widget=dev0"
# 	@echo "  - dev1: http://localhost:8080/index.html?widget=dev1"
# 	@echo "  - develop: http://localhost:8080/index.html?widget=develop"
# 	@echo "  - staging: http://localhost:8080/index.html?widget=staging"
# 	@echo "  - fomo7: http://localhost:8080/index.html?widget=fomo7"
# 	@echo "  - yolo247: http://localhost:8080/index.html?widget=yolo247"
# 	@echo "  - fun88: http://localhost:8080/index.html?widget=fun88"
# 	@echo "  - iw247: http://localhost:8080/index.html?widget=iw247"
# 	cd src/yolo_frontend/frontend && python -m http.server 8080

# $(eval bot-status ?= New)
# psp_update_support_case:
# 	@uv run src/gpsp/scripts/update_support_case.py $(client) $(ticket-id) --bot-status=$(bot-status)

# psp_reset_yolo_dev:
# 	uv run src/gpsp/scripts/update_support_case.py yolo --reset
