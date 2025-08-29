FROM alpine:latest

RUN apk --no-cache add bind-tools

WORKDIR /app


COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
