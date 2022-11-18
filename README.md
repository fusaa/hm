# Summary

I did this ETL(Extraction, Transform, Load) while learning. It scraps the American version of the H&M website jeans department. I started using Beautiful Soup initially; however, the website had dynamic content that relied on user behaviour to display information. So I had to change in the middle of the progress to Selenium.

I divided the project into three parts:

Extraction - [job_one.py](https://github.com/fusaa/hm/blob/main/job_one.py) - contains functions that extract different content from different website sub-pages, returning a pandas data frame. 

Transformation - [job_two.py](https://github.com/fusaa/hm/blob/main/job_two.py) (or [Job-2.ipynb](https://github.com/fusaa/hm/blob/main/Job-2.ipynb)) - initially, data was transformed using Jupyter notebook and then ported to python for batch execution.

Loading - [job_three.py](https://github.com/fusaa/hm/blob/main/job_three.py) - It loads the data into a SQL database.
