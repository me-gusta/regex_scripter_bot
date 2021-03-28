FROM python:3.9.1-slim


COPY ./req.txt /req.txt


RUN apt-get update
RUN apt-get install gcc libc-dev -y

RUN pip install -r req.txt

RUN apt-get remove gcc libc-dev -y
RUN apt-get clean autoclean
RUN apt-get autoremove --yes


RUN mkdir /regex_scripter
COPY ./regex_scripter /regex_scripter
WORKDIR /regex_scripter

CMD python3 app.py