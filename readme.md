# Every Season is Beerable
# Abstract
This project aims mainly at studying the beer trends based on seasons. In fact, each individual may tend to consume different beers based on its mood or feeling influenced by the season. A study of a high variety of beers may help to see if some beers have variable success rate accross the year or inversely have a constant consumption rate. After identifying how some specific types of beers are consumed at different times of the year, we could dig further those tendencies to see if they also varies accross the years. This would helps to identify if the beer success at some time was ephemere or inversely anchored in the consumption habits of beer drinkers. Seeing this seasonal variability, we will investigate the comment's enthusiasm for a beer accross season and see if this correlates with the seasonal cyles observed. Finally, we will see how the beweries take advantage of those cyclic consumption rates in their beer proposal.


# Research Questions
## `Task 1:` Season-dependent beer (e.g: beer almost exclusively drank during one season)
- Is a beer more incline to be consumed at one time of the year and if so, at which time of the year ?

## `Task 2:` Ephemere and long-lasting season dependent beers
- Do some beers are highly rated during only one season during one specific year and then are forgotten in the next years ?

## `Task 3:` Features of season-dependent beers
- Which characteristics such as the aroma, the taste, ... of a beer makes it to be more a spring-beer or a fall-beer ?

## `Task 4:` Drinking at the wrong season 
- Is there a shift of the season-dependent beer ratings if it is not tasted during the adequate period ?

## `Task 5:` Dataset Quality Enhancement
### Professional vs Occasional drinker
- The dataset contains a high number of user of different profiles. We identified 2 main types of users:
    - `A:` The professional rater, he rates a high number of beers, accross a wide spectrum of beer style throughout the year, he might not taste beers accordingly to his preferences or what fits the current season
    - `B:` The occasional rater, he rates a small number of beers, spontaneously testing beers he wants to
- Isolate group `A` from `B` and re-run all the analysis to see wether or not the seasonable beer pattern is accentuated without the group `B`

### Elude ratings from south hemipshere
- Having in the same dataset ratings from south and north hemisphere might lead to self-canceling of the season cycles. One could either delete ratings from the S.H or offset by 6 months the time of S.H ratings

## `Task 6:` Sentimental analysis
- Compute the "distance" between the actual rating's grade and the inferred grade from the textual content (using natural language processing tools like [Hugging Face](https://huggingface.co/tasks/text-classification) or the proposed method from paper ...)
- Perform this test for group `A` and `B` on seasonal and non-seasonal beers
- Will users from group `B` be more precise in their ratings than group `A` for seasonal beers, is it also the case for non-seasonal beers ?

## `Task 7:` Seasonal beers oriented breweries
- Identify wether or not breweries focus more on seasonal beers than others
- If so, what are their characteristics

# Proposed additional datasets (if any) 
- No additional dataset to provide, complete dataset !

# Methods
- For each ratings, the location was added with a union operation between the ratings and the users dataset (based on user_id). The dates were also discretised in months and years in order to perfom a monthly analysis. Ratings with missing abv index were completed with the average index of the corresponding beer style. Ratings with missing location, date or beer style were dropped from the dataset.

- After cleaning the data, the two sites RateBeer and BeerAdvocate were compared. To identify the most implicated countries, 
the contribution of different countries in the % of ratings was plotted in Beer Advocate and RateBeer and those percentages were mapped.
For the seasonal variability of ratings, we firstly identified the most rated style in the world. Then, we compared the weighting of the ratings for each sites. This was done by performing a LinearRegression on both sites' data and taking as features the appearance, aroma, palate, taste and overall and as output the rating.

- The datasets were now ready to be analysed more in depth. The monthly rating number was plotted to have an idea of the overall rating dynamic that could influence the micro analysis to be done afterwards. The monthly distribution of the IPA, Pilsner and Belgian Strong Ale reviews was studied to observe the first patterns of season-dependency.

- Then with statisticals analysis such as t-test we will analyse which feature such as alcool degree, appearance, aroma, palate, taste, or even users' location have the highest impact on the seasonality of the beer. This will help us to identify which kind
of beers are prefered at which time of the year. Then, a splitting of the dataset into clients types A and B will be conducted and similar
analysis as before will be performed to see if we really have at lesast 2 discernable categories of consummers in the batch of the users.

- To complement the findings, a sentimental analysis on the comments will be performed to see if the ratings and the comments' postivity correlate strongly to each others and if they also vary with the seasons. This would indicate a clear change of mood from the users in addition to their rating frequency. The sentimental analysis of the comments will be performed using an already trained machine learning classifier that could be downloaded on the site : https://huggingface.co/tasks/text-classification. This classifier assigns a grade based on the degree of positivity of the comment.

- Finally for a global view, we will inspect how the breweries proposal vary and converge to specific beers using t-test as well. This could show the beweries offer's variability depending on their targetted clients.

# Timeline and organization within the team

```mermaid
gantt
    title ChatChuiPT
    dateFormat MM-DD
	axisFormat %m-%d

	section Task 1,2
		Identify S.B (ephemere and long term)   :t1, 11-17, 2w
	section Task 3
		Categories S.B based on their features  :t3, after t1 h2, 1w
    section Task 4
		Wrong season ratings (harsher ratings?) :after t1 h2, 1w
	section Task 5
		Dataset Quality Enhancement             :t51, after t1 h2, 1w
		Rerun analysis with enhanced dataset    :t52, after t51, 1w
	section Task 6
		Sentimental analysis                    :after t1 h2, 1w
	section Task 7 
		Seasonal beers oriented breweries       :after t1 h2, 1w
	section H2
		Homework 2                              :h2, 11-17, 2w
	section Report
		Website, redaction                      :after t1, 2w
```
S.B: Seasonal Beer
