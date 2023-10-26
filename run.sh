#!/usr/bin/env bash

function find_python_command() {
    for cmd in python python3; do
        if command -v $cmd &> /dev/null; then
            echo $cmd
            return
        fi
    done
    echo "Python not found. Please install Python."
    exit 1
}

PYTHON_CMD=$(find_python_command)

if $PYTHON_CMD -c "import sys; sys.exit(sys.version_info < (3, 10))"; then
    $PYTHON_CMD scripts/check_requirements.py
    if [ $? -eq 1 ]
    then
        echo
        $PYTHON_CMD -m poetry install --without dev
        echo
        echo "Finished installing packages!"
        echo
    fi
    echo "Starting TextCraft..."
    $PYTHON_CMD -m textcraft
else
    echo "Python 3.10 or higher is required to run TextCraft."
fi
