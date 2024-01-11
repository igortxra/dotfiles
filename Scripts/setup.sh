git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

# zsh-autosuggestions
rm -rf ~/.zsh/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions


# Astro Nvim - https://docs.astronvim.com/
rm ~/.local/share/nvim
rm ~/.local/state/nvim
rm ~/.cache/nvim
mv ~/.config/nvim ~/.config/nvim.bkp
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim

# Catppuccin Theme - Qutebrowser
git clone https://github.com/catppuccin/qutebrowser.git ~/.config/qutebrowser/catppuccin

# Catppuccin Theme - Qutebrowser
git clone https://github.com/catppuccin/qutebrowser.git ~/.config/qutebrowser/catppuccin

# Catppuccin Theme - GTK
yay -S catppuccin-gtk-theme-mocha --quiet --noconfirm --needed
