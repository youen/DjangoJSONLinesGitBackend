#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

VENOM_VERSION="$1"
wget -O /usr/bin/venom -nv https://github.com/ovh/venom/releases/download/v${VENOM_VERSION}/venom.linux-amd64
chmod +x  /usr/bin/venom
