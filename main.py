import logging
import os

import fire


VERSION = 1.0
NAME = "PyFileSplitter"
AUTHOR = "Rakesh Gariganti"


class Component(object):
    FORMAT = "%(message)s"
    log = None

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=self.FORMAT)
        self.log = logging.getLogger(__name__)

    def split(self, filename, parts):
        """
        Splits the given file into given parts
        """
        self.log.info("Splitting " + filename)
        if os.path.isfile(filename):
            self.log.info("File size: %s , splitting into %d parts" % (
                self._convert_bytes(os.path.getsize(filename)), parts))
        else:
            self.log.error("%s is not a file" % (filename))
            return 1
        size = os.path.getsize(filename)
        offset = (size/parts)
        with open(filename, 'rb') as f:
            buf_size = min(offset, (10*1024))
            for i in xrange(parts):
                pointer = 0
                with open(filename+"_"+str(i), 'w') as w:
                    while pointer < offset:
                        buf = f.read(buf_size)
                        w.write(buf)
                        pointer += buf_size
                    w.flush()
        self.log.info("Successfully split the file")

    def join(self, firstfilename):
        """
        Joins the files starting firstfilename into filename_joined
        """
        self.log.info("Joining " + firstfilename)
        filename = "".join(os.path.basename(firstfilename).split('_')[:-1])
        filename_without_ext = os.path.splitext(filename)[0] or ""
        extension = os.path.splitext(filename)[1] or ""
        dirlist = os.listdir(os.path.dirname(firstfilename))
        files = []
        for i in dirlist:
            if filename+"_" in i:
                files.append(i)
        files.sort()
        print files
        with open(filename_without_ext+"_joined"+extension, 'wb') as f:
            for i in files:
                s_filename = os.path.join(os.path.dirname(firstfilename), i)
                with open(s_filename, 'rb') as s:
                    s_size = os.path.getsize(s_filename)
                    buf_size = min(s_size, 10*1024)
                    pointer = 0
                    while pointer < s_size:
                        buf = s.read(buf_size)
                        f.write(buf)
                        pointer += buf_size
            f.flush()


    def _convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc till TBs
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0


if __name__ == "__main__":
    fire.Fire(Component)
