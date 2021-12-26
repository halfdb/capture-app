start:
	docker-compose up -d
	python ui.py

lib:
	$(MAKE) -C ocrlib
