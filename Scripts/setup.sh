# Setup dotfiles
echo ".dotfiles" > ~/.gitignore
git clone --bare https://github.com/$USER/dotfiles.git $HOME/.dotfiles
alias dotfiles="/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME"
dotfiles config --local status showUntrackedFiles no
dotfiles checkout -f

# Install Yay AUR Helper
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

# Install packages
sudo pacman -S --needed --noconfirm --quiet - < ~/Setup/pkg-list.txt
yay -S --needed --noconfirm --quiet - < ~/Setup/foreign-pkg-list.txt

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

# Clone Catppuccin Wallpapers
git clone https://github.com/bsimic/catppuccin_wallpapers.git ~/Pictures/Wallpapers/catppuccin_wallpapers

# Change default shell to zsh
chsh $USER -s /bin/zsh
