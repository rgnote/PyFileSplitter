# PyFileSplitter
A python tool to split a file(huge one) into smaller ones and re-join them. The motivation for this is that many email services have a upper limit on the attachments. Using this tool, a large file can be broken down into smaller ones and transferred them over email/whatever and re-join them at the other end.

# Usage   
Install the requirements with the command `pip install -r requirements.txt`   

Split a file   : `$ python Splitter.py split <<path to the file>> <<number of splits>>`   
Join the files : `$ python Splitter.py split <<path to the first split file>>`

