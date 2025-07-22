# My Dotfiles
🗄️ Here I store my dotfiles. Think the repo root as the $HOME dir. This README.md are a mini documentation of how I manage my OS.

🫠 Basically an `Arch Linux` OS with `Qtile` as Window Manager; `Xorg` as display server with `Picom` compositor.

## How it Looks 
![image](https://github.com/user-attachments/assets/7bddf0a4-3cb6-4110-bbf9-f72b2befa1a4)

## Summary
  - [Main Applications](#main-applications)
  - [Installing](#installing)
    - [1. Minimal installation](#minimal-installation)
    - [2. Setup Script](#setup-script)
    - [3. First-run settings](#first-run-settings)
      - [Wallpaper](#wallpaper)
      - [Screens](#screens)
  - [Keybindings](#keybindings)
    - [Remaps](#remaps)
    - [Basics](#basics)
    - [Switch Between Windows](#switch-between-windows)
    - [Apps and Menus](#apps-and-menus)
    - [Screenshots](#screenshots)
    - [Move Windows](#move-windows)
    - [Floating Windows](#floating-windows)
    - [Resize Windows](#resize-windows)
    - [Notifications](#notifications)
    - [Music Control](#music-control)
    - [Groups](#groups)
    - [Move Window to Group](#move-window-to-group)
  - [How it Looks](#how-it-looks)

Here I store my dotfiles, which is meant to be used in Arch Linux.

## Main Applications
- Qtile (Window Manager)
- Zsh (Default Shell)
- Rofi (Launcher Menu)
- Kitty (Terminal Emulator)
- Dunst (Notification Daemon)
- Picom (Compositor)
- Network Manager

See all the packages in `PACKAGES.md`

## Installing
(Consigering you are installing from scratch)

### Minimal installation
With `archinstall`:
  - Add your user (with sudo privileges);
  - Select **NetworkManager** as newtork;
  - Select **Xorg** as installation profile (will install xorg and graphic drivers);
  - Add **git** and **vim** (or any text editor) as additional package;

When the basic installation is finished, reboot and login with the created user.

### Setup Script
Once logged in, clone this repository and execute the setup script:
```bash
# Clone dotfiles into a temporary folder
git clone --depth 1 https://github.com/igortxra/dotfiles.git $HOME/temp

# Run setup script
. $HOME/temp/.setup.sh

# Remove temporary clone
rm -rf $HOME/temp
```
Reboot and login. You will see the Qtile Interface.

### First-run settings
#### Wallpaper
A wallpaper will not be set by default. You need:
- Download a Wallpaper image and save into `~/Wallpapers`.
- Reload Qtile (Check Keybindings).

**Obs.:** Qtile Bar has a widget for change the wallpaper.

#### Screens
If u want to use more than one screen/monitor do the following:
- Use `arandr` to configure your screen.
- Open a terminal and run `autorandr --save <profile-name>`. E.g: `autorandr --save two-screens`.
- Repeat the last two steps for each profile you want to create.
- Now these profiles can be switched with the Screen Menu (Check Keybindings).

## Keybindings

### Remaps
The <kbd>Caps Lock</kbd> act as <kbd>SUPER</kbd>. 
If you want to change this, edit `~/.local/bin/autostart.sh`;

### Basics

| Keys                                                 | Description                        |
|------------------------------------------------------|------------------------------------|
| <kbd>SUPER</kbd> + <kbd>control</kbd> + <kbd>r</kbd> | Reload the config                  |
| <kbd>SUPER</kbd> + <kbd>control</kbd> + <kbd>q</kbd> | Shutdown Qtile                     |
| <kbd>SUPER</kbd> + <kbd>x</kbd>                      | Kill focused window                |
| <kbd>SUPER</kbd> + <kbd>Return</kbd>                 | Launch terminal                    |
| <kbd>SUPER</kbd> + <kbd>Tab</kbd>                    | Toggle between layouts             |
| <kbd>SUPER</kbd> + <kbd>b</kbd>                      | Toggle bar visibility              |
| <kbd>SUPER</kbd> + <kbd>m</kbd>                      | Change focus to the next screen    |

---

### Switch Between Windows

| Keys                                                 | Description                           |
|------------------------------------------------------|---------------------------------------|
| <kbd>SUPER</kbd> + <kbd>h</kbd>                      | Move focus to the left                |
| <kbd>SUPER</kbd> + <kbd>l</kbd>                      | Move focus to the right               |
| <kbd>SUPER</kbd> + <kbd>j</kbd>                      | Move focus down                       |
| <kbd>SUPER</kbd> + <kbd>k</kbd>                      | Move focus up                         |
| <kbd>SUPER</kbd> + <kbd>ALT</kbd> + <kbd>k</kbd>     | Focus the previous window             |
| <kbd>SUPER</kbd> + <kbd>ALT</kbd> + <kbd>j</kbd>     | Focus the next window                 |

---

### Apps and menus

| Keys                                                 | Description                       |
|------------------------------------------------------|-----------------------------------|
| <kbd>SUPER</kbd> + <kbd>e</kbd>                      | Spawn file manager                |
| <kbd>SUPER</kbd> + <kbd>space</kbd>                  | Spawn application launcher        |
| <kbd>SUPER</kbd> + <kbd>p</kbd>                      | Spawn power menu                  |
| <kbd>SUPER</kbd> + <kbd>s</kbd>                      | Spawn screens menu                |
| <kbd>SUPER</kbd> + <kbd>v</kbd>                      | Spawn clipboard menu              |
| <kbd>SUPER</kbd> + <kbd>=</kbd>                      | Spawn utils menu                  |

---

### Screenshots

| Keys                                     | Description                             |
|------------------------------------------|-------------------------------------------|
| <kbd>Print</kbd>                         | Launch screenshot menu                    |
| <kbd>SHIFT</kbd> + <kbd>Print</kbd>      | Take a full-screen screenshot             |

---

### Move Windows

| Keys                                                            | Description                            |
|-----------------------------------------------------------------|----------------------------------------|
| <kbd>SUPER</kbd> + <kbd>SHIFT</kbd> + <kbd>h</kbd>              | Move window to the left                |
| <kbd>SUPER</kbd> + <kbd>SHIFT</kbd> + <kbd>l</kbd>              | Move window to the right               |
| <kbd>SUPER</kbd> + <kbd>SHIFT</kbd> + <kbd>j</kbd>              | Move window down                       |
| <kbd>SUPER</kbd> + <kbd>SHIFT</kbd> + <kbd>k</kbd>              | Move window up                         |

---

### Floating Windows

| Keys                                                                       | Description                                |
|----------------------------------------------------------------------------|--------------------------------------------|
| <kbd>SUPER</kbd> + <kbd>f</kbd>                                            | Toggle window floating                     |
| <kbd>SUPER</kbd> + <kbd>c</kbd>                                            | Center float window (and bring to front)   |
| <kbd>SUPER</kbd> + <kbd>ALT</kbd> + <kbd>f</kbd>                           | Bring floating window to the front         |
| <kbd>SUPER</kbd> + <kbd>ALT</kbd> + <kbd>b</kbd>                           | Move floating window to the bottom         |

---

### Resize Windows

| Keys                                | Description                                |
|-------------------------------------|--------------------------------------------|
| <kbd>F10</kbd>                      | Toggle fullscreen on the focused window    |
| <kbd>SUPER</kbd> + <kbd>i</kbd>     | Increase window size                       |
| <kbd>SUPER</kbd> + <kbd>d</kbd>     | Decrease window size                       |
| <kbd>SUPER</kbd> + <kbd>r</kbd>     | Reset window size                          |
| <kbd>SUPER</kbd> + <kbd>g</kbd>     | Maximize window                            |

---

### Notifications

| Keys                                                 | Description                |
|------------------------------------------------------|------------------------------|
| <kbd>SUPER</kbd> + <kbd>n</kbd>                      | Open notification context    |
| <kbd>SUPER</kbd> + <kbd>SHIFT</kbd> + <kbd>n</kbd>   | Close notification context   |

---

### Music Control

| Keys                                     | Description                     |
|------------------------------------------|---------------------------------|
| <kbd>SUPER</kbd> + <kbd>period</kbd>     | Next music track                |
| <kbd>SUPER</kbd> + <kbd>comma</kbd>      | Previous music track            |
| <kbd>SUPER</kbd> + <kbd>semicolon</kbd>  | Toggle play/pause music track   |

---

### Groups
| Keybinding                                  | Description                            |
|---------------------------------------------|----------------------------------------|
| <kbd>SUPER</kbd> + <kbd>{number}</kbd>      | Switch to group (1-9)                  |

---

### Move Window to Group
| Keybinding                                                     | Description                            |
|----------------------------------------------------------------|----------------------------------------|
| <kbd>SUPER</kbd> + <kbd>Shift</kbd> + <kbd>{number}</kbd>      | Move focused window to group (1-9)     |

---



