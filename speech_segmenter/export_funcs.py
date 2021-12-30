# encoding: utf-8

import pandas as pd
from pytextgrid.PraatTextGrid import PraatTextGrid, Interval, Tier

def seg2csv(lseg, fout=None):
    df = pd.DataFrame.from_records(lseg, columns=['labels', 'start', 'stop'])
    df.to_csv(fout, sep='\t', index=False)

def seg2textgrid(lseg, fout=None):
    tier = Tier(name='inaSpeechSegmenter')
    for label, start, stop in lseg:
        tier.append(Interval(start, stop, label))
    ptg = PraatTextGrid(xmin=lseg[0][1], xmax=lseg[-1][2])
    ptg.append(tier)
    ptg.save(fout)
