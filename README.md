SQLook
======

SQLook is a simple Python program that helps you examine an Android application's SQLite database running on an emulator or compatible device using a 3rd party SQLite client application.   

<img src="https://raw.github.com/jgilfelt/SQLook/master/screenshot.png"/>

SQLook is intended as an alternative to the adb `sqlite3` command prompt for developers who prefer more graphical database tools. It assumes databases are managed and stored in the standard location defined by Android's `SQLiteOpenHelper` class. All the normal security restrictions for database and file access still apply here - this tool will only really work with an emulator or rooted device.

A worker thread monitors the database file for client changes and will immediately push the modified databse file back to the device. Modifications made to the database by the app will not be refelected in the SQLite client until it is closed and SQLook is run again. Such changes may be lost if modifications were also made in the client.

### Note: currently Mac OSX support only - pull requests welcome

BYO client
----------

SQLook requires a 3rd party SQLite database client. You will be prompted to configure its executable path the first time you run this program. Here are a few that are available:

### Mac OSX

- Base http://menial.co.uk/base/ (commercial)
- SQLite Database Browser http://sqlitebrowser.sourceforge.net/ (free)

Install
-------

    chmod a+x src/sqlook 
    sudo cp src/sqlook src/sqlook.py /usr/bin

Usage
-----

    Usage: sqlook [options] package_name database_file
    
    Examine an Android SQLite database using a client application of your choice
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -d                    directs command to the only connected USB device,
                            returns an error if more than one USB device is
                            present.
      -e                    directs command to the only running emulator, returns
                            an error if more than one emulator is running.
      -s <specific device>  directs command to the device or emulator with the
                            given serial number or qualifier. Overrides
                            ANDROID_SERIAL environment variable.
      -c, --configure       configure the default SQLite client.

Credits
-------

Author: [Jeff Gilfelt](https://github.com/jgilfelt).


License
-------

    Copyright 2013 readyState Software Limited

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
