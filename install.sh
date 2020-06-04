#!/usr/bin/env bash
#Author:Igwaneza Bruce
#Email:knowbeeinc@gmail.com


echo "installing packages..."

pip3 install -r requirements.txt
filename="wisty.py"
path=$PWD/$filename
echo "configuring wisty"
echo "alias wisty=$path" >> ~/.bashrc 
exec bash
echo "wisty installed successfully"
