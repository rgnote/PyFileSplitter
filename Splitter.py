import logging
import os

import fire


VERSION = 1.0
NAME = "PyFileSplitter"
AUTHOR = "Rakesh Gariganti"


class Splitter(object):
    FORMAT = "%(levelname)s: %(message)s"
    MAX_BUF_SIZE = 50 * 1024
    log = None

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=self.FORMAT)
        self.log = logging.getLogger(NAME)

    def split(self, filepath, parts):
        """
        Splits the given file into given parts
        """
        self.log.info("Splitting " + filepath)
        if os.path.isfile(filepath):
            self.log.info("File size: %s , splitting into %d parts" % (
                os.path.getsize(filepath), parts))
        else:
            self.log.error("%s is not a file" % (filepath))
            return 1
        size = os.path.getsize(filepath)
        offset = (size / parts)
        g_c = 0
        self.log.info("Each splitted file's size : " + str(offset))
        with open(filepath, 'rb') as f:
            buf_size = min(offset, self.MAX_BUF_SIZE)
            self.log.info("Buffer size : " + str(buf_size))
            for i in xrange(parts):
                self.log.info("Writing part-%d" % (i + 1))
                pointer = 0
                with open(filepath + "_" + str(i + 1), 'w') as w:
                    while pointer < offset:
                        if (offset - pointer) < buf_size:
                            buf = f.read(offset - pointer)
                        else:
                            buf = f.read(buf_size)
                        w.write(buf)
                        pointer += len(buf)
                    self.log.info("Written %d bytes" % (pointer))
                    g_c += pointer
                    w.flush()
                print
        self.log.info("Written " + str(g_c))
        self.log.info("Successfully split the file")

    def join(self, firstfilepath):
        """
        Joins the files starting with firstfile into filename_joined
        """
        self.log.info("Joining " + firstfilepath)
        filename = "".join(os.path.basename(firstfilepath).split('_')[:-1])
        filename_without_ext = os.path.splitext(filename)[0] or ""
        extension = os.path.splitext(filename)[1] or ""
        dirlist = os.listdir(os.path.dirname(firstfilepath))
        last_file_index = 1
        for i in dirlist:
            if filename + "_" in i:
                file_index = int(i.split("_")[-1])
                if file_index > last_file_index:
                    last_file_index = file_index
        self.log.info(
            "Total files found in the given directory: " + str(last_file_index))
        destfilename = filename_without_ext + "_joined" + extension
        g_c = 0
        with open(destfilename, 'wb') as f:
            self.log.info("Writting to " + destfilename)
            for i in xrange(1, last_file_index+1):
                this_file = filename + "_" + str(i)
                os_filename = os.path.join(
                    os.path.dirname(firstfilepath), this_file)
                self.log.info("Reading from " + this_file)
                with open(os_filename, 'rb') as s:
                    s_size = os.path.getsize(os_filename)
                    self.log.info("File size of " + str(i) +
                                  " is : " + str(s_size))
                    buf_size = min(s_size, self.MAX_BUF_SIZE)
                    pointer = 0
                    while pointer < s_size:
                        if (s_size - pointer) < buf_size:
                            buf = s.read(s_size - pointer)
                        else:
                            buf = s.read(buf_size)
                        f.write(buf)
                        pointer += len(buf)
                    g_c += pointer
                print
            self.log.info("Written %d bytes to %s" % (g_c, destfilename))
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
    fire.Fire(Splitter)
