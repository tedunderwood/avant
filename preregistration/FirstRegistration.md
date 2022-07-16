## Pre-registration for “Innovation, Publicity, and Change in Literary Culture”

Because book reviews are richly recorded in published indexes, scholars of literary history have an unusual opportunity to compare literature’s textual history (in the books themselves) to its social history (who talked about those books, what they said, how widely it circulated). We plan to use this opportunity to study the rewards for innovation, and the way those rewards are related to change across relatively long spans of time (roughly 80 years).

**Textual data:** We’ll take a random sample of English-language fiction from HathiTrust Digital Library, from 1890 to 2000, keeping the number of volumes per decade constant. We’ll form a model of 300 topics (basing this number on a previous experiment by Underwood, Kiley, Shang, and Vaisey). For volumes not present in this sample, we can extrapolate topic proportions using a topic inferencer created by MALLET.

**Review data:** We have extracted metadata about book reviews, and excerpts of the reviews, from the _Book Review Digest,_ 1917-1950. We also have reviews from _Kirkus,_ and metadata about reviews in little magazines from the _Comprehensive Index to English-Language Little Magazines._

**Other reception data:** We have lists of bestsellers, and Pulitzer-prize winning authors, and a retrospective representation of “the avant-garde” constructed using recent secondary sources.

Together, these sources about reception will allow us to study reception in ten different ways.



1. Books that got the most reviews.
2. Books about which most was written (adding up the length of each review).
3. Books more _positively_ reviewed, measured with the +/- codes included in the BRD, supplemented by a sentiment model trained on those +/- codes and used for reviews that are lacking a code.
4. Books reviewed by specific publications (we can itemize, say, 10 leading publications in the _BRD_).
5. Books widely reviewed by little magazines; this is one way of defining an "avant garde."
6. Books published by particularly prestigious publishers (e.g., Knopf).
7. Books that won Pulitzer/Nobel prizes.
8. Bestsellers (the top 10 per year from Unsworth’s list).
9. We can use principal component analysis on the whole reception matrix, and then “rotate” the components to find one that tends to distinguish wide-circulation venues (like newspapers) from little magazines. This is another way of defining “avant garde,” and arguably better than the absolute count in (5) at identifying books that get relatively _more_ attention in intellectual venues than in mass-market ones.
10. A retrospective definition of the early-20c avant-garde extracted from recent 21c secondary sources by David Bishop and Liza Senatorova.

**A. Analyzing the review data on its own.** Before we even look at the texts of books, it’s reasonable to ask whether these different measures are positively related to each other. Are best-selling (8) and prize-winning (7) books also written about a lot (2) or written about positively (3)?

And do the _evaluative judgments_ of different reviewing venues tend to correlate positively with each other?

Broadly, we do expect positive correlation, with the possible exception that our measure (9)—which will be defined by contrasting small-circulation venues to wide-circulation ones—may not correlate positively with the total volume of review discourse (2). Also there may be a few pairs of venues whose judgments do correlate negatively.

**B. Measuring novelty and precocity in the texts of books:** The measure of “novelty” in Barron et al. (2018) provides a simple way to measure innovation (as, say, KL divergence from the topic distributions of books in the last 25 years). We propose to use a 25-year window because Underwood and So (2020) found empirically, looking at a different collection of primarily nineteenth-century fiction, that patterns of this kind are legible within a window of 20 to 25 years.

We’ll similarly measure “transience” as KL divergence from the topic distributions of books in the next 25 years.

Precocity is novelty minus transience.

**Handling the generic heterogeneity of literary culture.** We know from previous experience that fiction is divided into genres with a lot of internal similarity. If we measure innovation and transience by looking at average similarity to the whole corpus, the books likely to have most “precocity” (forward shift on the timeline) could simply be books in genres that are growing. By definition, there will be more of those books in the future than the past.

But—at least arguably—this isn’t what most people mean by literary innovation. A book that introduces a new technique or theme to the mystery genre might be said to resemble the future even if the mystery genre as a whole is shrinking. Its innovation *relative to its genre* could be seen as more important than the fortunes of the genre as a whole. There is thus a strong argument for calculating innovation and transience within genres.

The challenge in doing this is that we don’t have genre tags for all books, and even if we did, it would be extremely difficult to reason about them across significant spans of time. Genres mutate, split, and fuse, and people have different perceptions about genre at different points in time. Asking whether China Miéville is in “the same genre” as JRR Tolkien would prejudge some of the questions about innovation and change we’re trying to answer.

The solution we’ll advance is to compare each book only to the 5% of volumes that most closely resemble it in any given year. This selection of volumes won’t necessarily coincide with the boundaries of a genre as defined by human readers. (Genres can be much smaller than 5% of the market.) But then again, we don’t know that works only influence works within the boundaries of a single genre. Comparing to the closest 5% is a reasonable way of measuring the innovation, or durability, of a work *relative to other works that could conceivably be seen as its precedents or inheritors*.

This solution was tested experimentally in Underwood and So 2020. In practice, measuring novelty and transience this way produces effects that are usually in the same direction as, and fairly close to, effects measured relative to all volumes. But since there is a theoretical justification for the more-tightly-focused measure, and it is arguably less vulnerable to noisy outliers, we will rely primarily on that. We will still, however, measure and discuss precocity measured with relation to the whole dataset.

**B1. Reception variables that correlate with novelty: **Equipped with these measures, we can ask which of the ten social locations itemized above tend to reward innovation. In other words, if we sort books using the total length of their reviews (in 2) or their tendency to be reviewed more in little magazines (in 9), which of those factors correlates most strongly with the novelty score we inferred from the book’s text?

Some of the reception variables we’re considering are binary (a book either is a bestseller or is not). Some of them are continuous (_how_ positively was a book reviewed?) But we can compare all the variables’ association with novelty by converting different measurements of effect size to Cohen’s _d._ We’ll focus on six measures of reception that are well attested and very different from each other: measures 2, 3, 7, 8, 9, and 10 above.

Each of the five of us ranked these variables by expected strength of association with novelty:

David: 9, 3, 2, 7, 8, 10

Liza: 10, 9, 7, 2, 8, 3

Ted: 9, 10, 8, 2, 7, 3

Wenyi: 10, 9, 2, 7, 3, 8

Yuerong: 10, 9, 8, 7, 2, 3

Averaging the rankings we get     	avg rank		rank after averaging

2: most written-about 		2.8			2

3: most positively reviewed		4.0			5

7: prizewinners			3.0			3

8: bestsellers				3.4			4

9: disproportionately in lit. mag.	0.6			0

10: later seen as avant-garde	1.2			1

Our predictions cluster pretty strongly. Kendall’s W is .50 and the mean Spearman correlation between individual rankers and the average is .76.

Whether the actual ranking is similar to this or quite different, our pre-registered prediction give us a way to discuss aspects of the ranking that diverge from expectation. We won’t of course be able to get a _p _value for that; the number of observations is too small.

**B2. How do rewards vary with a work’s degree of innovation?**

We can also infer a reward curve, like the one in Silver, Childress, et al (2022). For instance, what is the relation between innovation and the amount a book gets discussed (measured as total number of words mentioned in the _BRD_.)

It’s straightforward to predict that we will get the inverted U observed by other researchers. Very conventional or very eccentric books are probably discussed less than ones in the middle range.

Because Shang has extracted contemporary genre categories from the BRD, we can also plot a reward curve specifically for “mystery and detective fiction” or “historical fiction.” [Across the 30-odd year span of a single reference book, genre instability doesn’t pose the same problems we would experience if we tried to apply stable genre categories across the full 100-year span of our topic model.]

**B3. Transience. **We will graph innovation versus transience. Here, we expect the linear relationship observed by Barron et al (2018). On average, radical innovations tend not to persist (although there are important exceptions).

**B4. Reception variables that correlate with precocity. **We can also pose questions about _durable_ change. Since innovations tend to be transient, innovation is not at all the same thing as durable change. But if we subtract difference from the future from difference from the past, we can get a measure of a book’s durable innovation. To put it another way, this is a measure of overall displacement on the timeline: how much _more_ a book resembles the future than the past. We call this “precocity.”

Each of the five of us ranked the same six reception variables discussed above by expected strength of association with precocity (again this will be measured as Cohen’s _d_.)

David: 8, 7, 2, 10, 9, 3 

Liza: 7, 10, 8, 2 9, 3

Ted: 2, 10, 8, 7, 9, 3

Wenyi: 10, 7, 3, 2, 8, 9

Yuerong: 9, 8, 10, 7, 2, 3

Averaging the rankings we get     	avg rank		rank after averaging

2: most written-about 		2.4			3

3: most positively reviewed		4.4			5

7: prizewinners			1.6			1

8: bestsellers				1.8			2

9: disproportionately in lit. mag.	3.4			4

10: later seen as avant-garde	1.4			0

In general, the retrospective avant-garde moves down here, and prizewinners & bestsellers move up. Clustering is less strong; Kendall’s W is 0.4 and the mean Spearman correlation with the average is 0.68. We can use those measures to ask whether the results we actually get fall within, or exceed, our typical divergence from each other.

Interpreting precocity is tricky. It could tell us which venues of reception were best at _identifying_ incipient directions of change—or, possibly, which venues exerted most _influence_ on literary culture. Since our evidence is observational, it will be hard to separate those possibilities. But measurement of precocity is in any case analogous to Granger causation or predictive power. With a fairly simple transformation (adding up all the books reviewed in a particular venue) we could actually measure Granger causation if we wanted to — and we will.

**B5. Fifth question, about the relation between venues that reward innovation and those that predict precocity:** Are the venues of reception that tend to reward innovation also the venues that tend to predict directions of durable change? These patterns should correlate at least a little, since precocity is just novelty minus transience. But how much will they correlate? 

Our prediction is implicit in our preregistered answers to the two questions above. Spearman correlation between our average rankings for novelty and precocity is 0.31.

We could also graph different magazines and newspapers on a scatterplot where the vertical axis is relation to novelty and the horizontal axis relation to transience. The four quadrants of this graph would be

ahead of the times			innovative but faddish

predictable but durable                     behind the times      

**B6. Final question: are books _far_ ahead of their time rewarded by attention _at_ the time?**

We expect that yes, overall, most reception variables will correlate positively with precocity. But it’s not clear whether this will apply to extreme examples.

Does “precocity” relate to the total reviewing word-count (2) or review sentiment (3) with the inverted U-shaped curve found in Silver et al 2022? Or is it a more straightforward ascending line?
