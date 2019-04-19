# Mathematical Concepts
> This document includes definitions, terms, theories in probability, data science, and statistics



## Contents

* [Statistics](#stats)
* [Probability](#prob)



<br/><a name="stats"></a>
## Statistics


### Definitions

* Standard Deviation (sd)
  - how wide data is spreading
  - https://en.wikipedia.org/wiki/Wiki
  - numpy.std

* Variance (var)
  - sd**2

* Normal Distribution
  - most common distribution in statistics
  - eg. the heights of a large group of people
  - symmetic with a central peek
  - the peek move left and right with the mean
  - the higher the sd, the more spreaded the data is
  - numpy.ramdom.normal(mean, sd, size)
  - 6% of samples will fall between +/- sd of the mean; 9% of samples will fall between +/- 2 stadard sd of the mean; 99.7% of sampels will fall between +/- 3 sd of the mean

* Binomial Distribution
  - eg. a basketball player makes 30% of his free throughs, he shoots 10 times, what is the possibility that he makes exactly 2?
  - https://en.wikipedia.org/wiki/Binomial_distribution
  - numpy,random.binomial(num_of_trails, p_of_success, size)

* Hypothesis Test
  - What si the probability that the two population means are the same and that the observed difference is the result of chance
  - **null hypothesis**: a statment that the observed difference is the result of chance

* Type I and Type II Errors:
  - Type I: **"false positive"**, the null hypothesis is rejected even though it is ture, eg. I think the are difference but actrually they are not
  - Type II: **"false negative"**, the null hypothesis is accepted even though it is wrong, eg. I think they are same but this are actually different

* P-Value
  - how confident we acan ve in the result
  - p-value is the probability that we yield the observed statistics under teh assuption that the null hypothesis is true
  - high threshold is more like to get false positive
  - generally we want our p-value of less than 0.05

* 1 Sample T-Tesing
  - univariate T-test
  - compares a sample mean to a hypothetiacal population eman
  - "what is the probability that the sample came from a distibution with the desired mean?"
  - **null hypothesis"**: no significant difference, "The set of samples belongs to a population with the target mean."
  - scipy: tstat, pval = ttest_1samp(example_distribution, expected_mean)
  - if pval > 0.05, we accept the null hypothesis, emaning that the difference between sample mean and expected mean is just a result of chance, our sample still have a mean of expected mean
  - if pval < 0.05, we reject the null hypothesis, meaning that the difference between them is not by chance, therefore we say the mean of sampel is not 30, the sample mean is a correct result

* 2 Sample Testing
  - eg. average amout of time spent per visitor to a website was 25 mins last, it is 28 minute this week, did teh average time sppet per vistor change? or it is just natural fluctuations
  - compares two set of data, which are both approximatly normally distributed
  - scipy: t_stats, pval = ttest_ind(data1, data2)

* ANOVA Testing
  - ANOVA tests the null hypothesis that all datasets have the same mean
  - scipy: fstat, pval = f_onelay(data1, data2, data3)

* Tueky's Range Test
  - determeine the difference between datasets
  - statsmodel: pairwise_tukeyhsd
  - concatenation = numpy.concatenate(data1, data2, data3)
  - labels = ['data1'] * len(data1) + ['data2'] * len(data2) = ['data3'] * len(data3)
  - tukey_results = pairwise_tukeyhsd(concatenation, labels, 0.05)

* Binomial Test
  - eg. compare the actrual number of heads from 1000 flips, of a weigted coint to the expected number of heads
  - scipy: binom_test(actual_value, n=1000, p=0.5)

* Chi Square Test
  - eg. An A/B test where half of users were shown a green submit button and the other half were shown a purple submit nutton. Which one group more likely to click the submit button?
  - Men and women were both given a survey asking "which of the folowing three prodects is your favorite" Did the men and women have significantly differt preferences?
  - scipy.stats: X = [[30, 10], [35, 5], [28, 12], [20, 20]]
  - chi2, pval, dof, expected = chi2_contingency(X)

### Terms

* Skewness
  - The datas is unbalanced to left or right
  - negative (left) skewed: the peek is on the right of graph, mean is smaller than median, or to the left of median
  - possitive (right) skewed: the peek is on the left of graph, mean is larger than median, or to the right of median

* Sample
  - a subset of a population
  - eg. the amount of sales of a day in a month


### Theories

* Central Limit Theorem
  - If we have a large enough sample size, all of our sample means will be sufficiently close to the population mean.

* Assumptions of Numerical Hypothesis Tests
  - sampels should each be nomally distruted
  - sd of each group should be equal
  - sampels must be independent


<br/><a name="prob"></a>
## Probability


### Definations

* Probability Desity Function (pdf)
  - the probability that a continous random variable is in between two certain values
  - eg. the amount of rainning tomorrow Y
  - pdf(a, b, Y) = P(a <= Y <= b)
  - https://en.wikipedia.org/wiki/Probability_density_function

* Probability Mass Function (pmf)
  - the probability that a discrete random variable is exactly some value
  - eg. the number of tails when tossing 3 coins
  - pmf(x) = P(X=x)
  - https://en.wikipedia.org/wiki/Probability_mass_function