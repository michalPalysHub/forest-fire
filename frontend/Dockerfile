FROM node:16

RUN mkdir /frontend
WORKDIR /frontend

COPY package.json .
RUN npm install

COPY . .
