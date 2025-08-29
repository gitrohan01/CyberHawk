FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y whatweb && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
