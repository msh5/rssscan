.PHONY: graph vendoring

graph:
	tools/update_graph.sh

vendoring:
	tools/update_vendor.sh
