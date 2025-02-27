
## Notifications

#### Send notifications
```bash
dunstify -a System -t 5000 "Title Here" "Body of the message here"
```

## Packages

#### List explicit installed packages
```bash
pacman -Qqe
```

#### Diff of PACKAGES.md file and installed packages
```bash
delta --side-by-side <(grep -v -e '^\s*$' -e '^#' ~/PACKAGES.md | sort) <(pacman -Qqe) 
```

#### Show packages installed that are not in PACKAGES.md
```bash
comm -13 <(grep -v -e '^\s*$' -e '^#' ~/PACKAGES.md | sort) <(pacman -Qqe | sort)
```

#### Show that are in PACKAGES.md but are not installed
```bash
comm -23 <(grep -v -e '^\s*$' -e '^#' ~/PACKAGES.md | sort) <(pacman -Qqe | sort) 
```
