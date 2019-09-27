#!/usr/bin/env sh

# adapted from https://github.com/locustio/locust/blob/246ec42e59fe38f0d27b8ea752209d838e27b898/docker_start.sh

if [ -z "${TARGET_URL}" ]; then
  echo "ERROR: TARGET_URL is not configured" >&2
  exit 1
fi

LOCUST_OPTS="-f ./stress_test.py -H ${TARGET_URL} --master"

echo "starting Locust"
echo "$ locust ${LOCUST_OPTS}"

locust ${LOCUST_OPTS}
