.PHONY: build-engine
build-engine:
	docker build -t sxo_local_engine:latest ops/containers/engine/
	
.PHONY: run-workflow $(workflow) $(scenario)
run-workflow:
	${MAKE} build-engine
	docker run -it -e SXO_LOCAL_SECRET_KEY -v $(PWD):/engine sxo_local_engine:latest objects/automation/workflows/$(workflow).json tests/inputs/$(workflow)/$(scenario).json
	
.PHONY: encrypt-all $(path) $(secret)
encrypt-all:
	if [ -z $(secret) ]; then \
		echo "Please provide the secret using 'secret=<secret>'"; \
		exit 1; \
	fi
	${MAKE} build-engine
	for f in "objects/account_keys/*"; do \
		docker run -it -v $(PWD)/objects:/objects -v $(PWD)/src:/src sxo_local_engine:latest encrypt $$f $(secret); \
	done

.PHONY: test
test:
	${MAKE} build-engine
	docker run -it -v $(PWD):/engine -e SXO_LOCAL_SECRET_KEY --entrypoint bash sxo_local_engine:latest -c "PYTHONPATH=./src pytest -v tests"

.PHONY: audit
audit:
	${MAKE} build-engine
	docker run -it -v $(PWD):/engine -e SXO_LOCAL_SECRET_KEY --entrypoint bash sxo_local_engine:latest -c "PYTHONPATH=./src python tests/audit.py"