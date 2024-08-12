FROM node:14-alpine

WORKDIR /frontend

COPY package.json /frontend
COPY package-lock.json /frontend

RUN npm install

COPY . /frontend/
