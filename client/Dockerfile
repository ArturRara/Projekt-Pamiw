FROM node:9.6.1 as react-build

ADD . /usr/src/app/
WORKDIR /usr/src/app

COPY package.json /usr/src/app/
RUN npm install --silent

EXPOSE 3000
CMD [ "npm", "run"]