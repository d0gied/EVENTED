#!/bin/sh

celery -A parser.app worker --loglevel=info -n parser@0 -E