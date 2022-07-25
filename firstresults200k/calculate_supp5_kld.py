# Calculate kld for chicago model

# This is based on previous calculate-kld scripts,
# but substantially revised in 2022 to address a different
# research question

import pandas as pd
import numpy as np
import random, sys, os
from multiprocessing import Pool
import kld_calc_worker_supp5 as kcw

numthreads = 10
# this can be changed if you like

measures2check = ['novelty', 'transience', 'resonance']
fractions2check = [1.0, 0.05]
timeradii2check = [25]
chunksize = 6000

meta = pd.read_csv('allmatchedbooks.tsv', sep = '\t')
data = pd.read_csv('topicdatastandardauths.tsv', sep = '\t', index_col = 'docid')

totalvols = meta.shape[0]

startposition = int(sys.argv[1])
endposition = startposition + chunksize
if endposition > totalvols:
    endposition = totalvols

print(startposition, endposition)

outputname = 'futuresurprise_' + str(startposition)
summaryfile = 'results/' + outputname + 'summary.tsv'
cossummaryfile = 'results/' + outputname + 'cossummary.tsv'
print(outputname)

segments = []
increment = ((endposition - startposition) // numthreads) + 1
for floor in range(startposition, endposition, increment):
    ceiling = floor + increment
    if ceiling > endposition:
        ceiling = endposition
    segments.append((floor, ceiling))

packages = []
for segment in segments:
    package = (meta, data, segment)
    packages.append(package)

print('Beginning multiprocessing.')
pool = Pool(processes = numthreads)

res = pool.map_async(kcw.get_kld_timelines, packages)
res.wait()
resultlist = res.get()
pool.close()
pool.join()
print('Multiprocessing concluded.')

for result in resultlist:
    novtrares4vols, cosnovtrares4vols = result

    if not os.path.isfile(summaryfile):
        with open(summaryfile, mode = 'w', encoding = 'utf-8') as f:
            outlist = ['docid']
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(measure + '_' + str(frac) + '_' + str(radius))
            header = '\t'.join(outlist) + '\n'
            f.write(header)


    if not os.path.isfile(cossummaryfile):
        with open(cossummaryfile, mode = 'w', encoding = 'utf-8') as f:
            outlist = ['docid']
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(measure + '_' + str(frac) + '_' + str(radius))
            header = '\t'.join(outlist) + '\n'
            f.write(header)


    with open(summaryfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, summary in novtrares4vols.items():
            outlist = [docid]
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(summary[measure][frac][radius])

            outline = '\t'.join([str(x) for x in outlist]) + '\n'
            f.write(outline)

    with open(cossummaryfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, summary in cosnovtrares4vols.items():
            outlist = [docid]
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(summary[measure][frac][radius])

            outline = '\t'.join([str(x) for x in outlist]) + '\n'
            f.write(outline)



