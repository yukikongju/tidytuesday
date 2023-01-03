# Sentiment Analysis for Financial News

Before buying a stock, quantitative investors often perform a financial 
analysis on the company they want to invest in. By investigating a 
company balance sheet, one can have a pretty good grasp of the company 
instrinsic value. However, this analysis is often insufficient to predict 
stock price since a large body of investors invest with their emotions.
By performing sentiment analysis on financial news, our goal is to gain 
additional insights that may not be apparent with raw data alone.


## Leading Questions

1. Can we predict stock price and movement using financial news? 
   - How do investors feel about a particular stock? We would like to study 
     financial tweets
2. Can we use sentiment analysis to identify immerging issues in risk? 
   - Can we identify company that are caught up in fraud/scandals?
   - Can we identify economic trend and government regulations that may impact
     the company?

## Methodology

Our first task is to classify whether a financial news is positive, negative 
or neutral. To do so, we will first perform data cleaning and data augmentation 
to make sure that our data is general enough. Then, we will test several 
models using different preprocessing methods. 

Once we are able to classify the financial news, we are going to do a bit more 
investigation inside positive title and negative one. Since we won't have 
any label for this task, our risk analysis will be based mostly on clustering 
and dimension reduction in order to group similar news together. 

