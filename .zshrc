# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

source ~/.oh-my-zsh/custom/themes/powerlevel10k/powerlevel10k.zsh-theme

export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
export LANGUAGE='en_US:en'
export TERM=xterm
export ZSH="${HOME}/.oh-my-zsh"

export PATH=$PATH:/home/vscode/.local/bin

# Fix some problems with key bindings
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[3~' delete-char

# Use docker and docker-compose without sudo
alias docker="sudo docker"
alias docker-compose="sudo docker-compose"

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# welcome message is computed every 12 hours
bash ~/welcome.sh
