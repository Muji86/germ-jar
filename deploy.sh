#!/bin/sh
# Copies Germ Jar to a home server running serve.py. The target comes from .deploy.env:
#   HOST=user@server   URL=https://server:5008
set -e
cd "$(dirname "$0")"
[ -f .deploy.env ] || { echo "Make .deploy.env with HOST= and URL= first"; exit 1; }
. ./.deploy.env
rsync -av serve.py README.md "$HOST":~/germ-jar/
rsync -av index.html "$HOST":~/germ-jar/public/
echo "Deployed: $URL"
