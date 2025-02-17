# https://github.com/mongo-express/mongo-express-docker/blob/403467f350d819b404f3d5150be7776217e810b7/1.0/20-alpine3.19/Dockerfile

ARG BASE_IMAGE_TAG=1.0.2-20-alpine3.19

FROM mongo-express:${BASE_IMAGE_TAG} AS mongoexpress

ARG IMAGE_USER_NAME=node
ARG IMAGE_USER_ID=1000
ARG IMAGE_GROUP_NAME=node
ARG IMAGE_GROUP_ID=1000

# for healthcheck triggering
RUN apk update && apk add --no-cache curl

# create user and group
#  && echo ${USER_NAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_NAME} \
#  && chmod 0440 /etc/sudoers.d/${USER_NAME}

USER node

EXPOSE 8081

ENTRYPOINT [ "/sbin/tini", "--", "/docker-entrypoint.sh"]
CMD ["mongo-express"]
