# My Dotfiles

Here I store my dotfiles, which is meant to be used in Arch Linux.

# Table of Contents
1. [Main Applications](#main-applications)
2. [Installing (Considering you are installing from scratch)](#installing-considering-you-are-installing-from-scratch)
    1. [1. Use `archinstall` script to execute minimal installation](#1-use-archinstall-script-to-execute-minimal-installation)
    2. [2. When the basic installation is finished, reboot and login with the created user](#2-when-the-basic-installation-is-finished-reboot-and-login-with-the-created-user)
    3. [3. Run the setup script](#3-run-the-setup-script)
    4. [4. Reboot and Login](#4-reboot-and-login)
    5. [5. Post-setup customizations](#5-post-setup-customizations)
3. [Qtile Keybindings](#qtile-keybindings)
    1. [1. Basics](#1-basics)
    2. [2. Spawners/Menus](#2-spawnersmenus)
    3. [3. Screenshots](#3-screenshots)
    4. [4. Switch Between Windows](#4-switch-between-windows)
    5. [5. Move Windows](#5-move-windows)
    6. [6. Floating Windows](#6-floating-windows)
    7. [7. Resize Windows](#7-resize-windows)
    8. [8. Notifications](#8-notifications)
    9. [9. Music Control](#9-music-control)
    10. [10. Groups](#10-groups)
    11. [11. Move Window to Group (Non-exclusive groups)](#11-move-window-to-group-non-exclusive-groups)
4. [Screenshots](#screenshots)

## Main Applications
- Qtile (Window Manager)
- Zsh (Default Shell)
- Rofi (Launcher Menu)
- Kitty (Terminal Emulator)
- Dunst (Notification Daemon)
- Picom (Compositor)

## Installing (Consigering you are installing from scratch)
### 1. Use `archinstall` script to execute minimal installation:
  - Add your user (with sudo privileges);
  - Select **NetworkManager** as newtork;
  - Select **Xorg** as installation profile (will install xorg and graphic drivers);
  - Add **git** and **vim** (or any text editor) as additional package;

### 2. When the basic installation is finished, reboot and login with the created user.

### 3. Run the setup script
Once logged in, clone this repository and execute the setup script:
```bash
# Clone dotfiles into a temporary folder
git clone --depth 1 https://github.com/igortxra/dotfiles.git $HOME/temp

# Run setup script
. $HOME/temp/.setup.sh

# Remove temporary clone
rm -rf $HOME/temp
```

### 4. Reboot and Login
You will see the Qtile Interface.

### 5. Post-setup customizations
#### Set Wallpaper
A wallpaper will not be set by default. You need:
- Download a Wallpaper image and save into `~/Wallpapers`.
- Reload Qtile ([Check keybinding](### 1. Basics)).

**Obs.:** Qtile Bar has a widget for change the wallpaper.

#### Configure screen profiles
If u want to use more than one screen/monitor do the following:
- Use `arandr` to configure your screen.
- Open a terminal and run `autorandr --save <profile-name>`. E.g: `autorandr --save two-screens`.
- Repeat the last two steps for each profile you want to create.
- Now these profiles can be switched with the Screen Menu ([Check Keybinding](### 2. Spawners/Menus)).

## Qtile Keybindings
The <kbd>Caps Lock</kbd> act as <kbd>SUPER</kbd>. If you want to change this, edit `~/.local/bin/autostart.sh`;

### 1. Basics

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + control + r</kbd>            | Reload the config                          |
| <kbd>SUPER + control + q</kbd>            | Shutdown Qtile                             |
| <kbd>SUPER + x</kbd>                      | Kill focused window                        |
| <kbd>SUPER + Return</kbd>                 | Launch terminal                            |
| <kbd>SUPER + Tab</kbd>                    | Toggle between layouts                     |
| <kbd>SUPER + b</kbd>                      | Toggle bar visibility                      |
| <kbd>SUPER + m</kbd>                      | Change focus to the next screen            |

---

### 2. Spawners/Menus

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + e</kbd>                      | Spawn file manager                         |
| <kbd>SUPER + space</kbd>                  | Spawn application launcher                 |
| <kbd>SUPER + p</kbd>                      | Spawn power menu                           |
| <kbd>SUPER + s</kbd>                      | Spawn screens menu                         |
| <kbd>SUPER + v</kbd>                      | Spawn clipboard menu                       |
| <kbd>SUPER + =</kbd>                      | Spawn utils menu                           |

---

### 3. Screenshots

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>Print</kbd>                          | Launch screenshot menu                     |
| <kbd>SHIFT + Print</kbd>                  | Take a full-screen screenshot              |

---

### 4. Switch Between Windows

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + h</kbd>                      | Move focus to the left                     |
| <kbd>SUPER + l</kbd>                      | Move focus to the right                    |
| <kbd>SUPER + j</kbd>                      | Move focus down                            |
| <kbd>SUPER + k</kbd>                      | Move focus up                              |
| <kbd>SUPER + ALT + k</kbd>                | Focus the previous window                  |
| <kbd>SUPER + ALT + j</kbd>                | Focus the next window                      |

---

### 5. Move Windows

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + SHIFT + h</kbd>              | Move window to the left                     |
| <kbd>SUPER + SHIFT + l</kbd>              | Move window to the right                    |
| <kbd>SUPER + SHIFT + j</kbd>              | Move window down                            |
| <kbd>SUPER + SHIFT + k</kbd>              | Move window up                              |

---

### 6. Floating Windows

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + f</kbd>                      | Toggle window floating                     |
| <kbd>SUPER + c</kbd>                      | Center float window                        |
| <kbd>SUPER + ALT + SHIFT + k</kbd>        | Bring floating window to the front         |
| <kbd>SUPER + ALT + SHIFT + j</kbd>        | Move floating window to the bottom         |

---

### 7. Resize Windows

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>F10</kbd>                            | Toggle fullscreen on the focused window    |
| <kbd>SUPER + i</kbd>                      | Increase window size                       |
| <kbd>SUPER + d</kbd>                      | Decrease window size                       |
| <kbd>SUPER + r</kbd>                      | Reset window size                          |
| <kbd>SUPER + g</kbd>                      | Maximize window                            |

---

### 8. Notifications

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + n</kbd>                      | Open notification context                  |
| <kbd>SUPER + SHIFT + n</kbd>              | Close notification context                 |

---

### 9. Music Control

| **Keys**                         | **Description**                             |
|----------------------------------|---------------------------------------------|
| <kbd>SUPER + period</kbd>                 | Next music track                           |
| <kbd>SUPER + comma</kbd>                  | Previous music track                       |
| <kbd>SUPER + semicolon</kbd>              | Toggle play/pause music track              |

---

### 10. Groups
| Keybinding                                  | Description                            |
|---------------------------------------------|----------------------------------------|
| <kbd>SUPER</kbd> + <kbd>{number}</kbd>      | Switch to group (1-9)                  |
---

### 11. Move Window to Group (Non-exclusive groups)

| Keybinding                                                      | Description                            |
|-----------------------------------------------------------------|----------------------------------------|
| <kbd>SUPER</kbd> + <kbd>Shift</kbd> + <kbd>{number}</kbd>      | Move focused window to group (1-7)      /
---


## Screenshots
| TODO

