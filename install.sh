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
#git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions 

echo "########## Configuring Display Manager (Ly) ##########"
yay -S Ly --noconfirm --quiet --needed 
sudo systemctl enable ly.service

echo "########## Configuring Window Manager (Qtile) ##########"
yay -S --noconfirm --quiet --needed xorg-xrandr wireless_tools alsa-utils flameshot python-pip python-iwlib python-psutil python-dbus-next python-requests python-xcffib python-cairocffi qtile-git qtile-extras-git 

echo "########## Configuring App Launcher (Rofi) ##########"
yay -S --noconfirm --quiet --needed rofi
git clone --depth=1 https://github.com/adi1090x/rofi.git
cd rofi && chmod +x setup.sh && source ./setup.sh && cd
rm -rf rofi

echo "########## Configuring Notification Daemon (Dunst) ##########"
yay -S --noconfirm --quiet --needed dunst

echo "########## Configuring Wallpaper (Nitrogen) ##########"
yay -S --noconfirm --quiet --needed nitrogen
nitrogen --set-auto ~/wallpapers/default.png

echo "########## Configuring Browser (Qutebrowser) ##########"
yay -S --quiet --needed --noconfirm qutebrowser 
git clone https://github.com/catppuccin/qutebrowser.git ~/.config/qutebrowser/catppuccin

echo "########## Installing AstroNvim ##########"
yay -S --quiet --needed --noconfirm neovim npm fzf
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim

echo "########## Installing Spotify ##########"
yay -S --quiet --needed --noconfirm spotify

echo "########## Install Picom Jonaburg ##########"
yay -S --quiet --needed --noconfirm meson uthash python-setuptools
git clone https://github.com/jonaburg/picom
cd picom && meson --buildtype=release . build && ninja -C build && sudo ninja -C build install && cd
rm -rf picom

echo "########## Install Thunar ##########"
yay -S --quiet --needed --noconfig thunar

echo "########## Install arandr and autorandr ##########"
echo "########## Install arandr and autorandr ##########"
yay -S arandr autorandr

echo "########## Install Developer Tools ##########"
yay -S --quiet --needed --noconfig asdf-vm
yay -S postman-bin

echo "########## Install Notes (Obsidian) ##########"
yay -S obsidian

echo "########## Install Clipboard Util (copyq) ##########"
yay -S copq

# yay -S inetutils-git
# yay -S ttf-jetbrains-mono
