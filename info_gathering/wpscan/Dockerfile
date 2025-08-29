FROM ruby:3.2-slim

RUN apt-get update && apt-get install -y git curl libcurl4-openssl-dev make gcc \
    && gem install wpscan \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
