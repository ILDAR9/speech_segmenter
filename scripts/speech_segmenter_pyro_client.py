# -*- coding: utf-8 -*-


import Pyro4
import sys
import os
import socket

from speech_segmenter import Segmenter


if __name__ == '__main__':
    dname = os.path.dirname(os.path.realpath(__file__))

    hostname = socket.gethostname()

    uri = sys.argv[1]
    jobserver = Pyro4.Proxy(uri)

    ret = -1
    outname = 'init'
    
    # batch size set at 1024. Use lower values with small gpus
    g = Segmenter(batch_size=1024)
    
    while True:
        lsrc, ldst = jobserver.get_njobs('%s %s' % (hostname, ret))
            
        print(lsrc, ldst)
        if len(lsrc) == 0:
            print('job list finished')
            break
        
        ret =  g.batch_process(lsrc, ldst, skipifexist=True, nbtry=3)
