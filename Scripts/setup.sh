# zsh-autosuggestions
rm -rf ~/.zsh/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions


# Astro Nvim - https://docs.astronvim.com/
rm ~/.local/share/nvim
rm ~/.local/state/nvim
rm ~/.cache/nvim
mv ~/.config/nvim ~/.config/nvim.bkp
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim


