#!/usr/bin/env python

# Copyright (C) 2011 XiaoyanZhu
# Authors : Xiaoyan Zhu <xyxyzh@gmail.com>


import sys
import main

if __name__ == "__main__":
    try:
        retval = main.main (sys.argv[1:])
        sys.exit (retval)
    except KeyboardInterrupt:
        print "\n\nReceived Ctrl-C or other break signal. Exiting."
        sys.exit (0)
        

