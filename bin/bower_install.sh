#!/usr/bin/env bash

sudo apt-get install nodejs
sudo apt-get install npm
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo npm install bower -g
bower install
