#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
pip uninstall -y dnspython
pip install -r requirements.txt
git clone https://github.com/rvrsh3ll/Sublist3r.git
touch Sublist3r/__init__.py
exit 1
