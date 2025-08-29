FROM node:20-slim

RUN npm install -g retire

WORKDIR /app


COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
