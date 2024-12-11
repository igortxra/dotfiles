# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Plugin manager: Zinit
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"

# Load powerlevel10k theme
zinit ice depth"1" # git clone depth
zinit light romkatv/powerlevel10k

# The Big Three!!!
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions

# Git Aliases
zinit snippet https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/refs/heads/master/plugins/git/git.plugin.zsh

zinit light Aloxaf/fzf-tab

# History
HISTFILE=~/.histfile
HISTSIZE=5000
SAVEHIST=5000
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_ignore_dups
setopt hist_save_no_dups
setopt hist_find_no_dups


setopt autocd extendedglob
unsetopt beep

# Keybindings
bindkey -v
bindkey '^R' history-incremental-search-backward
bindkey '^k' history-search-backward
bindkey '^j' history-search-forward

bindkey '^f' autosuggest-accept

# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '$HOME/.zshrc'
zstyle ":completion:*" matcher-list 'm:{a-z}={A-Za-z}'
zstyle ":completion:*" list-colors "${(s.:.)LS_COLORS}"
zstyle ":completion:*" menu no
zstyle ":fzf-tab:complete:cd:*" fzf-preview 'ls --color $realpath'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# Load aliases
source $HOME/.aliases

# LOAD ASDF
. "$HOME/.asdf/asdf.sh"

# Shell Integrations
eval "$(fzf --zsh)"
eval "$(zoxide init zsh)"

# Path additions
path+=("$HOME/.local/bin")

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# Make prompt displays at bottom
precmd() {
  local rows
  rows=999
  print -Pn "\e[${rows}H"
}

PROMPT='%n@%m %~ %#\n'
