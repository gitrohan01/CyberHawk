FROM alpine:latest

# Install whois package
RUN apk --no-cache add whois

WORKDIR /app


COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
