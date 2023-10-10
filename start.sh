#!/bin/bash
source .env
uvicorn api:app --host 0.0.0.0 --port 8000