# Variables
IMAGE_NAME = serverless-rag-client
CONTAINER_PORT = 8084

include .env
export

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run \
		-e BUCKET_NAME=$(BUCKET_NAME) \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-p $(CONTAINER_PORT):$(CONTAINER_PORT) \
		-it $(IMAGE_NAME)