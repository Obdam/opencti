FROM python:3-alpine

COPY src /opt/opencti-worker

WORKDIR /opt/opencti-worker

RUN apk --no-cache add git build-base libmagic libffi-dev \
    && pip3 install --no-cache-dir --requirement requirements.txt \
    && pip3 install \
    --upgrade \
    --force \
    --no-cache-dir \
    git+https://github.com/Obdam/client-python@fix/custom-auth-header-tweak \
    && apk del git build-base

ENV OPENCTI_URL=https://opencti-web-umubf6op2a-ez.a.run.app

ENV OPENCTI_TOKEN=0f21a7cb-f470-af10-9568-0f73282ecb42

ENV WORKER_LOG_LEVEL=error

ENV OPENCTI_AUTH_FILE_PATH=./auth/google_cloud_serverless.py

ENV OPENCTI_AUTH_CLASS=GCPServerlessAuth

ENTRYPOINT ["python3"]
CMD ["worker.py"]
