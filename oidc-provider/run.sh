#!/bin/bash

virtualenv .
. bin/activate
pip install -r simple_op/requirements.txt
cd simple_op && python src/run.py --base https://localhost:8443 -p 8443 -d settings.yaml

# This is how you would register a client. Uses the httpie package.
#C=$(http --verify=no POST https://localhost:8443/registration redirect_uris:='["https://localhost:8080/oauth2callback"]')

