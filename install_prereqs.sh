#!/bin/bash

sudo apt-get update
sudo apt-get install -y Xvfb python-selenium unzip
sudo apt-get install -y chromium-browser
if [ ! -e /usr/local/bin/chromedriver ]
then
	TMP_DIR=`mktemp -d`
	cd "$TMP_DIR"
	wget 'https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip' --output-document=zipfile.zip
	unzip zipfile.zip
	sudo chown root:root chromedriver
	sudo mv chromedriver /usr/local/bin/
	cd -
	rm -r "$TMP_DIR"
fi

