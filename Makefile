ifndef service
$(error "service" is not set)
endif
build-service:
	docker build -t "evented-$(service)" . -f ./docker/service.Dockerfile --build-arg SERVICE_NAME=$(service)