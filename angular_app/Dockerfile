FROM node:current-bullseye

COPY . /code/angular_app

WORKDIR /code/angular_app

RUN npm install && npm install -g @angular/cli

EXPOSE 4200

ENTRYPOINT ["ng", "serve", "--host", "0.0.0.0"]