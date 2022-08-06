# installing the packages
install.packages(c("dslabs", "here", "easypackages"))
install.packages(c("gganimate"))
# install.packages("animate")
install.packages("gapminder")
devtools::install_github("thomasp85/gganimate")
library("easypackages")
libraries(c("dslabs", "here"))
libraries(c("ggplot2", "dplyr", "lubridate"))

# reading the data
murders <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-12-10/international_murders.csv")
gun_murders <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-12-10/gun_murders.csv")
diseases <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-12-10/diseases.csv")
nyc_regents <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-12-10/nyc_regents.csv")

## More Datasets

# dslabs::oecd
# dslabs::tissue_gene_expression
# dslabs::temp_carbon
# dslabs::nyc_regents_scores


## Diseases

### Time Series of [disease] by year 

disease_types <- diseases %>% distinct(disease)
all_states <- diseases %>%  distinct(state)

time_series_by_disease_and_state <- function(disease_type, state_type){
  tmp <- diseases %>% 
    filter(disease == disease_type, state == state_type) %>% 
    arrange(year)
  # p <- ggplot(tmp, aes())
  return(tmp)
}

time_series_by_disease_and_state("")

time_series_animation_by_state <- function(state_type){
  tmp <- diseases %>% 
    filter(state == state_type) %>% 
    group_by()
  
}




gapminder::gapminder_unfiltered
