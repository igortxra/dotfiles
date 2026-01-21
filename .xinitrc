#!/bin/sh

xinitdir="/etc/X11/xinit"
if [ -d "$xinitdir"/xinitrc.d ] ; then
	for f in "$xinitdir/xinitrc.d"/?*.sh ; do
		[ -x "$f" ] && . "$f"
	done
	unset f
fi

export XDG_SESSION_TYPE=x11

exec dbus-run-session -- qtile start
