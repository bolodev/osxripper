# OSXRipper
OSXRipper is a tool to gather system and user information from OSX file systems. Currently it is supporting OSX versions 10.6 - 10.15 (Snow Leopard to Catalina).

[![Total alerts](https://img.shields.io/lgtm/alerts/g/exceljs/exceljs.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/exceljs/exceljs/alerts/)

#### Alternatives to OSXRipper

Apple Pattern of Life Lazy Output'er (APOLLO)
- https://github.com/mac4n6/APOLLO<br />

MAC APT
- https://github.com/ydkhatri/mac_apt<br />

OSX Auditor
- https://github.com/jipegit/OSXAuditor<br />

iParser
- http://az4n6.blogspot.co.uk/2012/08/automated-plist-parser.html<br />
- https://github.com/mdegrazia/iParser

Mac Plist Ripper
- https://bitbucket.org/chrishargreaves/mac_plist_ripper

If anyone knows of alternatives I would be more than happy to add them here.

#### Uses the CCL Forensics BPlist parser
https://github.com/cclgroupltd/ccl-bplist

__Prereqs__<br />
Assumes at least Python 3.4.3 is installed

#### Usage

python3 osxripper.py --help

__Options__<br />
-h, --help                       Show help message and exit<br />
-i DIRECTORY, --input=DIRECTORY  input directory<br />
-o DIRECTORY, --output=DIRECTORY output directory<br />
-l, --list List the available plugins<br />
-s, --summary                    Run Summary plugin only<br />

__Notes__<br />
N.B. if run on Linux and OSX systems user may have to escalate privileges to root<br />
N.B. the output directory must exist

__On OSX:__<br />
<em>sudo python3 osxripper.py -i /Volumes/my_mounted_volume -o /Users/username/Desktop/my_analysis</em><br />

__On Linux:__<br />
<em>sudo python3 osxripper.py -i /mnt/hfs_mount -o /home/username/my_analysis</em><br />
N.B. if kpartx used to mount the image the input path may be /media/...<br />

__On Windows:__<br />
<em>python.exe osxripper.py -i X:\extracted_files_root -o C:\Users\username\Desktop\my_analysis</em><br />

#### Plugin Development Guide
Check the Wiki page for getting started with plugin development or make use of existing plugins under __plugins/osx__
