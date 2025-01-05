#!/bin/bash

sudo rm -r "scitus"

git clone https://github.com/scitus-bot/scitus.git

cp .env scitus/.env

python3 scitus/py/main.py