# NYC_Yellow_Cab_Project
Analyze and optimization on yellow cab data 
===================================
![Our Team](https://github.com/ChengdaoYang/NYC_Yellow_Cab_Project/blob/master/Files/connectivity.png "Our Team")
===================================
## Business Anlytics Project
* [What is it](#What-is-it)
* [Define Problem](#Define-Problem)
* [How to operate it](#How-to-operate-it)
* [Sample](#Sample)
* [Group Members](#Group-Members)

### What is it
NYC_Yellow_Cab_Project:
we use the data from NYC TLC: https://www1.nyc.gov/site/tlc/businesses/yellow-cab.page
we clean and analyze the data, from which we then try to discover
an optimal strategies for a taxi driver for in day base on the data 
via machine learn, statistical test, integer programing and tailored algorithm
base on graph theory.
The problem as we defined is NP-hard。
After a week working on it, we are yet to delivery the best
strategies for it, due to time and life constrains for us, humans.
LOL, yes, another NP-hard problem, :P


### Define Problem
define object as: E(min the overall wait time of the day)
         & weight E(max the overall trip time of the day) for a yellow cab taxi driver
   s.t.
      distance_matirx
      wait_time_matrix
      probability matrix
      detail see notebook and algorithm.py
      
 weight: is a mapping: time -> revenue
 
### How to operate it
simply cone the repo:
``` {.sourceCode .bash}
$git clone https://github.com/ChengdaoYang/NYC_Yellow_Cab_Project.git
```
install the requiriment.txt:
``` {.sourceCode .bash}
$pip3 install requirements.txt
```
open Presentation.ipynb with jupyter notebook
and run the algorithm


### Sample
Here is a screenshot of the algorithm, plot on the map
![Our Team](https://github.com/ChengdaoYang/NYC_Yellow_Cab_Project/blob/master/Files/map_path.png "Our Team")
