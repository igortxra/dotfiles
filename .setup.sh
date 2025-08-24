#!/bin/bash

####################################################
### BASIC CONFIGURATIONS AND AUXILIARY FUNCTIONS ###
####################################################

LOGFILE="$HOME/setup.log"
COLOR='\033[0;35m'
RESET='\033[0m'

log_output() {
    "$@" >> "$LOGFILE" 2>&1
}

echo_color() {
    echo -e "${COLOR}$1${RESET}"
}

#######################
### INITIALIZE SUDO ###
#######################

echo_color "Confirming permission..."

sudo -v

( while true; do sudo -n true; sleep 60; done; ) &
SUDO_KEEP_ALIVE_PID=$!

cleanup() {
    kill "$SUDO_KEEP_ALIVE_PID"
    exit
}
trap cleanup EXIT

##########################
### START INSTALLATION ###
##########################

##############
### PACMAN ###
##############

echo_color "\n\nConfiguring Pacman..."
PACMAN_CONF="/etc/pacman.conf"

log_output sudo sed -i 's/^#Color/Color/' "$PACMAN_CONF"
log_output sudo sed -i 's/^#ParallelDownloads/ParallelDownloads/' "$PACMAN_CONF"

log_output sudo pacman-key --init
log_output sudo pacman-key --populate archlinux

echo_color "Pacman Configured!"

###########
### YAY ###
###########

echo_color "\n\nConfiguring YAY (AUR Helper)..."

YAY_DIR="$HOME/yay"
YAY_REPO="https://aur.archlinux.org/yay.git"

if [ ! -d "$YAY_DIR" ]; then
  echo_color "Cloning Yay repository..."
  log_output git clone $YAY_REPO "$YAY_DIR" --quiet
else
  echo_color "Yay dir already present. Skipping cloning."
fi

if [ -d "$YAY_DIR" ]; then
  echo_color "Installing Yay..."
  log_output bash -c "cd $YAY_DIR && makepkg -si --noconfirm --noprogressbar" 
else
  echo_color "Error: Yay dir not created."
fi

echo_color "Syincing Yay database..."
log_output yay -Sy

echo_color "Yay configured!"

################
### DOTFILES ###
################

echo_color "\n\nCloning Dotfiles..."

DOTFILES_URL=https://github.com/$USER/dotfiles.git
DOTFILES_DIR=$HOME/.dotfiles

log_output git clone --bare "$DOTFILES_URL" "$DOTFILES_DIR"
log_output /usr/bin/git --git-dir=$DOTFILES_DIR --work-tree=$HOME config --local status.showUntrackedFiles no
log_output /usr/bin/git --git-dir=$DOTFILES_DIR --work-tree=$HOME checkout -f

echo_color "Dotfiles configured!"

##########################
### INSTALLING PACKAGES ###
##########################

PACKAGE_LIST_FILE="$HOME/docs/PACKAGES.md"
echo_color "\n\nInstalling packages defined in $PACKAGE_LIST_FILE..."

PACKAGE_LIST=$(grep -v '^\s*#' "$PACKAGE_LIST_FILE" | grep -v '^\s*$' | tr '\n' ' ' )
if [ -z "$PACKAGE_LIST" ]; then
  echo_color "No package specified. Skipping."
else
  echo_color "Installing packages: $PACKAGE_LIST"
  log_output yay -S --needed --noconfirm --asexplicit --batchinstall --sudoloop $(echo $PACKAGE_LIST)

  if [ $? -eq 0 ]; then
    echo_color "Packages Installed."
  else
    echo_color "Packages installation failed."
  fi
fi

##############
### NEOVIM ###
##############
echo_color "\n\nConfiguring Neovim ..."

# Check if the directory exists before moving it
if [ -d "$HOME/.config/nvim" ]; then
  echo_color "MOVING CURRENT NEOVIM CONFIGURATION TO: $HOME/.config/nvim_bkp"
  mv "$HOME/.config/nvim" "$HOME/.config/nvim_bkp"
fi

# Clone the repository, even if the directory doesn't exist
echo_color "Cloning neovim config..."
git clone https://github.com/igortxra/nvim "$HOME/.config/nvim"

echo_color "Neovim configured!"

###############
### asdf-vm ###
###############
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.1

################################
### Change Defaut User Shell ###
################################
chsh $USER --shell=/bin/zsh

#################################################
## Configure Screen Locker (Betterlockscreen) ###
#################################################
sudo systemctl enable betterlockscreen@$USER

#####################################
## Configure Wallpaper and colors ###
#####################################
wal -i $HOME/Wallpapers/default.jpg --cols16 -t --saturate 0.7 -o $HOME/.local/bin/utils/colors.sh
