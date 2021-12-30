# -*- coding: utf-8 -*-


import Pyro4
import sys

if __name__ == '__main__':
    uri = sys.argv[1]
    csvfname = sys.argv[2]

    jobserver = Pyro4.Proxy(uri)

    ret = jobserver.set_jobs(csvfname)
    print(ret)
