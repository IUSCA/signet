#!/bin/bash
set -e
set -o pipefail

sudo docker compose -f "docker-compose-prod.yml" build api
sudo docker compose -f "docker-compose-prod.yml" up -d