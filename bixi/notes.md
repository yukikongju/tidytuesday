
## ToDos

- [.] Download deplacement and stations data
    - [ ] for 2021
- [X] Draw bixis capacity on Montreal Map using [geopandas](https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972) (see `notebooks/explore stations.ipynb`)
- [X] Generate monthly usage count datasets
- [o] Generate Capacity count by hour/minutes (year, month, day)
    - [X] daily raw
    - [ ] daily: for each station, for every 5 minutes in a day (14440/5), capacity ( see `notebooks/yearly station usage.ipynb` )
- [ ] Generate daily duration without bikes 
- [ ] Cross-reference all start and end stations


- [ ] WHY 2022 start_pk_emplacement starts with 1000?
- [ ] WHY capacity sum to negatives?


## Questions

- [o] station usage by year
    - [X] longitudinal study: what happened previously
    - [ ] projection for next 5 years
- [ ] Most popular stations
- [ ] How much revenue does BIXI generates?
    - [ ] How long do each trips last?
- [ ] which station is the most empty?
- [ ] where do people park their bike (start -> end)
- [ ] which station capacity should be increased? by how much?
    - [ ] how much time does a station spend without bike (poisson distribution)
    - [ ] 
