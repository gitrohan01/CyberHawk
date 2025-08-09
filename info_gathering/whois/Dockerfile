FROM alpine:latest

# Install whois package
RUN apk --no-cache add whois

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/whois

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
