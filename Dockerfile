
# FROM jupyter/datascience-notebook:x86_64-ubuntu-22.04
FROM python:3.11
EXPOSE 8888
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]


# https://github.com/svolodarskyi/docker_turtorial
# https://medium.com/@18bhavyasharma/setting-up-and-running-jupyter-notebook-in-a-docker-container-d2acd713ce66
# docker-compose up -d 