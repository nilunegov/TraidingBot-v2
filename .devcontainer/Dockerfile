FROM python:3.12.11-bullseye

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    git \
    curl \
    sudo \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя vscode
RUN useradd -m -s /bin/bash vscode && \
    echo 'vscode ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

# Переключение на обычного пользователя
USER vscode

EXPOSE 5000
CMD [ "bash" ]
