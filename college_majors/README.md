# College Majors

A demographic and economical analysis on US college majors graduate in 2021


## Leading Questions

1. What are the difference between STEM and non-STEM majors? 
   - Are there really more man in STEM?
   - Do STEM majors make more money than non-STEM majors? Starting Salary? 
   - Are they more employable? What is the average time it takes by major 
     to find employment? What is the employment rate?
   - Do non-STEM majors actually use their degrees?
   - What is the average amount of debth carried by graduates?
   - Are non-STEM major easier to get in that STEM majors?
2. Is the pay gap even real? 
   - Do women make less money than man within their respective field?
   - What are the best predictors when predicting wage? When predicting 
     employment?
   - What majors are dominated by men? woman?
3. Which major is the best? 
   - Which major pay the most?
   - Which major has the most employment rate?


## Methodology

To determine whether there is a significative
difference between two groups (or more), we will perform hypothesis testing 
using Bonferonni correction. If it is adequate, we will also perform 
more advanced hypothesis testing on several variables, namely using rectangle 
and ellipsoid hypothesis testing.

To determine the best predictors for a response variable, we will try to fit 
a multiple linear regression onto the data. We will first verify that all 
linear regression assumptions are met by analysing the standardized residuals.
If one of the assumption isn't met, we will a Box-Cox plot to find the best 
transformation we can use to allow us to model the data using a linear regression.
If the data isn't linear, we will try to add some quadratic terms to get rid 
of non-linearity problem.
We will then check whether there is any outliers making our model less accurate.
We will find these outliers using 3 methods: (1) using the 1.5 IQR method, 
(2) using the jacknive residual method and (3) using the Cook's distance method.



## Conclusion


