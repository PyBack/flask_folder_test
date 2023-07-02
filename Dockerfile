FROM python:3.8-slim

WORKDIR /app

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

# update submodule
# RUN git submodule update --init --recursive

CMD ["python3",  "src/app.py"]
