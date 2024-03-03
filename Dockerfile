FROM python:3.9-alpine

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
COPY service_redis.yaml /code
ARG BUILD_VERSION
ENV BUILD=$BUILD_VERSION
RUN echo "BUILD VERSION: $BUILD"
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--timeout", "300"]
