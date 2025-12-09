# Deploy all scripts to Argos directory
deploy:
	mkdir -p ~/.config/argos/secrets
	cp scripts/*.{py,sh} ~/.config/argos/ 2>/dev/null || true
	cp secrets/*.{py,sh} ~/.config/argos/secrets/ 2>/dev/null || true
	@echo "All scripts and secrets deployed to ~/.config/argos/"

# Deploy a specific script
deploy-script SCRIPT:
	mkdir -p ~/.config/argos/secrets
	cp scripts/{{SCRIPT}} ~/.config/argos/
	@./.deploy-secrets.sh scripts/{{SCRIPT}}
	@echo "{{SCRIPT}} deployed to ~/.config/argos/"

# List available scripts
list:
	@echo "Available scripts:"
	@ls -1 scripts/*.{py,sh} 2>/dev/null | xargs -n1 basename || echo "No scripts found"