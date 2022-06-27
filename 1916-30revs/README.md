First release of Book Review Digest data
========================================

This folder contains fifteen tab-separated tables that report data about fiction book reviews excerpted in the Book Review Digest. These files have one row for each *review*.

It also contains aggregated_by_book.tsv, which has book-level summary information (one row for each *book*), and publisher_analysis.py, which produced the aggregated_by_book summary.

what's in the tables
--------------------

The tables contain factual bibliographic data about the books reviewed, and the magazines reviewing them. For instance, the publisher, the number of words in each review, etc. They also contain bags-of-words used in each review excerpt, sorted alphabetically--but not sequential text. They also contain the *average* sentiment value of reviews for a book, but they don't report the actual review sentiment (expressed as plusses or minuses) at a per-review level. Finally, they don't include subject headings or index headings from the BRD, except insofar as those may sometimes accidentally (and very rarely)get fused with the book publisher or review text. On manual inspection I don't find cases of this happening, and you'll see that the code has been written to prevent it. But it's a conceivable error that could sometimes, rarely, happen.

specific columns
----------------

Each table has these columns

bookauthor -- who wrote the book reviewed
booktitle -- its title
brdpage -- the page location in BRD where it was reviewed
price -- of the book in dollars
publisher -- of the book; sometimes also trailing words from the title, or a price that hasn't been correctly parsed
publication -- that reviewed the book, or "summary" for an initial unattributed summary
citation -- page numbers and word counts of the book review
quote -- a bag of words, sorted alphabetically, taken from the review excerpt
wordcount -- the total number of words in reviews of this book, inferred from the word counts in the "citation" column
avgsentiment -- a numeric representation of the average +/- sentiment of reviews for this book, where - is 1, -+ is 2, +- is 3, and + is 4. Missing data is imputed to the mean for this volume of the BRD.
bookindex -- keyed to a book-level list of fiction volumes reviewed
numreviewswithsent -- how many of the reviews for this book had +/- values present
numreviewsofbk -- simply how many reviews were there; this will be equal to the rowcount for bookindex
authtitlefromindex -- we inferred this was fiction by matching to the volume index; this is the author and title spelling present there, in case we have doubts about the correctness of the "fiction" inference
matchcloseness -- a numeric reflection of the quality of the author-title fuzzy match; we might use this to identify dubious volumes

the code used
-------------

select_fiction_reviews.py is the script that actually produced these files; you can inspect it to see what was selected or omitted. It's working from other files present in the capsule; parsing the reviews, and the index; pairing the two to identify fiction volumes, etc is a long process.
