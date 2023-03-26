FROM python:3.8

WORKDIR /app

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["python3",  "src/app.py"]
