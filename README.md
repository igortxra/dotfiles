# Dotfiles
Dotfiles and instructions to make my SO portable and easy to replicate

## Demo video
>_TODO_

## Last Screenshot
![image](https://github.com/igortxra/dotfiles/assets/91085060/e8d16f8e-2442-472f-b361-f745fb0ea17e)


# How I Installed Arch Linux

## Installation Steps
- Boot live environment
- Set your keyboard layout `loadkeys <layout>`
- Connect to the internet 
    - Plug the ethernet cable or use iwctl for wireless connections `iwctl station <INTERFACE> connect <SSID>`
- Use archinstall command `archinstall`
    
    This command will make your life easier, some of my choices are:
    
   ```yaml
   Bootloader: systemd-bootctl
   Profile: xorg
   Audio: pipeware
   NetworkConfiguration: Copy ISO
   AdditionalPackages: [
        vim,                # Test Editor
        git,                # Git
  ]
   ```
   **Note 1:** Set a password for root and add an non root user \
   **Note 2:** You do not need chroot into the installed SO, just reboot and login \
   **Note 3:** I only install vim and git as additional packages at this point.
    

# Post Installation

## AUR helper - [Yay](https://github.com/Jguer/yay#readme)
- Install yay. (I will use it for all packages installations)
    ```bash
        git clone https://aur.archlinux.org/yay.git
        cd yay
        makepkg -si
    ```

## Shell - [Zsh](https://wiki.archlinux.org/title/Zsh)
- Run `chsh -s /usr/bin/zsh` (to make it default shell)
- Install `exa` and `procs` (that replace `ls` and `ps`. See more on [Rewritten in Rust Commands](https://zaiste.net/posts/shell-commands-rust))
- Clone `zsh-autosuggestions` [from GitHub](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#manual-git-clone)
- Install and configure [powerlevel10k](https://github.com/romkatv/powerlevel10k) (zsh theme)
- Install `fzf` fuzzy finder 

## Terminal Emulator - [Kitty](https://wiki.archlinux.org/title/Kitty)

## Display Manager - [Ly](https://github.com/fairyglade/ly)
- Enable Ly service
    ```bash
        sudo systemctl enable ly.service
    ```

## Window Manager - [Qtile](https://wiki.archlinux.org/title/Qtile)
- Install these packages:
    ```bash
        yay -S wireless_tools iwgtk alsa-utils flameshot python-pip

        # wireless_tools (for wlan widget)
        # iwgtk (for GUI on click of wlan widget)
        # alsa-utils (for volume)
        # flameshot (for screenshots)
        # pip (for install python packages)
    ```
    
- Install these python packages
    ```bash
        pip install iwlib psutil dbus-next
    ```

- Install a compositor (for transparency, transitions, blurs and more effects) \
    I use `picom-jonaburg-git`

**Note 1:** If Qtile renders broken icons (retangles), check your fonts. \
**Note 2:** Check [Qtile documentation](http://docs.qtile.org/en/stable)
**Note 3:** Make sure you have an terminal emulator installed before use Qtile.
    
## Fonts
I use Font Awesome because of icons and Iosevka because of ligations.
**Note:** I tried FiraCode, but somehow font awesome icons gets weird after FiraCode installation.
- I Install these fonts:
    ```bash
        yay -S ttf-font-awesome ttc-iosevka
    ```

## Wallpapers and Screen Locker - [Betterlockscreen](https://github.com/betterlockscreen/betterlockscreen)
- Download some wallpaper images into `~/wallpapers`

- Install the screen locker
    ```bash
        yay -S betterlockscreen
        betterlockscreen -u ~/wallpapers
    ```

- Use [Nitrogen](https://wiki.archlinux.org/title/Nitrogen) to set the wallpaper (or [Feh](https://wiki.archlinux.org/title/Feh) but remember to modify `~/.config/qtile/autostart.sh`)
    ```bash
        # Example
        nitrogen --set-auto wallpapers/your-image.png
    ```

## App Launcher and menus - [Rofi](https://wiki.archlinux.org/title/Rofi)
-   - Run `dotfiles restore ~/.config/rofi`
    - For power menu works as expected with you have to find a way to allow your user run poweroff and reboot commands without sudo. I Used [**polkit**](https://wiki.archlinux.org/title/Polkit) and created a file for these rules:
```javascript
polkit.addRule(function(action, subject) {
	if (	action.id == "org.freedesktop.login1.power-off" ||
		action.id == "org.freedesktop.login1.reboot" ||
		action.id == "org.freedesktop.login1.suspend" ||
		action.id == "org.freedesktop.login1.hibernate"
	) {
		if (subject.isInGroup("wheel")) {
			return polkit.Result.YES;
		}
	}
});
```
**Note:** It is possible use sudo for this too.

## File Manager - [Thunar](https://wiki.archlinux.org/title/Thunar)
- Check **custom actions** to see if they match your setup.]
- Install `ffmpegthumbnailer` and `tumbler`


# Dotfiles (This reposiory)
- Clone and checkout dotfiles repository
    
    ```bash
    echo ".dotfiles" >> .gitignore
    git clone --bare <https://github.com/igortxra/dotfiles.git> $HOME/.dotfiles
    alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
    dotfiles config --local status.showUntrackedFiles no
    dotfiles checkout
    ```
    **Obs.:** When checking out you may receive a message requesting to remove files when you already have them.


## Developer utilities
- asdf-vm
- neovim with [my configuration](https://github.com/igortxra/nvim)
- docker
- github-cli

## Other
### Discord 
`yay -S discord ttf-symbola noto-fonts-cjk noto-fonts-emoji`
### OBS Studio 
`yay -S obs-studio-git`
### udiskie 
`yay -S udiskie` and see [permissions](https://github.com/coldfix/udiskie/wiki/Permissions)

## More Configurations
- Install and use **lxappearance** to set themes and icons. I like [Catppuccin](https://github.com/catppuccin) for colors and [Dracula](https://draculatheme.com/) icons.

- Set Qutebrowser as default browser running: `xdg-settings set default-web-browser org.qutebrowser.qutebrowser.desktop`

- Set your Qutebrowser quickmarks (I stored somewhere and downloaded)

- Set a theme for Qutebrowser such as [Dracula](https://draculatheme.com/qutebrowser)

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
| MOD | 0 | Remap capslock as super|
| MOD | [1 ... 9] | Go to workspace |
| MOD | N | Next Workspace/Group |
| MOD | B | Previous Workspace/Group |
| MOD | [H J K L] | Move between windows |
| MOD + SHIFT | [H J K L] | Move current window position |
| MOD | ENTER | Open Terminal Emulator |
| MOD | W | Close focused window |
| MOD | E | File Explorer |
| MOD | P | Power Menu |
| MOD | M | Change screen focus |
| MOD + SHIFT | M | Move window to (the current group of) another screen |
| MOD | G | Grow main Panel (for monadTall layout) |
| MOD + SHIFT | G | Shrink main Panel (for monadTall layout) |
| MOD | TAB | Next window layout |
| MOD + SHIFT | TAB | Previous window layout |
| MOD | SPACE | App Launcher |
| MOD | PRTSC | Print Screen Menu |
| MOD  + CTRL | Q | Shutdown Qtile |
| MOD  + CTRL | R | Reload Qtile config |
| MOD + CTRL | 0 | Set screen profile onlynotebook |
| MOD + CTRL | 1 | Set screen profile onlyexternal |
| MOD + CTRL | 2 | Set screen profile dualmonitor |

### Keychords

For a better understand of table below, see KeyChords in Qtile documentation.

| Modifier combination | Key | Mode | Description |
| --- | --- | --- | --- |
| MOD | S | SETTINGS | Another key to access modes: Audio, Brightness,  Wi-Fi,  Taskbar |

## Notes
- Fullscreen ArchLinux in VirtualBox: https://youtu.be/hmku7eW8UFg
- Set public/private keys for SSH (note just to remember)
