FROM node:20.11.1

WORKDIR /app

RUN npm install -g dynamodb-admin

CMD ["dynamodb-admin"]