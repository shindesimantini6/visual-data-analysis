# Visual Data Analysis

Application of visual data analysis on Gapminder dataset of fertility rates and income per person vs life expectancy for the world.

The project involves creating a visual of three parameters correlating with each other, i.e. the income per person, fertility rates, life expectancy and population. The visual is created for data from 1960 to 2022. 

The five datasets have been melted, merged and cleaned for visualisations. 

# Problems tackled

In the initial analysis, the size of the population bubbles remained static over the years (i.e. 1960 to 2022), which is obviously not true. To solve this, I calculated a factor to be multiplied to the range of sizes parameter while creating the chart. The factor was calculated by taking the mean of the population for the particular year to the mean of the total population for all years.

# Life Expectancy vs Fertility rates

# Life Expectancy vs Fertility rates vs income per person 
![Alt text](final_gif_with_income_png.gif)

# Requirements

Python 3.9.0
imageio.v2
Pandas
