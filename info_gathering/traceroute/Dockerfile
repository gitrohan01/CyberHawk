FROM alpine:latest
RUN apk add --no-cache busybox-extras
COPY run.sh /run.sh
RUN chmod +x /run.sh
ENTRYPOINT ["/run.sh"]
