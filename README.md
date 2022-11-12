# Dotfiles
Dotfiles and instructions to make my SO portable and easy to replicate

## Last Screenshot
![image](https://user-images.githubusercontent.com/91085060/200951007-c51a142a-c3b7-438c-bdb2-2f0c5468c4f2.png)

# How I Installed Arch Linux

- Boot live environment
- Use archinstall command
    
    This command will make your life easier, some of my choices are:
    

   ```yaml
   Bootloader: grub
   Profile: xorg
   Audio: pulseaudio
   NetworkConfiguration: Copy ISO
   AdditionalPackages: [
   qtile, qutebrowser, ranger, zip, unzip, vi, vim, neovim, lightdm, lightdm-gtk-greeter, picom, brightnessctl, zsh, alacritty, arandr, autorandr, dunst, feh, git]

   ```

- Set public and private key for SSH (note just to remember)
- Clone and checkout dotfiles repository
    
    ```bash
    echo ".dotfiles" >> .gitignore
    git clone --bare <https://github.com/igortxra/dotfiles.git> $HOME/.dotfiles
    3alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
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

### Screen Locker

- Make betterlockscreen work as expected
    - Install and configure betterlockscreen
    - Install feh and set the wallpaper

### Window Manager

- Make Qtile works as expected
See [documentation](http://docs.qtile.org/en/stable) to install required dependencies for widgets
    - Install wireless_tools (for wlan widget)
    - Install alsa-utils (for volume)
    - Install python modules: iwlib psutil dbus-next
    - Install Font Awesome (Icons here: [https://fontawesome.com/v5/cheatsheet](https://fontawesome.com/v5/cheatsheet))
    - Install Flameshot (for screenshot)

### Display Manager

- Make Lightdm works as expected
    - Install and run `sudo lightdm-gtk-greeter-settings`
    - Make sure lightdm service is enabled

### Launcher

- Make Rofi works as expected
    - Install Rofi and [adi1090x/rofi](https://github.com/adi1090x/rofi)
    - Custom as you want

### Developer utilities

- Install asdf
- Install LunarVim (needs neovim)
- Install docker

### Optionals

- Optional utilities
    - Install xdg-user-dirs (for /home organization)
    - Run `xdg-user-dirs-update`

### Configurations

- Screen Profiles
    - Use **arandr** to configure screen layout
    - Use **autorandr** to save the profile
        
        ```bash
        autorandr --save <profile-name>
        ```
        
        I use 3 different profiles:
        
        | Key (used for shortcuts) | Profile Name | Description |
        | --- | --- | --- |
        | 0 | onlynotebook | To use only notebook screen |
        | 1 | onlyexternal |  To use only external monitor |
        | 2 | dualmonitor | To use both, notebook and external screen. External as primary and notebook as secondary |
        
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
