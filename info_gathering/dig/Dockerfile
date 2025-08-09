FROM alpine:latest

RUN apk --no-cache add bind-tools

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/dig

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
