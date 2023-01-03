ARG DEBIAN_VERSION=bullseye
ARG PYTHON_VERSION=3
ARG DOCKER_VERSION=20

FROM docker:${DOCKER_VERSION} AS docker
FROM python:${PYTHON_VERSION} AS python

####################################################################################
## python-devcontainer-ci stage                                                   ##
##   contains minimal setup to run on a CI platform                               ##
####################################################################################

FROM python:${PYTHON_VERSION}-${DEBIAN_VERSION} AS python-devcontainer-ci

# Required packages for CI
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget curl \
    bash zsh \
    git \
    sqlite3 \
    && rm -r /var/lib/apt/lists /var/cache/apt/archives

COPY scripts/* /usr/local/bin/

RUN    groupadd -g 1000 -r vscode \
    && useradd -r -u 1000 -g vscode -s /bin/zsh vscode \
    && cp -r /root/. /home/vscode \
    && chown -R vscode:vscode /home/vscode \
    && install-venom.sh 1.0.1 \
    && install-neon.sh  1.5.5

USER vscode

####################################################################################
## python-devcontainer stage                                                      ##
##   contains a slim setup for development usage                                  ##
####################################################################################

FROM python-devcontainer-ci AS python-devcontainer

USER root

# Timezones
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    locales tzdata \
    sudo \
    figlet \
    jq \
    && rm -r /var/lib/apt/lists /var/cache/apt/archives \
    # Generate default locale
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    # Promote user as sudoer
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Docker CLI and docker-compose
COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker
RUN wget -O /usr/local/bin/docker-compose -nv https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 && \
    chmod +x /usr/local/bin/docker-compose

USER vscode

# Default values, override with a dotfile repository (https://code.visualstudio.com/docs/remote/containers#_personalizing-with-dotfile-repositories)
ENV TZ= \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    TERM=xterm

# Zsh Theme
RUN wget -O- -nv https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k && \
    rm -rf ~/.oh-my-zsh/custom/themes/powerlevel10k/.git* && \
    mkdir -p ~/.cache/gitstatus && \
    wget -O- -nv https://github.com/romkatv/gitstatus/releases/download/v1.3.1/gitstatusd-linux-x86_64.tar.gz | tar -xz -C ~/.cache/gitstatus gitstatusd-linux-x86_64

# Zsh Theme configuration
COPY .zshrc /home/vscode/.zshrc
COPY .p10k.zsh /home/vscode/.p10k.zsh

COPY welcome.sh /home/vscode/welcome.sh

ENTRYPOINT [ "/bin/zsh" ]
