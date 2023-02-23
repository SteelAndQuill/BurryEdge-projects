FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libssl-dev graphviz parallel

COPY . /burryedge

WORKDIR /burryedge

RUN pip install --upgrade pip

RUN pip install --no-cache -r requirements.txt

WORKDIR /burryedge/members-edge

CMD ["python3", "main.py"]
