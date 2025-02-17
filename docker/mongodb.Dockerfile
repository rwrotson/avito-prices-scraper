ARG BASE_IMAGE_TAG=7.0.3-ubi9

FROM mongodb/mongodb-community-server:${BASE_IMAGE_TAG} AS runner

USER root

# copy healthcheck script
COPY --chown=mongod:mongod docker/_check-mongo /check-mongo
RUN chmod +x /check-mongo

# copy initialization script
COPY --chown=mongod:mongod docker/_init-mongo /docker-entrypoint-initdb.d/init-mongo.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-mongo.sh

USER mongod

ENTRYPOINT ["python3", "/usr/local/bin/docker-entrypoint.py"]
CMD ["mongod"]
