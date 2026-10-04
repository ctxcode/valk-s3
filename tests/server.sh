#!/usr/bin/env bash
# Starts or stops the MinIO server the tests run against. The official minio/minio image is no
# longer published, so this uses the community build of the same server.
set -e

NAME=valk-s3-test
PORT=${MINIO_PORT:-9100}
IMAGE=${MINIO_IMAGE:-pgsty/minio:RELEASE.2026-08-04T00-00-00Z}
USER=${MINIO_USER:-valktest}
PASSWORD=${MINIO_PASSWORD:-valktest-secret}

case "${1:-up}" in
    up)
        if [ -n "$(docker ps -aq -f name=^${NAME}$)" ]; then
            docker start ${NAME} >/dev/null
        else
            docker run -d --name ${NAME} -p ${PORT}:9000 \
                -e MINIO_ROOT_USER=${USER} -e MINIO_ROOT_PASSWORD=${PASSWORD} \
                ${IMAGE} server /data >/dev/null
        fi
        for i in $(seq 1 60); do
            if curl -fs "http://127.0.0.1:${PORT}/minio/health/live" >/dev/null; then
                echo "minio listening on 127.0.0.1:${PORT}"
                exit 0
            fi
            sleep 0.5
        done
        echo "minio did not start" >&2
        docker logs ${NAME} >&2
        exit 1
        ;;
    down)
        docker rm -f ${NAME} >/dev/null 2>&1 || true
        echo "removed the test server"
        ;;
    *)
        echo "usage: $0 [up|down]" >&2
        exit 1
        ;;
esac
