LiveTwin
========

LiveTwin is a cross-platform "hacker's dropbox". It is a small python script that monitors the local filesystem for changes and syncs contents with a remote folder with rsync.

Installation
------------

1. Install dependencies:

	sudo pip install watchdog pexpect

2. Download livetwin.py

Usage
-----
Run LiveTwin from Terminal:

	python livetwin.py [local dir] [remote dir] [server] [user]

LiveTwin will then ask you for your password. Change the directory contents to watch instant sync!
