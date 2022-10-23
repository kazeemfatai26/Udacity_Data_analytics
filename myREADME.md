# Prosper Loan Data Exploration
## by Kazeem Fatai Oabamiji


## Dataset

> The Prosper loan dataset, provided by Udacity, contains loan information froom different borrowers in United States of America. These data contains about a hundred thousand rows and 81 columns. With how much the columns are, we need a specific area of interest hence, we will need to specify the columns to investigate these area of interests.
This was done by adding the `usecols` parameter to the read_csv function. There were no duplicates in my data but it contains null values in some columns. Upon Visual assessment of my dataset in Microsoft Excel, I realised that my dataset variables has two categories which are records for data recorded after august 2009 and data recorded before 2009. ProsperScore and ProsperRating (Alpha) contain records applicable for data recorded after august 2009. 
Upon discovering this, i wrote a code to seperate out this records for their different date range. Also, the null values in the BorrowerState, Occupation and EmploymentStatus might not pose a threat to our data analysis as they will be replace with Not available for the different variables
And of course, null values in CurrentDeliquencies, AvailableBankCredit and TotalProsperLoans are all statistically correct as not all Borrowers have these variables recorded or available.
Hence, i wrote a function to replace the null values with "Not Available" for all the columns in other to be able to categorize records for which i do not have their records


## Summary of Findings
> I wanted to find out factors that affect the loan status, characteristics of borrowers with high loan amount and how the loan amount is related with its interest rate, that is, does a higher loan amount translate to a better loan in terms of interest rate?
Hence, the main features of interest in my dataset are those features that helped to effectively find out the answer to the questions listed above.
For the Univariate exploration, i used seaborn displot and matplotlib's `plt.hist()` for non-categorical variables and seaborn countplot for categorical variables, i investigated the distribution of the data set. Interestingly, about 50% of the loans are currently on with 30% completed. 
I also noticed that most of the loans do not have the best risk score and rating by Prosper but an higher percentage of the loans were considered low risk loans given by their ProsperScore.
About 80% of the loans have a loan term of 3 years with the remaining percent shared between the 5-Year and 1-year term.
There was a need to perform log transformations on the `StatedMonthlyIncome`  and `AvailableBankCardCredit` column in order to properly and effectively show the distributions of the values across the borrowers. 
the statedMonthlyIncome and Available Bank Card credit showed outliers in the values ,which affected distribution, when i plotted an histogrm. I had to perform a log transformation to the data in order to be able to properly plot the data on a histogram. I also had to reorganize the `LoanStaus` categorical variables. The past due loans were summed up into one category to reduce redundancy.

>From the Bivariate exploration, the interest rate is not entierly based on the Amount of the loan. also, i discovered that for each category of loanStatus,its frequency among the loans does not determine the average loan amount taken by that category as categories with more loans had even lower average loan amount taken. 
furthermore,I noticed that there is a decrease in the median of the interest rate as the risk scores and ratings improve. For the Loan term, the loan term of one year have most of their loans have been completed already. for the one year, the completed loans form the highest percentage amongst other loanStatus category at over 90%.
It also looks like for completed loans, not a lot of money have being paid on average but loans with their final payment in progress also happens to have a high average Loan amount, second to the average loan amount from loans that are currently on.
In the multivariate section, the focus was on the effect of the Prosper Rating on the relationship between the interest rate and the loan amount taken. Here, i discovered that the better the rating, the lower the interest rate and vice versa.
For my explanatory visualizations slides, i aim to tell the story of how the loan status, term, amount and the prosper rating relates with each other.


## Key Insights for Presentation

> About half of the loans are currently on with only about 30% completed. Only a few loans have the best risk score but a good percentage of all the loans have good risk rating. Most of the loans have their length to be 3 years. The variables listed above are the focus of this presentation and interestingly, have a relationhip with the interest rate and loan amount. The median of the interest rate decreases as the prosper score improves and lower interest rates are associated with Loans with better Prosper Ratings. This indicates the close relationship between the prosper score and prosper rating. A high percentage of loans whose term is 1 year are completed already. The presentation focuses on how the Prosper Rating affects the interest rate of the loans for different loan amounts.


