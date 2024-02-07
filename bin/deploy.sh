#!/bin/bash
set -e
set -o pipefail

# build API
sudo docker compose -f "docker-compose-prod.yml" build api

# starts postgres if it is not running
sudo docker compose -f "docker-compose-prod.yml" up -d postgres

# recreates and starts api and ui
sudo docker compose -f "docker-compose-prod.yml" up -d --force-recreate api
