# Check if the container exists and remove it if it does
if [ $(docker ps -a -q -f name=inference_api) ]; then
    docker rm -f inference_api
fi

# Build the Docker image
docker build . -t aqapi

# Run the Docker container
docker run --network airquality_default --env-file local.env --name inference_api -p 8000:8000 aqapi
