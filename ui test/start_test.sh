#!/bin/bash

# Проверка на Windows или Linux/Mac
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows OS"

    # Проверка и установка Python
    if ! command -v python &> /dev/null; then
        echo "Python is not installed. Please install Python manually."
        exit 1
    fi

    # Создание виртуального окружения
    python -m venv venv

    # Активация виртуального окружения
    source venv/Scripts/activate

    # Установка pytest
    pip install -r requirements.txt

    # Запуск pytest
    pytest e2e.py
else
    echo "Detected Linux/Mac OS"

    # Проверка и установка Python
    if ! command -v python3 &> /dev/null; then
        echo "Python3 is not installed. Please install Python3."
        exit 1
    fi

    # Создание виртуального окружения
    python3 -m venv venv

    # Активация виртуального окружения
    source venv/bin/activate

    # Установка pytest
	pip install -r requirements.txt

    # Запуск pytest
    pytest e2e.py
fi

exec $SHELL