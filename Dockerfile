FROM python:latest

RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y python3
RUN apt-get install -y sqlite3
RUN apt-get install -y git

RUN git clone https://github.com/yuyu29/appsec_report4_code
WORKDIR /appsec_report4_code

RUN pip3 install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 8080

CMD python3 -m flask run --port 8080

