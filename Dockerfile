FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY . /app
RUN pip install -r /app/requirements
RUN apt-get update
RUN apt-get install -y sqlite3 libsqlite3-dev
