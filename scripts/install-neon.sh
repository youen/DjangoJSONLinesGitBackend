#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

NEON_VERSION="$1"
wget -O /usr/bin/neon -nv https://github.com/c4s4/neon/releases/download/${NEON_VERSION}/neon-linux-amd64
chmod +x  /usr/bin/neon
