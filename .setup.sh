#!/bin/bash

####################################################
### BASIC CONFIGURATIONS AND AUXILIARY FUNCTIONS ###
####################################################

LOGFILE="$HOME/setup.log"
COLOR='\033[0;35m'
RESET='\033[0m'

log_output() {
    "$@" 2>&1 | tee -a "$LOGFILE"
}

echo_color() {
    echo -e "${COLOR}$1${RESET}"
}

##########################
### START INSTALLATION ###
##########################

##############
### PACMAN ###
##############

echo_color "\n\nCONFIGURING PACMAN (Package Manager)..."
# Pacman configuration file path
PACMAN_CONF="/etc/pacman.conf"

# Enable pacman colorized output
log_output sudo sed -i 's/^#Color/Color/' "$PACMAN_CONF"

# Activate parallel downloads (5 specifically)
log_output sudo sed -i 's/^#ParallelDownloads/ParallelDownloads/' "$PACMAN_CONF"

# NOTE: You must run `pacman-key --init` before first using pacman; the local
# keyring can then be populated with the keys of all official Arch Linux
# packagers with `pacman-key --populate archlinux`.
log_output sudo pacman-key --init
log_output sudo pacman-key --populate archlinux

echo_color "PACMAN CONFIGURED!"

###########
### YAY ###
###########

echo_color "\n\nCONFIGURING YAY (AUR Helper)..."

YAY_DIR="$HOME/yay"
YAY_REPO="https://aur.archlinux.org/yay.git"

# Check if the yay directory exists
if [ ! -d "$YAY_DIR" ]; then
  echo_color "Yay folder does not exist. Cloning Yay repository..."

  # Clone the Yay repository as the specified user
  log_output git clone $YAY_REPO "$YAY_DIR" --quiet
else
  echo_color "Yay folder already exists. Skipping clone."
fi

# Install Yay if the folder exists
if [ -d "$YAY_DIR" ]; then
  echo_color "Installing Yay..."
  log_output bash -c "cd $YAY_DIR && makepkg -si --noconfirm --noprogressbar" 
else
  echo_color "Error: Yay folder was not created successfully."
fi

echo_color "Sync Yay database..."
log_output yay -Sy

echo_color "YAY CONFIGURED!"


################
### DOTFILES ###
################

echo_color "\n\nPULLING DOTFILES..."

DOTFILES_URL=https://github.com/$USER/dotfiles.git
DOTFILES_DIR=$HOME/.dotfiles

# Clone dotfiles as bare repository
log_output git clone --bare "$DOTFILES_URL" "$DOTFILES_DIR"

# Configure dotfiles to not show untracked files in `git status` command
log_output /usr/bin/git --git-dir=$DOTFILES_DIR --work-tree=$HOME config --local status.showUntrackedFiles no

# Apply dotfiles
log_output /usr/bin/git --git-dir=$DOTFILES_DIR --work-tree=$HOME checkout -f

echo_color "DOTFILES CONFIGURED!"

##########################
### Installig Packages ###
##########################

echo_color "\n\nINSTALLING PACKAGES DEFINED IN $PACKAGE_LIST_FILE..."

PACKAGE_LIST_FILE="$HOME/PACKAGES.md"

# Read and filter the packages from the file, ignoring comments and empty lines
PACKAGE_LIST=$(grep -v '^\s*#' "$PACKAGE_LIST_FILE" | grep -v '^\s*$' | tr '\n' ' ' )

# Check if any packages are left to install
if [ -z "$PACKAGE_LIST" ]; then
  echo_color "NO PACKAGES SPECIFIED. SKIPPING"
else
  # Install packages using yay
  echo_color "INSTALLING PACKAGES: $PACKAGE_LIST"

  # Run yay as the specified user
  log_output yay -S --needed --noconfirm --asexplicit --batchinstall --sudoloop $(echo $PACKAGE_LIST)

  # Check if the installation was successful
  if [ $? -eq 0 ]; then
    echo_color "PACKAGES INSTALLED SUCCESSFULLY."
  else
    echo_color "PACKAGE INSTALLATION FAILED."
  fi
fi


##############
### NEOVIM ###
##############
echo_color "\n\nCONFIGURING NEOVIM..."

# Check if the directory exists before moving it
if [ -d "$HOME/.config/nvim" ]; then
  echo_color "MOVING CURRENT NEOVIM CONFIGURATION TO: $HOME/.config/nvim_bkp"
  mv "$HOME/.config/nvim" "$HOME/.config/nvim_bkp"
fi

# Clone the repository, even if the directory doesn't exist
echo_color "CLONING NEOVIM CONFIG FROM IGORTXRA..."
git clone https://github.com/igortxra/nvim "$HOME/.config/nvim"

echo_color "NEOVIM CONFIGURED!"

###############
### asdf-vm ###
###############
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.1

################################
### Change Defaut User Shell ###
################################

chsh igortxra --shell=/bin/zsh

#################################################
## Configure Screen Locker (Betterlockscreen) ###
#################################################
sudo systemctl enable betterlockscreen@$USER
