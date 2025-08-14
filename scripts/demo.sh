#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://127.0.0.1:5000}"
PLAYER="${PLAYER:-McCurl}"
ANSWER="${ANSWER:-your-answer-here}"
JAR="${JAR:-.cookies.txt}"

PLAYER="${1:-$PLAYER}"
ANSWER="${2:-$ANSWER}"
BASE="${3:-$BASE}"

echo "BASE=$BASE"
echo "PLAYER=$PLAYER"
echo "ANSWER=$ANSWER"
echo "COOKIE_JAR=$JAR"
echo

# Common curl flags (follow redirects is handy for Flask)
CURL_COMMON=(-sS -i -L)
if curl --help all 2>/dev/null | grep -q -- '--fail-with-body'; then
  CURL_COMMON+=("--fail-with-body")
else
  CURL_COMMON+=("-f")
fi

# 0) Start Quest 1: Start
echo "==> Start Quest 1: Start..."
curl "${CURL_COMMON[@]}" -c "$JAR" "$BASE/game/start"
printf "\n"

# 1) Complete Quest 1: Start - send a variable in path
echo "==> Complete Quest 1: Start - send a variable in path..."
curl "${CURL_COMMON[@]}" -c "$JAR" "$BASE/game/start/foobar"
printf "\n"

# 2) Start quest 2: registration
echo "==> Start quest 2: registration..."
curl "${CURL_COMMON[@]}" -c "$JAR" "$BASE/auth/register"
printf "\n"

# 3) Completed quest 2: Register use form and POST
echo "==> Completed quest 2: Register use form and POST..."
curl "${CURL_COMMON[@]}" -c "$JAR" -X POST "$BASE/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=$PLAYER"
echo -e "\n"

# 4) Start Quest 3: Instructions on how to authorize...
echo "==> Start Quest 3: Instructions on how to authorize..."
curl "${CURL_COMMON[@]}" -b "$JAR" "$BASE/game/identify-yourself"
printf "\n"

# 5) Complete Quest 3: an answer to the next quest (form)
echo "==> Complete Quest 3: an answer to the next quest (form)..."
curl "${CURL_COMMON[@]}" -b "$JAR" -X POST "$BASE/game/identify-yourself" \
  -H "Authorization: $PLAYER"
printf "\n"

# 6) Start Quest 4: get to quest now authorization is required.
echo "==> Start Quest 4: get to quest now authorization is required...."
curl "${CURL_COMMON[@]}" -b "$JAR" "$BASE/game/hire-jason" \
  -H "Authorization: $PLAYER"
printf "\n"

# 7) Complete Quest 4: use JSON to hire Jason
echo "==> Complete Quest 4: use JSON to hire Jason..."
curl "${CURL_COMMON[@]}" -b "$JAR" -X POST "$BASE/game/hire-jason" \
  -H "Authorization: $PLAYER" \
  -H "Content-Type: application/json" \
  -d "{\"jason\":\"hire\"}"
printf "\n"

echo "Done."
