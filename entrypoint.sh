#!/bin/bash

# entrypoint.sh - Start the FastAPI server for OmniParse
# Port: 8000

set -e

echo "=========================================="
echo "OmniParse Server Starting..."
echo "=========================================="

# Set default values if not provided
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8000"}
DOCUMENTS=${DOCUMENTS:-"true"}
MEDIA=${MEDIA:-"false"}
WEB=${WEB:-"false"}
RELOAD=${RELOAD:-"false"}

echo "Configuration:"
echo "  Host: ${HOST}"
echo "  Port: ${PORT}"
echo "  Documents: ${DOCUMENTS}"
echo "  Media: ${MEDIA}"
echo "  Web: ${WEB}"
echo "  Reload: ${RELOAD}"
echo "=========================================="

# Parse boolean flags for the server
DOCS_FLAG=""
MEDIA_FLAG=""
WEB_FLAG=""
RELOAD_FLAG=""

if [ "${DOCUMENTS}" = "true" ]; then
    DOCS_FLAG="--documents"
fi

if [ "${MEDIA}" = "true" ]; then
    MEDIA_FLAG="--media"
fi

if [ "${WEB}" = "true" ]; then
    WEB_FLAG="--web"
fi

if [ "${RELOAD}" = "true" ]; then
    RELOAD_FLAG="--reload"
fi

# Start the FastAPI server
echo "Starting server on ${HOST}:${PORT}..."
exec python3 server.py --host "${HOST}" --port "${PORT}" ${DOCS_FLAG} ${MEDIA_FLAG} ${WEB_FLAG} ${RELOAD_FLAG}
