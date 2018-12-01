Foodi 

## Introduction

Foodi is a program that aims to help local Food Aid Non-Governmental Organizations (NGO), which distributes food baskets to needy people's homes on a regular basis with the help of volunteers, to find the best driving paths in terms of saving driving time.
Foodi uses google API for checking different allocations of volunteers to distribute the food baskets to the people's homes, and it outputs the best option. 
Foodi relies on the Probability theory to do so.

 ## Requirements
This module requires the following modules/libraries: 

* Pandas
* Numpy
* Matplotlib
* Datetime
* googlemaps (+ google developers api key)
* gmplot (+ google developers api key)

## Configuration

1. Enter your google api_key on the Start settings section of main.py  
2. Enter your data & settings Excel file name on the Start settings section of main.py

The file needs to have 3 sheets:
    1. "data" - 3 columns (in this order) for each point:
                    * "Week" - Point week (this column need to be filled even for one group only use)
                    *  "Name" - Point name (unique name for each row)
                    *  "Adderss" - Point adderss (steert + street number)

    2. "basic_settings" - 2 columns "name" and "set_to" (value) with this settings options:
                    * "distribution_city" - City name of all points in the file
                    * "distribution_country" - Country name of all points in the file
                    * "distribution_center_Name" - Center point name
                    * "distribution_center_Address" - Center point address (steert + street number)
                    * "distribution_weekday" - Weekday of the next food baskets distribution
                    * "distribution_time" - Time of the next food baskets distribution (HH:MM)
                    * "iterations" - Number of random iterations for finding the best volunteers allocation
                    * "score" - Measure for choosing the best volunteers allocation:
                                                                    - 'average' - minimize the average driving time of volunteers
                                                                    - 'min' - minimize the longest driving time of volunteers

    3. "group_settings" - 2 columns for each volunteers groups:
                    * "week" - volunteers groups week (the weeks needs to be written exactly as in the "data" sheet)
                    * "group_size" - number of distribution points to allocate for this group
        Note that the sum of groups size needs to be equal to the number of points in the file (per week)


## Autor
Eyal Berger

## Version
v1.0



       



 
  