
# Arch Linux Dotfiles

Dotfiles and information about what i use in my linux setup
## Screenshot
![image](https://github.com/igortxra/dotfiles/blob/main/screenshot.png)

## Details
#### Install Arch Linux following the official documentation
First packages installed (via pacstrap from live environment):
- base base-devel linux linux-firmware git vi vim sudo

#### Install and configure more packages

- **Network manager**: systemd-networkd (needs to be enabled) 
- **Wireless manager**: [iwd](https://wiki.archlinux.org/title/Iwd#Optional_configuration) (needs to be enabled) \
    **Obs.**: set *systemd-resolved* as *NameResolvingService* in `/etc/iwd/main.conf` \
    **with**: iwgtk

- **Bootloader**: [GRUB](https://wiki.archlinux.org/title/GRUB) and efibootmgr (see [microcode](https://wiki.archlinux.org/title/Microcode))
- **Mirrors sync**: [Reflector](https://wiki.archlinux.org/title/Reflector)

##### Audio
- **Video driver**: x86-video-... (it depends on your machine)
- **Sound System**: alsa-utils; alsa-firmeware; pulseaudio; pulseaudio-alsa; sof-firmeware;

##### Video
- **Display server**: xorg
- **Compositor**: [picom](https://wiki.archlinux.org/title/Picom)
- **Brightness**: brightnessctl

##### Window Manager and other choices
- **Window manager**: [Qtile](https://wiki.archlinux.org/title/Qtile) \
    **Obs.:**: Remember to see [documentation](http://docs.qtile.org/en/stable) to install required dependencies for widgets
- **Display manager**: lightdm \
    **with**: lightdm-gtk-greeter \
    **with**: lightdm-gtk-greeter-settings
    
- **Terminal emulator**: Alacritty
- **Shell**: zsh \
    **run**: `chsh -s /usr/bin/zsh` (to make it default shell) \
    **with**: [powerlevel10k](https://github.com/romkatv/powerlevel10k) \
    **with**: zsh-autosuggestions \
    **with**: [Rewritten in Rust Commands](https://zaiste.net/posts/shell-commands-rust)

- **Web Browser**: Qutebrowser
- **File Explorer**: Ranger    
- **AUR helper**: yay
- **Notifications**: Dunst
- **Screen locker**: betterlockscreen \
    **run**: `betterlockscreen -u ~/Pictures/wallpaper.jpg`
- **Wallpapel and image viewer**: feh 

- **Launcher**: rofi \
    **for**: Power Menu, Apps Menu \
    **with**: [adi1090x/rofi](https://github.com/adi1090x/rofi) (as theme)

+ **Fonts**: 
    - Fira Code
    - Noto fonts
    - Nerd fonts

- **User Directories**: xdg-user-dirs \
    **for**: Manage "well known" user directories
    **run**: xdg-user-dirs-update

##### Development utilities
- **Code editor**: neovim \
   **with**: lunarvim as IDE layer
- **Language version manager**: asdf
- **Containers**: Docker

##### Screenshot utilities
- **maim xclip viewnior**

##### More
- **Compression**: zip unzip

## Using this dotfiles
```bash
echo ".dotfiles" >> .gitignore
git clone --bare https://github.com/igortxra/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
dotfiles checkout
```
**Obs.:** When checking out you may receive a message requesting to remove files when you already have them.
