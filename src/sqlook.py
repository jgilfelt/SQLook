'''
Created on Jun 6, 2012

@author: jgilfelt
'''

import subprocess
import os
from os.path import expanduser
import optparse
import shelve
import tempfile
import threading
import time

class WatchFileThread (threading.Thread):
    
    def __init__(self, threadID, name, pkg, db, adb_cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pkg = pkg
        self.db = db
        self.adb_cmd = adb_cmd
        
    def run(self):
        print "Starting watcher"
        monitor_push_changes(self.name, self.pkg, self.db, self.adb_cmd)
        print "Exiting watcher"
        
def main():
    p = optparse.OptionParser()
    # mirror the adb device options
    p.add_option('-d', dest='use_device', default=False, action='store_true',
                 help='directs command to the only connected USB device, returns an error if more than one USB device is present.')
    p.add_option('-e', dest='use_emulator', default=False, action='store_true',
                 help='directs command to the only running emulator, returns an error if more than one emulator is running.')
    p.add_option('-s', metavar='<specific device>',
                 help='directs command to the device or emulator with the given serial number or qualifier. Overrides ANDROID_SERIAL environment variable.')
    # manual configure
    p.add_option('--configure', dest='configure', default=False, action='store_true',
                 help='configure the default SQLite client.')
    options, arguments = p.parse_args()
    
    # validate args
    if len(arguments) != 2:
        p.print_help()
        return
    pkg = arguments[0]
    db = arguments[1]
    
    # construct our adb command
    adb_cmd = get_adb_cmd(options)
    
    # get the user SQLite client command
    sqlite_cmd = get_sqlite_client_cmd(options)
    
    # pull the database file from device
    fname = pull_db(adb_cmd, pkg, db)
    
    # start our watcher thread to write back db changes
    watcher = WatchFileThread(1, fname, pkg, db, adb_cmd)
    watcher.setDaemon(True)
    watcher.start()
    
    # launch the client application
    # TODO this is mac osx specific!
    proc = subprocess.Popen(['open', '-W', '-a', sqlite_cmd, fname], shell=False, stdout=subprocess.PIPE)
    
    # wait for the subprocess to return
    proc.wait()
    print 'Exiting ' + proc.returncode
    
    # clean up the temporary database file
    os.remove(fname)
    
def get_adb_cmd(options):
    if options.use_device:
        return 'adb -d'
    elif options.use_emulator:
        return 'adb -e'
    elif options.s != None:
        return 'adb -s ' + options.s
    else:
        return 'adb'

def get_sqlite_client_cmd(options):
    home = expanduser("~")
    settings = shelve.open(os.path.join(home,'.sqlook.settings'))
    if (not options.configure) and settings.has_key('cmd'):
        cmd = settings['cmd']
    else:
        cmd = raw_input('Enter your SQLite client program executable path: ')
        settings['cmd'] = cmd
    settings.close()
    return cmd   

def get_db_path(pkg, db):
    return '/data/data/' + pkg + '/databases/' + db

def pull_db(adb_cmd, pkg, db): 
    (f, dest) = tempfile.mkstemp()
    path = get_db_path(pkg, db)
    cmd = adb_cmd + ' pull ' + path + ' ' + dest
    print cmd
    subprocess.call(cmd, shell=True)
    return dest

def monitor_push_changes(fname, pkg, db, adb_cmd):
    last_modified = os.stat(fname).st_mtime
    while True:
        mod = os.stat(fname).st_mtime
        if (mod != last_modified):
            last_modified = mod
            print 'database changed'
            path = get_db_path(pkg, db)
            cmd = adb_cmd + ' push ' + fname + ' ' + path
            print cmd
            subprocess.call(cmd, shell=True)
        else:
            time.sleep(3)
    
if __name__ == "__main__":
    main()