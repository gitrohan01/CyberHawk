FROM projectdiscovery/httpx:latest

WORKDIR /app
RUN mkdir -p /app/reports/info_gathering/httpx

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]
