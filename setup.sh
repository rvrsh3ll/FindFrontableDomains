#!/bin/bash

[[ $# -gt 0 && "--venv" =~ $@ ]] && venv=true || venv=false

if [[ $EUID -ne 0 && $venv == "false" ]]; then
	echo "This script must be either run as root or within a virtual environment." 1>&2
	exit 1
fi

pip3 uninstall -y dnspython
pip3 install -r requirements.txt
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
python3 setup.py install
pip3 install -r requirements.txt
touch __init__.py
exit 1
