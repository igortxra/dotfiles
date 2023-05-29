# Dotfiles
Dotfiles and instructions to make my OS portable and easy to replicate.

## Demo video
>_TODO_

## Last Screenshot
![image](https://github.com/igortxra/dotfiles/assets/91085060/e8d16f8e-2442-472f-b361-f745fb0ea17e)


# How I Installed Arch Linux

## Installation Steps
- Boot into the live environment.
- Set your keyboard layout: `loadkeys <layout>`.
- Connect to the internet:
    - Plug in the Ethernet cable or use `iwctl` for wireless connections: `iwctl station <INTERFACE> connect <SSID>`.
- Use the `archinstall` command.
    
    This command will make your life easier. Here are some of my choices:
    
   ```yaml
   Bootloader: systemd-bootctl
   Profile: xorg
   Audio: pipewire
   NetworkConfiguration: Copy ISO
   AdditionalPackages: [
        vim,                # Text Editor
        git,                # Git
  ]
   ```
   **Note 1:** Set a password for root and add a non-root user. \
   **Note 2:** You do not need to chroot into the installed OS, just reboot and log in. \
   **Note 3:** At this point, I only install Vim and Git as additional packages.
    

# Post Installation


## AUR helper - [Yay](https://github.com/Jguer/yay#readme)
- Install yay (I will use it for all package installations):
    ```bash
        git clone https://aur.archlinux.org/yay.git
        cd yay
        makepkg -si
    ```


## Shell - [Zsh](https://wiki.archlinux.org/title/Zsh)
- Run `chsh -s /usr/bin/zsh` to make it the default shell.
- Install `exa` and `procs` (which replace `ls` and `ps`, respectively). See more on [Rewritten in Rust Commands](https://zaiste.net/posts/shell-commands-rust).
- Clone `zsh-autosuggestions` [from GitHub](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#manual-git-clone).
- Install and configure [powerlevel10k](https://github.com/romkatv/powerlevel10k) (a Zsh theme).
- Install `fzf` (a fuzzy finder).


## Terminal Emulator - [Kitty](https://wiki.archlinux.org/title/Kitty)


## Display Manager - [Ly](https://github.com/fairyglade/ly)
- Enable the Ly service:
    ```bash
        sudo systemctl enable ly.service
    ```


## Window Manager - [Qtile](https://wiki.archlinux.org/title/Qtile)
- Install the following packages:
    ```bash
        yay -S wireless_tools iwgtk alsa-utils flameshot python-pip

        # wireless_tools (for the wlan widget)
        # iwgtk (for GUI on click of the wlan widget)
        # alsa-utils (for volume)
        # flameshot (for screenshots)
        # pip (for installing Python packages)
    ```
    
- Install the following Python packages:
    ```bash
        pip install iwlib psutil dbus-next
    ```

- Install a compositor for transparency, transitions, blurs, and more effects. I use `picom-jonaburg-git`.

**Note 1:** If Qtile renders broken icons (rectangles), check your fonts. \
**Note 2:** Check the [Qtile documentation](http://docs.qtile.org/en/stable). \
**Note 3:** Make sure you have a terminal emulator installed before using Qtile.


## Fonts
I use Font Awesome for icons and Iosevka for ligatures.
**Note:** I tried FiraCode, but somehow Font Awesome icons looked weird after installing FiraCode.
- Install the following fonts:
    ```bash
        yay -S ttf-font-awesome ttc-iosevka
    ```


## Wallpapers and Screen Locker - [Betterlockscreen](https://github.com/betterlockscreen/betterlockscreen)
- Download some wallpaper images into `~/wallpapers`.

- Install the screen locker:
    ```bash
        yay -S betterlockscreen
        betterlockscreen -u ~/wallpapers
    ```


- Use [Nitrogen](https://wiki.archlinux.org/title/Nitrogen) to set the wallpaper (or [Feh](https://wiki.archlinux.org/title/Feh), but remember to modify `~/.config/qtile/autostart.sh`):
    ```bash
        # Example
        nitrogen --set-auto wallpapers/your-image.png
    ```


## App Launcher and Menus - [Rofi](https://wiki.archlinux.org/title/Rofi)
- Run `dotfiles restore ~/.config/rofi`.
- For the power menu to work as expected, you have to find a way to allow your user to run poweroff and reboot commands without sudo. I used [**polkit**](https://wiki.archlinux.org/title/Polkit) and created a file for these rules:
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
**Note:** It is also possible to use sudo for this.


## File Manager - [Thunar](https://wiki.archlinux.org/title/Thunar)
- Check **custom actions** to see if they match your setup.
- Install `ffmpegthumbnailer` and `tumbler`.


# Dotfiles (This repository)
*Note:* Use this repository as a reference. Fork it because I change my dotfiles quite often.
- Clone and checkout the dotfiles repository:
    
    ```bash
    echo ".dotfiles" >> .gitignore
    git clone --bare https://github.com/igortxra/dotfiles.git $HOME/.dotfiles
    alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
    dotfiles config --local status.showUntrackedFiles no
    dotfiles checkout
    ```
    **Note:** When checking out, you may receive a message requesting to remove files that you already have.


## Developer Utilities
- asdf-vm
- Neovim with [my configuration](https://github.com/igortxra/nvim)
- Docker
- GitHub CLI

## Other
### Discord 
`yay -S discord ttf-symbola noto-fonts-cjk noto-fonts-emoji`
### OBS Studio 
`yay -S obs-studio-git`
### udiskie 
`yay -S udiskie` and see [permissions](https://github.com/coldfix/udiskie/wiki/Permissions)


## More Configurations
- Install and use **lxappearance** to set themes and icons. I like [Catppuccino](https://github.com/cat

ppuccino) for colors and [Dracula](https://draculatheme.com/) icons.

- Set Qutebrowser as the default browser by running: `xdg-settings set default-web-browser org.qutebrowser.qutebrowser.desktop`

- Set your Qutebrowser quickmarks (I stored them somewhere and downloaded them).

- Set a theme for Qutebrowser, such as [Dracula](https://draculatheme.com/qutebrowser).

- Screen Profiles:
    - First, use **arandr** to configure the screen layout.
    - After that, use **autorandr** to save the profile:
         ```bash
            autorandr --save <profile-name>
         ```
    - In the qtile configuration, I mapped some shortcuts to switch between screen profiles.
        
        I have 2 monitors (notebook and HDMI) and I use 3 different profiles:
        
        | Key (used for shortcuts) | Profile Name | Description |
        | --- | --- | --- |
        | SUPER + CTRL + 0 | onlynotebook | To use only the notebook screen |
        | SUPER + CTRL + 1 | onlyexternal | To use only the external monitor |
        | SUPER + CTRL + 2 | dualmonitor | To use both the notebook and external screens, with the external screen as primary and the notebook screen as secondary |
        
        In the **qtile** configuration, I have shortcuts to set these profiles.


## About Qtile Configuration

### Keybindings

MOD → Super or CAPS LOCK (Caps lock is remapped to act as Super)

| Modifier combination | Key | Action |
| --- | --- | --- |
| MOD | 0 | Remap caps lock as Super|
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

For a better understanding of the table below, see KeyChords in the Qtile documentation.

| Modifier combination | Key | Mode | Description |
| --- | --- | --- | --- |
| MOD | S | SETTINGS | Another key to access modes: Audio, Brightness, Wi-Fi, Taskbar |


## Notes
- Fullscreen Arch Linux in VirtualBox: https://youtu.be/hmku7eW8UFg
- Set up public/private keys for SSH (just a reminder).
