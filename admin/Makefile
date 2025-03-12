# Variables
IMAGE_NAME = serverless-rag-admin
CONTAINER_PORT = 8083

include .env
export

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
# Note: AWS credentials should be passed from environment variables
run:
	docker run \
		-e BUCKET_NAME=$(BUCKET_NAME) \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-p $(CONTAINER_PORT):$(CONTAINER_PORT) \
		-it $(IMAGE_NAME)

# Build and run
all: build run

# Clean up containers and images
clean:
	docker stop $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME)) 2>/dev/null || true
	docker rm $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME)) 2>/dev/null || true
	docker rmi $(IMAGE_NAME) 2>/dev/null || true

.PHONY: build run all clean
