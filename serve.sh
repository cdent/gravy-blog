#!/usr/bin/env bash

TMP_DIR=tmp

if [ ! -d "$TMP_DIR" ] ; then
    echo "Missing data directory: $TMP_DIR .. creating now";
    mkdir $TMP_DIR
fi

export DJANGO_SETTINGS_MODULE='settings'
CMD=old_dev_appserver.py

$CMD \
    --skip_sdk_update_check \
    --datastore_path=tmp/data \
    --blobstore_path=tmp/blobstore \
    --smtp_port=1025 \
    --smtp_host=localhost \
    --require_indexes \
    $@ \
    .
