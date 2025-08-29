FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/Tuhinshubhra/CMSeeK /opt/cmseek && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/cmseek

# Copy run.sh (no local reports)
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["sh", "/app/run.sh"]