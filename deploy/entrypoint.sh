#!/bin/sh

uvicorn app.main.main:make_app --factory --host 0.0.0.0 --port 8000