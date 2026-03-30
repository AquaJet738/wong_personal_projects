#!/bin/bash

# Update package list and install dependencies
apt-get update
apt-get install -y libxml2-dev libxslt-dev

# Proceed with the regular pip install
pip install -r requirements.txt

