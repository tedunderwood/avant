import pandas as pd
import numpy as np
import random, sys, os
from scipy.stats import entropy
from scipy.spatial.distance import cosine

def get_kld_timelines(package):
    '''
    Calculates Kullback-Leibler divergence forward and back in time
    for a "segment" of rows in the metadata frame.

    Accepts as its argument a 3-tuple that should be:

    1 metadata DataFrame
    2 doc-topic proportions (data), as a DataFrame indexed by docid
    3 segment, a 2-tuple (startposition, endposition)

    Returns two objects:

    1 summary statistics listing the novelty, transience, and resonance
    averaged over different timespans and fractions. For def of novelty,
    transience and resonance see Barron et al. (2018).

    2 cosine-distance calculated backward and forward in time. This is not
    something we're necessarily planning to use in the experiment, but
    it's here to permit various kinds of sanity checking.
    '''

    meta, data, segment = package
    start, end = segment

    klds4vols = dict()
    novtrares4vols = dict()
    cosines4vols = dict()
    cosnovtrares4vols = dict()

    fractions2check = [1.0, 0.05]

    timeradii2check = [25]

    databyyear = dict()

    for year, df in data.groupby('firstpub'):
        databyyear[year] = df

    topicfields = ['t' + str(x) for x in range(200)]
    ctr = 0

    for idx in range(start, end):
        row = meta.loc[idx, : ]
        date = int(row['lowest_date'])
        doc1 = row['docid']
        author1 = row['standard_auth']

        ctr += 1
        if ctr % 20 == 1:
            print(ctr)

        if doc1 not in data.index:
            print(doc1, ' not found')
            continue

        basevector = np.array(data.loc[doc1, topicfields], dtype = np.float64)

        klds4year = dict()
        cosines4year = dict()

        floor = date - 25
        if floor < 1890:
            floor = 1890
        ceiling = date + 26
        if ceiling > 1976:
            ceiling = 1976

        # The asymmetry there is because the central date itself
        # will not be counted as part of either the forward range
        # (1851-1900, inclusive) or the backward range (1800-1849, inclusive).
        # Yet python by default would assume that 1850 is included looking
        # forward. If we exclude it on both sides, we have to add one
        # to the endpoint.

        # First let's just calculate KLD for individual documents,
        # and organize those calculations by year.

        for yr in range (floor, ceiling):
            offset = yr - date
            klds4year[offset] = []
            cosines4year[offset] = []

            thisyear = databyyear[yr]

            for idx2 in thisyear.index:
                author2 = thisyear.loc[idx2, 'standard_auth']

                if author1 == author2:
                    continue
                    # We don't check KLD btw vols with the same author.
    
                compvector = np.array(thisyear.loc[idx2, topicfields], dtype = np.float64)

                # this is a weird variant where the future is always surprising

                if offset < 0:
                    ent = entropy(basevector, compvector)
                elif offset >=0:
                    ent = entropy(compvector, basevector)

                # normally we do
                # ent = entropy(basevector, compvector)

                # NB the order of the two arguments for this function
                # matters! KL(a|b) ≠ KL(b|a).

                klds4year[offset].append(ent)

                cos = cosine(compvector, basevector)
                cosines4year[offset].append(cos)

        # Now to average kld by year. We will get different
        # averages when we consider different "fractions" of the range.

        avgkldbyyear = dict()
        avgcosbyyear = dict()

        for fraction in fractions2check:
            avgkldbyyear[fraction] = dict()
            avgcosbyyear[fraction] = dict()

        for i in range(-25, 26):
            if i in klds4year and len(klds4year[i]) > 0:
                thekl = klds4year[i]
                thekl.sort()
                for fraction in fractions2check:
                    cut = int(len(thekl) * fraction)
                    if cut < 1:
                        cut = 1
                    selectedgroup = thekl[0 : cut]
                    average = sum(selectedgroup) / len(selectedgroup)
                    avgkldbyyear[fraction][i] = average

            if i in cosines4year and len(cosines4year[i]) > 0:
                thecos = cosines4year[i]
                thecos.sort()
                for fraction in fractions2check:
                    cut = int(len(thecos) * fraction)
                    if cut < 1:
                        cut = 1
                    selectedgroup = thecos[0 : cut]
                    average = sum(selectedgroup) / len(selectedgroup)
                    avgcosbyyear[fraction][i] = average

        klds4vols[doc1] = avgkldbyyear
        cosines4vols[doc1] = avgcosbyyear

        # these arcs for different fractions will be written out in the "klds" files

        novelty = dict()
        transience = dict()
        resonance = dict()

        cosnovelty = dict()
        costransience = dict()
        cosresonance = dict()

        for fraction in fractions2check:
            novelty[fraction] = dict()
            transience[fraction] = dict()
            resonance[fraction] = dict()
            cosnovelty[fraction] = dict()
            costransience[fraction] = dict()
            cosresonance[fraction] = dict()

            for timeradius in timeradii2check:

                novsum = 0
                trasum = 0

                cosnovsum = 0
                costrasum = 0

                fullradius = True
                for i in range(-timeradius, 0):
                    if i in avgkldbyyear[fraction]:
                        novsum += avgkldbyyear[fraction][i]
                        cosnovsum += avgcosbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    novelty[fraction][timeradius] = novsum / timeradius
                    cosnovelty[fraction][timeradius] = cosnovsum / timeradius
                else:
                    novelty[fraction][timeradius] = np.nan
                    cosnovelty[fraction][timeradius] = np.nan

                fullradius = True
                for i in range(1, timeradius + 1):
                    if i in avgkldbyyear[fraction]:
                        trasum += avgkldbyyear[fraction][i]
                        costrasum += avgcosbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    transience[fraction][timeradius] = trasum / timeradius
                    costransience[fraction][timeradius] = costrasum / timeradius
                else:
                    transience[fraction][timeradius] = np.nan
                    costransience[fraction][timeradius] = np.nan

                resonance[fraction][timeradius] = novelty[fraction][timeradius] - transience[fraction][timeradius]

                cosresonance[fraction][timeradius] = cosnovelty[fraction][timeradius] - costransience[fraction][timeradius]

        novtrares4vols[doc1] = dict()
        cosnovtrares4vols[doc1] = dict()

        novtrares4vols[doc1]['novelty'] = novelty
        cosnovtrares4vols[doc1]['novelty'] = cosnovelty
        novtrares4vols[doc1]['transience'] = transience
        cosnovtrares4vols[doc1]['transience'] = costransience
        novtrares4vols[doc1]['resonance'] = resonance
        cosnovtrares4vols[doc1]['resonance'] = cosresonance

    return novtrares4vols, cosnovtrares4vols

