echo "#######################################"
echo "########## Installing YAY... ##########"
echo "#######################################"
rm -rf yay
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si && cd .. && rm -rf yay
yay -Sy

echo "#############################################"
echo "########## Configuring Shell (zsh) ##########"
echo "#############################################"
yay -S zsh exa procs fzf --noconfirm --quiet --needed

# Powerlevel10k
yay -S --noconfirm --quiet --needed zsh-theme-powerlevel10k-git

# Autosuggestions
rm -rf ~/.zsh/zsh-autosuggestions 
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions 

echo "###########################################################"
echo "########## Configuring Terminal Emulator (Kitty) ##########"
echo "###########################################################"
yay -S kitty --noconfirm --quiet --needed

echo "###########################################################"
echo "########## Configuring Window Manager (Qtile) #############"
echo "###########################################################"

yay -S --noconfirm --quiet --needed python-pip 
pip install xcffib==1.4 --break-system-packages
pip install cairocffi==1.6 --break-system-packages
yay -S --noconfirm --quiet --needed python-pywlroots
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


echo "#####################################################"
echo "########## Configuring App Launcher (Rofi) ##########"
echo "#####################################################"
yay -S --noconfirm --quiet --needed rofi
rm rofi -rf
git clone --depth=1 https://github.com/adi1090x/rofi.git
cd rofi && chmod +x setup.sh && bash ./setup.sh && cd ..
rm -rf ./rofi

echo "#####################################################"
echo "#### Configuring Notification Daemon (Dunst) ########"
echo "#####################################################"
yay -S --noconfirm --quiet --needed dunst

echo "#####################################################"
echo "########## Configuring Browser (Qutebrowser) ########"
echo "#####################################################"
yay -S --quiet --needed --noconfirm qutebrowser 
rm -rf ~/.config/qutebrowser/catppuccin
git clone https://github.com/catppuccin/qutebrowser.git ~/.config/qutebrowser/catppuccin

echo "############################################"
echo "########## Install Picom ###################"
echo "############################################"
yay -S --quiet --needed --noconfirm picom
 
echo "###################################################"
echo "########## Install File Manager (Thunar) ##########"
echo "###################################################"
yay -S --quiet --needed --noconfirm thunar

echo "#################################################################"
echo "########## Install Screen Utils (arandr and autorandr) ##########"
echo "#################################################################"
yay -S --quiet --needed --noconfirm arandr autorandr

echo "###############################################################"
echo "########## Install Clipboard Utils (copyq and xclip) ##########"
echo "###############################################################"
yay -S --quiet --needed --noconfirm copyq
yay -S --quiet --needed --noconfirm xclip

echo "###################################################"
echo "########## Install Nerd Fonts (Iosevka Nerd) ######"
echo "###################################################"
yay -S --quiet --needed --noconfirm ttf-iosevka-nerd

echo "###################################################"
echo "########## Configuring Wallpaper (Nitrogen) #######"
echo "###################################################"
yay -S --noconfirm --quiet --needed nitrogen

echo "##########################################"
echo "########## Creating user dirs ############"
echo "##########################################"
yay -S --quiet --needed --noconfirm xdg-user-dirs
xdg-user-dirs-update --force

echo "################################################################"
echo "########## Installing themes (Dracula and Catppuccin) ##########"
echo "#####################################################@##########"
yay -S --quiet --needed --noconfirm lxappearance
yay -S --quiet --needed --noconfirm dracula-cursos-git
yay -S --quiet --needed --noconfirm dracula-icons-git
yay -S --quiet --needed --noconfirm catppuccin-gtk-theme-mocha

# Opcionais
echo "#####################################"
echo "########## Install ASDF-VM ##########"
echo "#####################################"
yay -S --quiet --needed --noconfirm asdf-vm

echo "##########################################"
echo "########## Installing AstroNvim ##########"
echo "##########################################"
yay -S --quiet --needed --noconfirm neovim npm fzf
rm -rf ~/.config/nvim
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim

echo "########################################"
echo "########## Installing Spotify ##########"
echo "########################################"
yay -S --quiet --needed --noconfirm spotify

echo "#################################################"
echo "########## Installing Notes (Obsidian) ##########"
echo "#################################################"
yay -S --quiet --needed --noconfirm obsidian

echo "###################################################"
echo "########## Make use of dotfiles ###################"
echo "###################################################"
echo ".dotfiles" >> .gitignore
rm -rf $HOME/.dotfiles
git clone --bare https://github.com/$USER/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
dotfiles checkout -f

echo "###################################################"
echo "########## Changing default shell to ZSH ##########"
echo "###################################################"
# Zsh as default shell
chsh -s /bin/zsh $(whoami)
