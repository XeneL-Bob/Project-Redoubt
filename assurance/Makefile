.PHONY: baseline graph coverage end-to-end test

baseline:
	python3 validate_baseline.py

graph: baseline
	python3 validate_graph.py

coverage: graph
	python3 analyze_coverage.py

end-to-end: coverage
	python3 validate_end_to_end.py

test: end-to-end
