#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

figlet -c Python Devcontainer

(
  source /etc/os-release
  printf "%-16s %13s " "${NAME}" "${VERSION}"
  echo "✅"
)

DOCKER_CLI_VERSION=$(docker version -f '{{.Client.Version}}' 2>/dev/null || :)
printf "├─ %-16s %10s " "Docker Client" "${DOCKER_CLI_VERSION}"
echo "✅"

DOCKER_COMPOSE_VERSION=$(sudo docker-compose --version 2>/dev/null | cut -d' ' -f4 | tr -d ',v' || :)
printf "├─ %-16s %10s " "Docker Compose" "${DOCKER_COMPOSE_VERSION}"
echo "✅"

GIT_VERSION=$(git --version | cut -d' ' -f3 || :)
printf "├─ %-16s %10s " "Git Client" "${GIT_VERSION}"
echo "✅"

ZSH_VERSION=$(zsh --version | cut -d' ' -f2 || :)
printf "├─ %-16s %10s " "Zsh" "${ZSH_VERSION}"
echo "✅"

PYTHON_VERSION=$(python --version | cut -d' ' -f2 || :)
printf "├─ %-16s %10s " "Python" "${PYTHON_VERSION}"
echo "✅"

NEON_VERSION=$(neon --version 2>/dev/null || echo -n "n/a")
printf "├─ %-16s %10s " "Neon" "${NEON_VERSION}"
echo "✅"

VENOM_VERSION=$(venom version 2>/dev/null | cut -d' ' -f3 | sed -e 's/^v//' || echo -n "n/a")
printf "├─ %-16s %10s " "Venom" "${VENOM_VERSION}"
echo "✅"

echo
