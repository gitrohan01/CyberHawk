FROM alpine:latest

RUN apk --no-cache add iputils

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/ping

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]

