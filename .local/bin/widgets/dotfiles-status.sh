local_status=$(git --git-dir=/home/$USER/.dotfiles --work-tree=/home/$USER status --short | grep -q . && echo "" || echo "")
remote_status=$(git --git-dir=/home/$USER/.dotfiles --work-tree=/home/$USER diff --name-only ORIG_HEAD | grep -q . && echo $local_status || echo "")


echo "Dotfiles $remote_status"| tr -d '\n'

