"""
	This script monitors a local directory and copies files to a remote directory when there are changes
	NOTE: Doesn't work with VIM because it apparently doesn't change the last modified timestamp

	Example usage: python livetwin.py temp/ temp/ nobel.princeton.edu saha

	if the local folder is temp/ in the same directory as livetwin.py
	and the remote folder is temp/ in the home directory of nobel.princeton.edu
"""

import os, sys, datetime, time, getpass, pexpect

import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


#TODO: turn this into proper argument reading soon!
LOCAL_DIR = sys.argv[1]
REMOTE_DIR = sys.argv[2]
REMOTE_SERVER = sys.argv[3]
REMOTE_SERVER_USER = sys.argv[4]
REMOTE_SERVER_PASSWORD = getpass.getpass("Remote Server Password: ")

print "Monitoring %s for changes and syncing with %s@%s:%s" % (LOCAL_DIR, REMOTE_SERVER_USER, REMOTE_SERVER, REMOTE_DIR)

print "First sync will take longer than the rest..."

class ChangeHandler(LoggingEventHandler):

    stale = True
        
    def sync(self):
        try:
            print "%s: Syncing..." % datetime.datetime.now()
            child = pexpect.spawn("rsync -avz --delete %s %s@%s:%s" % (LOCAL_DIR, REMOTE_SERVER_USER, REMOTE_SERVER, REMOTE_DIR))
            child.expect(".*password:.*")
            child.sendline(REMOTE_SERVER_PASSWORD)
            child.expect(".*sent.*")

            print "%s: Sync complete" % datetime.datetime.now()
        except:
            print "%s: Sync failed" % datetime.datetime.now()

    def on_moved(self, event):
        self.stale = True
      
    def on_created(self, event):
        self.stale = True

    def on_deleted(self, event):
        self.stale = True

    def on_modified(self, event):
        if ".DS_Store" not in event.src_path:
            self.stale = True

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
event_handler = ChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=sys.argv[1], recursive=True)
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