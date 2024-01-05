ARG FUNCTION_DIR="/function"

FROM python:3.10-alpine

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev libressl-dev cargo g++ elfutils-dev autoconf automake libtool make cmake \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install awslambdaric \
    && apk del .build-deps

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

# Pass the name of the function handler as an argument to the runtime
# CMD python main.py
CMD [ "lambda_function.handler" ]
