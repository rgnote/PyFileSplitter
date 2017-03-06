import logging
import os

import fire


PROJECT_VERSION = 1.0
PROJECT_NAME = "PyFileSplitter"
PROJECT_AUTHOR = "Rakesh Gariganti"


class Splitter(object):
    LOG_FORMAT = "%(levelname)s: %(message)s"
    MAX_BUF_SIZE = 50 * 1024
    log = None

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format=self.LOG_FORMAT)
        self.log = logging.getLogger(PROJECT_NAME)

    def split(self, file_path, num_parts):
        """
        Splits the given file into given num_parts
        """
        self.log.info("Splitting " + file_path)
        if os.path.isfile(file_path):
            self.log.info("File size: %d bytes, splitting into %d num_parts" % (
                os.path.getsize(file_path), num_parts))
        else:
            self.log.error("%s is not a file" % (file_path))
            return 1
        size = os.path.getsize(file_path)
        offset = (size / num_parts)
        bytes_written = 0
        self.log.info("Each splitted file's size : " + str(offset))
        with open(file_path, 'rb') as source_file:
            buf_size = min(offset, self.MAX_BUF_SIZE)
            self.log.info("Buffer size : " + str(buf_size))
            for each_part in xrange(num_parts):
                self.log.info("Writing part-%d" % (each_part + 1))
                read_pointer = 0
                with open(file_path + "_" + str(each_part + 1), 'w') as dest_file:
                    while read_pointer < offset:
                        if (offset - read_pointer) < buf_size:
                            buf = source_file.read(offset - read_pointer)
                        else:
                            buf = source_file.read(buf_size)
                        dest_file.write(buf)
                        read_pointer += len(buf)
                    self.log.info("Written %d bytes" % (read_pointer))
                    bytes_written += read_pointer
                    dest_file.flush()
        self.log.info("Written " + str(bytes_written))
        self.log.info("Successfully split the file")

    def join(self, first_file_path):
        """
        Joins the files starting with firstfile into filename_joined
        """
        self.log.info("Joining " + first_file_path)
        file_name = "".join(os.path.basename(first_file_path).split('_')[:-1])
        filename_without_ext = os.path.splitext(file_name)[0] or ""
        extension = os.path.splitext(file_name)[1] or ""
        dir_name = os.path.dirname(first_file_path)
        if dir_name == "":
            dir_name = "./"
        dirlist = os.listdir(dir_name)
        last_file_index = 1
        for i in dirlist:
            if file_name + "_" in i:
                file_index = int(i.split("_")[-1])
                if file_index > last_file_index:
                    last_file_index = file_index
        self.log.info(
            "Total files found in the given directory: " + str(last_file_index))
        dest_file_name = filename_without_ext + "_joined" + extension
        bytes_written = 0
        with open(dest_file_name, 'wb') as dest_file:
            self.log.info("Writting to " + dest_file_name)
            for i in xrange(1, last_file_index + 1):
                source_file_name = file_name + "_" + str(i)
                source_file_path = os.path.join(
                    os.path.dirname(first_file_path), source_file_name)
                self.log.info("Reading from " + source_file_path)
                with open(source_file_path, 'rb') as source_file:
                    source_file_size = os.path.getsize(source_file_path)
                    self.log.info("File size of " + source_file_path +
                                  " is : " + str(source_file_size))
                    buf_size = min(source_file_size, self.MAX_BUF_SIZE)
                    read_pointer = 0
                    while read_pointer < source_file_size:
                        if (source_file_size - read_pointer) < buf_size:
                            buf = source_file.read(
                                source_file_size - read_pointer)
                        else:
                            buf = source_file.read(buf_size)
                        dest_file.write(buf)
                        read_pointer += len(buf)
                    bytes_written += read_pointer
            self.log.info("Written %d bytes to %s" %
                          (bytes_written, dest_file_name))
            dest_file.flush()

if __name__ == "__main__":
    fire.Fire(Splitter)
