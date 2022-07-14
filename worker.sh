#!/usr/bin/env bash
celery -A configuration worker -Q celery,update_stock,get_items_for_stock_update --loglevel=INFO -E
