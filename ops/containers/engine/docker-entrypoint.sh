#!/bin/bash

if [ "$1" == "encrypt" ]; then
    shift;
    echo "Encrpting file: $1"
    echo "$2" > /tmp/secret.txt
    ansible-vault encrypt "$1" --vault-password-file /tmp/secret.txt
    rm /tmp/secret.txt
else
    python src/engine.py "$@"
fi