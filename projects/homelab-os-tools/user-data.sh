#!/bin/bash
### EC2 macOS user data: fetch project from S3, run test.py, ship log, self terminate.
### Runs as root via ec2-macos-init on amzn-ec2-macos AMIs.

REGION="us-east-2"
BUCKET="python-lib-690712292635-us-east-2-an"
PREFIX="macos-userdata-test"
WORKDIR="/tmp/macos-userdata-test"
LOG="$WORKDIR/result.txt"

mkdir -p "$WORKDIR"
cd "$WORKDIR" || exit 1

### Everything in this block is captured to the log file.
{
  echo "### RUN METADATA ###"
  echo "utc:      $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname: $(hostname)"
  echo "uname:    $(uname -a)"
  echo "macos:    $(sw_vers -productName) $(sw_vers -productVersion) $(sw_vers -buildVersion)"
  echo "arch:     $(uname -m)"
  echo ""

  ### AWS CLI: Amazon macOS AMIs ship it, but do not assume.
  echo "### AWS CLI CHECK ###"
  if command -v aws >/dev/null 2>&1; then
    echo "found: $(command -v aws) -> $(aws --version 2>&1)"
  else
    echo "not found, installing official macOS pkg"
    curl -fsSL "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o /tmp/AWSCLIV2.pkg \
      && installer -pkg /tmp/AWSCLIV2.pkg -target /
    export PATH="/usr/local/bin:$PATH"
    echo "now: $(command -v aws) -> $(aws --version 2>&1)"
  fi
  echo ""

  ### python3: probe real interpreters. Bare /usr/bin/python3 on macOS is a
  ### shim that pops the Xcode CLT installer, so verify it actually executes.
  echo "### PYTHON3 CHECK ###"
  PY=""
  for c in /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
    if [ -x "$c" ] && "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
  done
  if [ -z "$PY" ] && command -v brew >/dev/null 2>&1; then
    echo "no usable python3, installing via Homebrew"
    su - ec2-user -c "brew install python@3.12" >/dev/null 2>&1
    for c in /opt/homebrew/bin/python3 /usr/local/bin/python3; do
      [ -x "$c" ] && PY="$c" && break
    done
  fi
  if [ -z "$PY" ]; then
    echo "FATAL: no usable python3 on this host"
    PY_OK=0
  else
    echo "found: $PY -> $($PY --version 2>&1)"
    PY_OK=1
  fi
  echo ""

  echo "### S3 DOWNLOAD ###"
  aws s3 cp "s3://$BUCKET/$PREFIX/" "$WORKDIR/" \
      --recursive --region "$REGION" --exclude "output/*" 2>&1
  echo "tree:"
  find "$WORKDIR" -type f -not -name result.txt | sed "s|$WORKDIR|.|"
  echo ""

  echo "### TEST EXECUTION ###"
  RC=0
  if [ "$PY_OK" = "1" ]; then
    if "$PY" -m venv "$WORKDIR/.venv" >/dev/null 2>&1; then
      echo "venv created, installing package editable"
      "$WORKDIR/.venv/bin/pip" install -q -e "$WORKDIR" 2>&1
      RUNPY="$WORKDIR/.venv/bin/python"
    else
      echo "venv unavailable, falling back to PYTHONPATH=src"
      export PYTHONPATH="$WORKDIR/src"
      RUNPY="$PY"
    fi
    echo "interpreter: $RUNPY"
    echo ""
    echo "### test.py STDOUT+STDERR ###"
    ### 2>&1 matters: test.py can raise, and tracebacks go to stderr.
    "$RUNPY" "$WORKDIR/test.py" 2>&1
    RC=$?
  else
    RC=127
  fi
  echo ""
  echo "### EXIT CODE: $RC ###"
  echo "note: test.py calls sys.exit(1) by design, so 1 is expected."
} > "$LOG" 2>&1

### Unique key per run so repeats do not clobber, plus a stable latest pointer.
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TOKEN="$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 300")"
IID="$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/instance-id)"

aws s3 cp "$LOG" "s3://$BUCKET/$PREFIX/output/result-$STAMP-$IID.txt" --region "$REGION"
aws s3 cp "$LOG" "s3://$BUCKET/$PREFIX/output/result-latest.txt" --region "$REGION"

### Self terminate: stops the INSTANCE charge. The dedicated host keeps billing
### until released, which Apple licensing blocks for a full 24 hours.
aws ec2 terminate-instances --instance-ids "$IID" --region "$REGION"
