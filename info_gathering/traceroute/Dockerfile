FROM alpine:latest

RUN apk --no-cache add traceroute

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/traceroute

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]

