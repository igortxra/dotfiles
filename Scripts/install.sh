echo "########## Remapping caps to super ##########"
setxkbmap -option caps:super

echo "########## Installing YAY... ##########"
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si && cd .. && rm -rf yay
yay -Sy

echo "########## Configuring Shell (zsh) ##########"
yay -S zsh exa procs fzf  --noconfirm --quiet --needed
# Zsh as default shell
chsh -s /bin/zsh $(whoami)
# Powerlevel10k
yay -S --noconfirm --quiet --needed zsh-theme-powerlevel10k-git
# Autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions 

echo "########## Configuring Display Manager (Ly) ##########"
yay -S Ly --noconfirm --quiet --needed 
sudo systemctl enable ly.service

echo "########## Configuring Terminal Emulator (Kitty) ##########"
yay -S kitty

echo "########## Configuring Window Manager (Qtile) ##########"
yay -S --noconfirm --quiet --needed python-pip 
pip install xcffib==1.4 --break-system-packages
pip install cairocffi==1.6 --break-system-packages
yay -S --noconfirm --quiet --needed python-setuptools-git-versioning
yay -S --noconfirm --quiet --needed qtile-git 
yay -S --noconfirm --quiet --needed qtile-extras-git 

yay -S --noconfirm --quiet --needed xorg-xrandr 
yay -S --noconfirm --quiet --needed wireless_tools 
yay -S --noconfirm --quiet --needed alsa-utils
yay -S --noconfirm --quiet --needed flameshot 
yay -S --noconfirm --quiet --needed python-iwlib 
yay -S --noconfirm --quiet --needed python-psutil 
yay -S --noconfirm --quiet --needed python-dbus-next 
yay -S --noconfirm --quiet --needed python-requests 

echo "########## Configuring App Launcher (Rofi) ##########"
yay -S --noconfirm --quiet --needed rofi
git clone --depth=1 https://github.com/adi1090x/rofi.git
cd rofi && chmod +x setup.sh && source ./setup.sh && cd ..
rm -rf ./rofi

echo "########## Configuring Notification Daemon (Dunst) ##########"
yay -S --noconfirm --quiet --needed dunst

echo "########## Configuring Browser (Qutebrowser) ##########"
yay -S --quiet --needed --noconfirm qutebrowser 
git clone https://github.com/catppuccin/qutebrowser.git ~/.config/qutebrowser/catppuccin

echo "########## Install Picom Jonaburg ##########"
yay -S --quiet --needed --noconfirm meson uthash python-setuptools
git clone https://github.com/jonaburg/picom
cd picom && meson --buildtype=release . build && ninja -C build && sudo ninja -C build install && cd ..
rm -rf ./picom ./build

echo "########## Install File Manager (Thunar) ##########"
yay -S --quiet --needed --noconfirm thunar

echo "########## Install Screen Utils (arandr and autorandr) ##########"
yay -S --quiet --needed --noconfirm arandr autorandr

echo "########## Install Clipboard Utils (copyq and xclip) ##########"
yay -S --quiet --needed --noconfirm copyq
yay -S --quiet --needed --noconfirm xclip

echo "########## Install Nerd Fonts (Iosevka Nerd) ##########"
yay -S --quiet --needed --noconfirm ttf-iosevka-nerd

echo "########## Inetutils ##########"
yay -S --noconfirm --quiet --needed inetutils-git

echo "########## Make use of dotfiles ##########"
echo ".dotfiles" >> .gitignore
git clone --bare https://github.com/$USER/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
dotfiles checkout

echo "########## Configuring Wallpaper (Nitrogen) ##########"
yay -S --noconfirm --quiet --needed nitrogen
nitrogen --set-auto ~/Wallpapers/default.png

echo "########## Creating user dirs ############"
yay -S --quiet --needed --noconfirm xdg-user-dirs
xdg-user-dirs-update --force

echo "########## Installing themes (Dracula and Catppuccin) ##########"
yay -S --quiet --needed --noconfirm lxappearance
yay -S --quiet --needed --noconfirm dracula-cursos-git
yay -S --quiet --needed --noconfirm dracula-icons-git
yay -S --quiet --needed --noconfirm catppuccin-gtk-theme-mocha

# Opcionais

echo "########## Install Developer Tools ##########"
yay -S --quiet --needed --noconfirm asdf-vm
yay -S --quiet --needed --noconfirm postman-bin

echo "########## Installing AstroNvim ##########"
yay -S --quiet --needed --noconfirm neovim npm fzf
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim

echo "########## Installing Spotify ##########"
yay -S --quiet --needed --noconfirm spotify

echo "########## Installing Notes (Obsidian) ##########"
yay -S --quiet --needed --noconfirm obsidian

