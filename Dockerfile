FROM alpine:3.18

RUN apk add py3-pip

RUN pip3 install --upgrade pip
RUN pip3 install discord


COPY app app
WORKDIR app

CMD ["python3", "main.py"]