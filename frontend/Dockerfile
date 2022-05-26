FROM node:16-alpine

RUN mkdir -p /opt/app
ENV APP_DIR /opt/app
WORKDIR $APP_DIR

COPY package.json .
RUN npm install

COPY src $APP_DIR/src
COPY public $APP_DIR/public

CMD ["npm", "run", "start"]
