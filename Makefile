host ?= 127.0.0.1
port ?= 9999

server:
	python3 server.py --host $(host) --port $(port)
client:
	python3 client.py --host $(host) --port $(port)
clean:
	rm -rf passwords.db users.db __pycache__