LiveTwin
========

LiveTwin is a cross-platform "hacker's dropbox". It is a small python script that monitors the local filesystem for changes and syncs contents with a remote folder via rsync.

Installation
------------
First, install dependencies:

	sudo pip install -r requirements.txt

Then, download livetwin.py

Usage
-----
Run LiveTwin from Terminal:

	python livetwin.py [local dir] [remote dir] [server] [user]

LiveTwin will then ask you for your password. Change the local directory contents to watch files instantly sync!

Coming Soon
------------
- PyPI installation
- Alias shortcut

