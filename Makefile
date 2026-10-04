vc ?= valk

test:
	$(vc) build ./tests --test --run
lint:
	$(vc) build ./src --lint
example:
	$(vc) build ./example --run
bench:
	$(vc) build ./bench -o bench/run && ./bench/run
docs:
	$(vc) doc . -o docs/api.md --markdown --no-private
	$(vc) doc . -o docs/api-full.md --markdown --no-private --full
server:
	./tests/server.sh up
server-down:
	./tests/server.sh down

.PHONY: test lint example bench docs server server-down
