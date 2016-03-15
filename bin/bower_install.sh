#!/usr/bin/env bash

sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo npm install bower -g
bower install
rm -rf ../static/vendors/bootstrap
bower install bootstrap
