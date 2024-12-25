#!/bin/bash

# OS check
if [ "$(uname)" != "Darwin" ]; then
	echo "Admin permissions need to install newer packages"
	sudo apt install libbsd-dev libncurses-dev
fi
# navigate to francinette directory
cd "$HOME"/francinette || exit

# update git repo
git fetch origin
git reset --hard origin
git submodule update --init

# activate venv
. venv/bin/activate

# install requirements
echo "Updating python dependencies..."
if ! pip3 install --disable-pip-version-check -q -r requirements.txt ; then
	echo "Problem updating francinette. Contact me (fsoares- on slack)"
	exit 1
fi

# final messages
echo -e "\033[1;37mFrancinette is updated. You can use it again!\033[0m"

printf "\033[33m... but don't forget, \033[1;37mpaco\033[0;33m is not a replacement for your own tests! \033[0m\n"
