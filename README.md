# My Dotfiles

Here I store my dotfiles, which is meant to be used in Arch Linux.


## How to use

### 1. Clean arch linux installed

Using `archinstall` script you have to:
- Add your user (with sudo privileges)
- Select NetworkManager as newtork
- Select Xorg as installation profile (will install xorg and graphic drivers)
- Add **git**, **vim** and **ansible** as additional packages

When the basic installation is finished, reboot and login.


### 2. Clone ansible arch setup

This is a repository that contains a playbook which automates the system configuration.

```bash
git clone https://github.com/igortxra/ansible-arch-setup.git $HOME/setup
```

Use ansible to run the playbook
```bash
cd $HOME/setup
make setup
# Wait untill setup is finished
```


## Screenshots
![2024-01-22_19-13](https://github.com/igortxra/dotfiles-clean/assets/91085060/a3b0cdd7-618c-4528-b970-fbbd85aa9a42)
![2024-01-22_19-16](https://github.com/igortxra/dotfiles-clean/assets/91085060/b0ac6e1e-0848-4362-b014-95ab1c679baf)
