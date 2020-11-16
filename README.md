## 602_Crime_Clusters
Homework 2 for UMBCs Data 602 Course. This project makes use of Baltiore City's available Crime Data.
  
## Overviews
 - With interest rates falling, and talk of police reform there are a lof of questions going on in town about "Where to buy? What's safe?". This project
 aims to help to break down available data of Baltimore City crime stats to answers those questions.
### Contents
  - [EDA and Technical Work](HW2_Technical.ipynb)
  - [Streamlined Data Report](HW2_Report.ipynb)
  - [Project Utilities](utils.py)
  - [README](READ.me)
  - [Baltimore City Neighborhood Map](Baltimore_neighborhoods_map.png)

## Goals
  - Create a RF model to describe which CrimeCodes have the highest Incidence and Frequency
  - Create a KMaesn model which describes which neighborhoods highest incidence of crime.
## Data

   - Data comes from : # dataset taken from [Here](https://data.baltimorecity.gov/api/views/2nh2-stru/rows.csv?accessType=DOWNLOAD)
    and can be pulled from [This link](https://github.com/marcelthebridge/602_Crime_Clusters/tree/main/Data)
    - Features of the data:
      - **CrimeDate** > Date of Crime.  We will be focusing on crimes from 2010 and on.
      - **CrimeCode** > 81 unique codes corresponding to specific crimes.
      - **Location** > Stret address of the crime in question.
      - **Description** > Short Description of the  Crime.
      - **District** > Which of Baltimore's 8 Districts did the crime occur in.
      - **Neighborhood** > Which of the 270 neighborhoods did the crimes occur in.
      - **Weapnon** > What Weapon, if any, was involved in the incident?
        - This feature had numerous null values, and as such I felt it better to simply drop it from the dataframe.
