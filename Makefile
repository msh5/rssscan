.PHONY: diagram vendoring

diagram:
	tools/update_diagram.sh

vendoring:
	tools/update_vendor.sh
