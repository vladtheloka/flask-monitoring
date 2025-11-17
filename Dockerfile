# syntax=docker/dockerfile:1.5
FROM python:3.12-slim

# Используем BuildKit cache для pip
ARG PIP_CACHE_DIR=/root/.cache/pip
ENV PIP_CACHE_DIR=${PIP_CACHE_DIR}

WORKDIR /restmon

# Устанавливаем системные зависимости
RUN apt add --update python py-pip gcc linux-headers make musl-dev python-dev

# Копируем только requirements для кэширования зависимостей
COPY requirements.txt /src/requirements.txt

# Устанавливаем зависимости с использованием кэша
RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    --cache-dir $PIP_CACHE_DIR

# Копируем остальной код
COPY restmon/ /src
COPY restmon /src/restmon

# Запускаем приложение
CMD python /src/api.py