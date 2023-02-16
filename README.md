# Dotfiles
Dotfiles and instructions to make my SO portable and easy to replicate

## Last Screenshot
![image](https://github.com/igortxra/dotfiles/blob/main/screenshot.png?raw=true)

# How I Installed Arch Linux

- Boot live environment
- Connect to the internet
- Use archinstall command
    
    This command will make your life easier, some of my choices are:
    
   ```yaml
   Bootloader: grub
   Profile: xorg
   Audio: pipeware
   NetworkConfiguration: Copy ISO
   AdditionalPackages: [
   qtile, qutebrowser, zip, unzip, vi, vim, neovim, ly, brightnessctl, zsh, kitty, arandr, autorandr, dunst, feh, git, tree, fzf]
   ```
   Set a password for root and add an non root user


- Set public/private keys for SSH (note just to remember)

- Clone and checkout dotfiles repository
    
    ```bash
    echo ".dotfiles" >> .gitignore
    git clone --bare <https://github.com/igortxra/dotfiles.git> $HOME/.dotfiles
    alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
    dotfiles config --local status.showUntrackedFiles no
    dotfiles checkout
    ```
    **Obs.:** When checking out you may receive a message requesting to remove files when you already have them.

### Shell

- Make Zsh works as expected
    - Run `chsh -s /usr/bin/zsh` (to make it default shell)
    - Install `exa` and `procs` (that replace `ls` and `ps`. See more on [Rewritten in Rust Commands](https://zaiste.net/posts/shell-commands-rust))
    - Install `zsh-autosuggestions` from GitHub
    - Install and configure [powerlevel10k](https://github.com/romkatv/powerlevel10k) (zsh theme)
    - Custom as you want

### AUR helper
- Install yay
    ```bash
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si
    ```

### Display Manager

- Make Ly works as expected
    - Make sure Ly service is enabled

### Screen Locker

- Make betterlockscreen work as expected
    - Install and configure betterlockscreen
    - Install feh and set the wallpaper

### Window Manager

- Make Qtile works as expected
See [documentation](http://docs.qtile.org/en/stable) to install required dependencies for widgets
    - Install wireless_tools (for wlan widget)
    - Install iwgtk (for GUI on click of wlan widget)
    - Install alsa-utils (for volume)
    - Install python modules: iwlib psutil dbus-next
    - Install Font Awesome (Icons here: [https://fontawesome.com/v5/cheatsheet](https://fontawesome.com/v5/cheatsheet))
    - Install Flameshot (for screenshot)


### Compositor
- Make transparency, transitions, blur, etc. Work as expected
    - I used [this](https://github.com/lcdse7en/jonaburg-picom) fork of picom

### Launcher

- Make Rofi works as expected
    - I used a part of [adi1090x/rofi](https://github.com/adi1090x/rofi) for my rofi theme

### File Manager

- Make Thunar works as expected
    - Install and use lxappearence to set themes and icons. I used "Dracula".
    - Check custom actions to see if they match your setup

### Developer utilities

- Install asdf
- Install neovim and use [my configuration](https://github.com/igortxra/nvim)
- Install docker

### Fonts
Make sure that you have:
- ttf-font-awesmoe
- ttf-noto-nerd
- ttf-firacode-nerd

### Configurations
- Set Qutebrowser as default browser running: `xdg-settings set default-web-browser org.qutebrowser.qutebrowser.desktop`

- Set your Qutebrowser quickmarks (I stored somewhere and downloaded)

- Screen Profiles
    - First use **arandr** to configure screen layout
    - After that use **autorandr** to save the profile
         ```bash
            autorandr --save <profile-name>
         ```
    - In qtile configuration i mapped some shortcuts to switch between screen profiles
        
        I have 2 monitors (notebook and HDM1) and I use 3 different profiles:
        
        | Key (used for shortcuts) | Profile Name | Description |
        | --- | --- | --- |
        | SUPER + CTRL + 0 | onlynotebook | To use only notebook screen |
        | SUPER + CTRL + 1 | onlyexternal |  To use only external monitor |
        | SUPER + CTRL + 2 | dualmonitor | To use both, notebook and external screen. External as primary and notebook as secondary |
        
        In **qtile** configuration i have shortcuts to set these profiles
        

## About Qtile configuration

### Keybindings

MOD → Super or CAPS LOCK (Caps lock is remapped to act as Super)

| Modifier combination | Key | Action |
| --- | --- | --- |
| MOD | [1 ... 9] | Go to workspace |
| MOD | [H J K L] | Move between windows |
| MOD | E | File Explorer |
| MOD | W | Close focused window |
| MOD | P | Power Menu |
| MOD | M | Change screen focus |
| MOD | G | Grow Panel (for monadTall layout) |
| MOD | TAB | Next window layout |
| MOD | SPACE | App Launcher |
| MOD | PRTSC | Print Screen Menu |
| MOD | ENTER | Open Terminal Emulator |
| MOD + SHIFT | M | Move window to another screen |
| MOD + SHIFT | TAB | Previous window layout |
| MOD + SHIFT | [H J K L] | Move current window position |
| MOD  + CTRL | Q | Shutdown Qtile |
| MOD + CTRL | 0 | Set screen profile onlynotebook |
| MOD  + CTRL | R | Reload Qtile config |
| MOD + CTRL | 1 | Set screen profile onlyexternal |
| MOD + CTRL | 2 | Set screen profile dualmonitor |
| MOD + ALT | [H L] | Previous/Next Workspace |

### Keychords

For a better understand of table below, see KeyChords in qtile configuration.

| Modifier combination | Key | Mode | Description |
| --- | --- | --- | --- |
| MOD | O | OPEN | Another key will open something |
| MOD | S | SETTINGS | Another key to access modes: Audio, Brightness,  Wi-Fi,  Taskbar |
