# Dotfile
Dotfiles and instructions to make my OS portable and easy to replicate.

## Demo video
>_TODO_

## Last Screenshot
>_TODO_

# How To Use
Before do the following steps make sure you forked this repository.

I am assuming you already know how to use archinstall script

- (optional) set the keyboard layout to make your life easier. Use `loadkeys <layout>`. Eg.: loadkeys br-abnt2
- run `archinstall` and set your choices.
    Make sure you:
    - Added a root password
    - Added a user and set it as sudo
    - Added git in additional packages
    - Select xorg profile 
    - Install and reboot 
- login in the user account you created earlier
- clone your fork using git: `git clone https://github.com/<your-user>/dotfiles.git`
- run `bash dotfiles/install.sh`
- reboot and done

### Configuring themes
- lxappearance

### Making github widget work
- Create a file `~/.github_token` with your personal token `ghp...`

### Configuring multiple monitors
For each combination of screen layout do the follow:
- Use arandr to configure a layout
- Open a terminal and run `autorandr --save <profile-name>`
Obs: To switch between profiles use SUPER+A

### Notes
- `dotfiles` command will be an alias to use git for your dotfiles. Eg.: `dotfiles status -u`. Check .gitignore befora adding new things.
- As browser I use qutebrowser, to keep my quickmarks with me I store somewhere and recover on new installations
