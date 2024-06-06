# EDA and Model Development for Predicting High Traffic Recipes

This repository contains the code and resources used for the DataCamp Data Scientist certification exam project. 
The project focuses on developing a model to predict which recipes will generate high traffic on a recipe website. The analysis and model development process is documented in detail below.

## Project Overview
The primary goal of this project is to create a data-driven model that predicts high traffic recipes to drive more subscribers to the website. 
The project addresses the current problem where the product manager selects daily homepage recipes based on personal preference, leading to variable website traffic. 
By leveraging historical data, we aim to develop a model that can reliably predict high traffic recipes.

## Table of Contents
* [Data Validation](#validation)
* [Data Exploration](#exploration)
* [Model Deployment and Evaluation](#model)
* [How to Help the Business](#help)

<a name="validation"></a>
## Data Validation
To ensure the quality and robustness of the data used for training the machine learning model, we performed the following steps:

* __Removing duplicates:__ Ensured that each recipe record is unique.
* __Checking and adjusting data types:__ Verified the correctness of data types for each column.
* __Handling null values:__ Addressed any missing values to avoid data quality issues.
* __The dataset contains 8 main variables:__
 * __recipe:__ Unique identifier of the recipe (numeric)
 * __calories:__ Number of calories (numeric)
 * __carbohydrate:__ Amount of carbohydrates in grams (numeric)
 * __sugar:__ Amount of sugar in grams (numeric)
 * __protein:__ Amount of proteins in grams (numeric)
 * __category:__ Type of recipe (character)
 * __servings:__ Number of servings (numeric)
 * __high_traffic:__ Indicates if the traffic was high (character)

<a name="exploration"></a>
## Data Exploration
We conducted exploratory data analysis (EDA) to understand the distribution and relationships within the data:

The four numerical columns (calories, carbohydrate, sugar, and protein) are right-skewed with outliers.
* Boxplots were used to identify outliers, and the median was chosen as a robust metric for central tendency.
* We applied the Yeo-Johnson transformation to normalize the data distributions.
* We also examined the impact of recipe categories on traffic:

Top categories with high traffic:
* Vegetable: 99% high traffic
* Potato: 94% high traffic
* Pork: 91% high traffic

<a name="model"></a>
## Model Deployment and Evaluation
### Model Selection
We approached this as a binary classification problem to predict whether a recipe will have high traffic. The following models were considered:
* Logistic Regression
* Decision Tree
* Random Forest
* Support Vector Machines (SVM)

Chosen Models:
* Logistic Regression: Used as the baseline model.
* Support Vector Machines (SVM): Used for comparison.

### Model Evaluation
We aimed for an accuracy of over 80% in predicting high traffic recipes. Recall was chosen as the primary metric to maximize the detection of high-traffic recipes.

* Logistic Regression:
Achieved recall over 80%.
No overfitting observed.
Slight elevation in test results indicating limited data presence.

* Support Vector Machines (SVM):
Indicated underfitting in the training set.
Recall value was 1, suggesting all elements were labeled as high traffic, which is not desirable.

<a name="help"></a>
## How to Help the Business
The main objective is to maximize website traffic by accurately predicting high-traffic recipes. Using recall as a metric ensures we minimize missed opportunities for high traffic.

* Recommendations:
  * Enhance data collection practices to improve model accuracy and reliability.
  * Implement a real-time analytics dashboard to monitor recipe performance and aid in quick, data-driven decision-making.

