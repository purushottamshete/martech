FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /martech
RUN mkdir logs
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
COPY . ./
EXPOSE 8000