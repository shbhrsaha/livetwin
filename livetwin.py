#!/usr/bin/env python
#
# Copyright 2013 Shubhro Saha
#
# Licensed under Creative Commons Attribution 3.0 Unported. You may obtain
# a copy of the license at
#
#     http://creativecommons.org/licenses/by/3.0/deed.en_US
#
# No attribution to the original author is required.
#

"""Python library for syncing local filesystem changes with a remote filesystem

LiveTwin is a cross-platform "hacker's dropbox". 
It is a small python script that monitors the local 
filesystem for changes and syncs contents with a 
remote folder via rsync.

Usage: python livetwin.py [local dir] [remote dir] [server] [user]

"""

import os, sys
import time, datetime
import logging, getpass, pexpect

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ChangeHandler(LoggingEventHandler):
    """
        Adapts watchdog's LoggingEventHandler for LiveTwin's purpose
    """

    stale = True

    def sync(self):
        try:
            logging.info("Syncing...")
            child = pexpect.spawn("rsync -avz --delete %s %s@%s:%s" % (LOCAL_DIR, REMOTE_SERVER_USER, REMOTE_SERVER, REMOTE_DIR))
            child.expect(".*password:.*")
            child.sendline(REMOTE_SERVER_PASSWORD)
            child.expect(".*sent.*")

            logging.info("Sync complete")
        except:
            logging.info("Sync failed")

    def on_moved(self, event):
        self.stale = True
      
    def on_created(self, event):
        self.stale = True

    def on_deleted(self, event):
        self.stale = True

    def on_modified(self, event):
        if ".DS_Store" not in event.src_path:
            self.stale = True


if __name__ == "__main__":
    doc_string = ("Usage: python livetwin.py [local dir] [remote dir] [server] [user]").format(sys.argv[0])
    if len(sys.argv) < 5:
        print(doc_string)
        exit()

    # read arguments
    LOCAL_DIR = sys.argv[1]
    REMOTE_DIR = sys.argv[2]
    REMOTE_SERVER = sys.argv[3]
    REMOTE_SERVER_USER = sys.argv[4]
    REMOTE_SERVER_PASSWORD = getpass.getpass("Remote Server Password: ")

    # give feedback
    logging.info("Monitoring %s for changes and syncing with %s@%s:%s" % (LOCAL_DIR, REMOTE_SERVER_USER, REMOTE_SERVER, REMOTE_DIR))
    logging.info("First sync may take longer than usual...")

    # start observing and syncing
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=LOCAL_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            if event_handler.stale:
                event_handler.sync()
                event_handler.stale = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()