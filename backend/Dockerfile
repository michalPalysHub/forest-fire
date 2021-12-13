FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .
