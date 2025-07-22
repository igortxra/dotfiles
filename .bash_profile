#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

# Load aliases
if [[ -f ~/.aliases ]]; then
  . ~/.aliases
fi

# Load X11
if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" = 1 ]; then
  exec startx
fi
