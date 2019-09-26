#!/usr/bin/env sh

# adapted from https://github.com/locustio/locust/blob/246ec42e59fe38f0d27b8ea752209d838e27b898/docker_start.sh

if [ -z "${TARGET_URL}" ]; then
  echo "ERROR: TARGET_URL is not configured" >&2
  exit 1
fi

LOCUST_MODE="${LOCUST_MODE:=standalone}"
LOCUST_OPTS="-f ./stress_test.py -H ${TARGET_URL}"

if [ "${LOCUST_MODE}" = "leader"]; then
  LOCUST_OPTS="${LOCUST_OPTS} --master"
elif [ "${LOCUST_MODE}" = "follower" ]; then
  if [ -z "$LOCUST_LEADER_HOST" ]; then
    echo "ERROR: LOCUST_LEADER_HOST is not configured. A follower node requires a leader node." >&2
    exit 1
  fi

  LOCUST_OPTS="${LOCUST_OPTS} --slave --master-host=${LOCUST_LEADER_HOST} --master-port=${LOCUST_LEADER_PORT:-5557}"
fi

echo "starting Locust"
echo "$ locust ${LOCUST_OPTS}"

locust ${LOCUST_OPTS}
