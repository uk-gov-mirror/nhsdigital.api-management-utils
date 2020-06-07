
ansible-lint:
	@# Only swallow checking errors (rc=2), not other problems (rc=1)
	poetry run ansible-lint -c ansible-lint.yml -p ansible/*.yml || test $$? -eq 2