FROM python:3.11-slim

# TODO: Move to base
ENV APP_USER=pyapp
ENV APP_GROUP=pyapp
ENV APP_HOME=/home/${APP_USER}
ENV APP_PORT="8080"
ENV GUNICORN_DEFAULT_TIMEOUT=90

ENV PATH=/home/${APP_USER}/.local/bin:$PATH

RUN groupadd --gid 1001 --system  ${APP_GROUP} && \
    useradd --home-dir ${APP_HOME} --create-home --uid 1001 --gid 1001 --shell /bin/bash ${APP_USER} && \
    chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}

USER ${APP_USER}:${APP_GROUP}
WORKDIR ${APP_HOME}
# TODO: End of Move to base

COPY --chown=${APP_USER}:${APP_GROUP} . ${APP_HOME}


RUN pip install -e . && chmod +x /home/pyapp/bin/entrypoint.sh && chmod +x /home/pyapp/bin/consumer-entrypoint.sh

ENTRYPOINT ["/home/pyapp/bin/entrypoint.sh"]




