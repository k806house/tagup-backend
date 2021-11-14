#!/bin/bash

set -e

git lfs fetch --all
git lfs pull
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d --remove-orphans
