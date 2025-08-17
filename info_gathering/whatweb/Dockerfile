FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y whatweb && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/whatweb

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
