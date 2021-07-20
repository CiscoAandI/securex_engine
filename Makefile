SECRET_VARS=-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY

.PHONY: build-engine $(tag)
build-engine:
	docker build -t securex_engine:$(tag) ops/containers/engine/

.PHONY: run-workflow $(tag) $(workflow) $(scenario)
run-workflow:
	${MAKE} build-engine tag=$(tag)
	docker run -it ${SECRET_VARS} -v $(PWD):/engine sxo_local_engine:latest objects/automation/workflows/$(workflow).json tests/inputs/$(workflow)/$(scenario).json

.PHONY: test $(tag)
test:
	${MAKE} build-engine tag=$(tag)
	docker run -it ${SECRET_VARS} -v $(PWD):/engine --entrypoint bash sxo_local_engine:latest -c "PYTHONPATH=./src pytest -v tests"

.PHONY: audit $(tag)
audit:
	${MAKE} build-engine tag=$(tag)
	docker run -it ${SECRET_VARS} -v $(PWD):/engine --entrypoint bash sxo_local_engine:latest -c "PYTHONPATH=./src python tests/audit.py"