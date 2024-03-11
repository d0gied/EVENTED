#!/bin/sh

celery -A app.app worker --loglevel=info -n database@0