git clone https://github.com/vllm-project/vllm.git

cd vllm

docker build -f docker/Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
