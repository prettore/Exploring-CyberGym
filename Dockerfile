# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.20
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/Cage4/cage-challenge-4"

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/WebGUI_dash/requirements.txt

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser

EXPOSE 8050

CMD ["python", "/app/WebGUI_dash/index.py"]