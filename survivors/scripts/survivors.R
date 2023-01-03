# installing the package
install.packages("survivoR")
install.packages("plotly")
install.packages("maptools")
install.packages("rgdal") 

library(plotly)
library(dplyr)

# storing data into variables
castaway_details <- survivoR::castaway_details
castaways <- survivoR::castaways
challenge_description <- survivoR::challenge_description
challenge_results <- survivoR::challenge_results
challenges <- survivoR::challenges
confessionals <- survivoR::confessionals
hidden_idols <- survivoR::hidden_idols
jury_votes <- survivoR::jury_votes
season_palettes <- survivoR::season_palettes
season_summary <- survivoR::season_summary
tribe_colours <- survivoR::tribe_colours
tribe_mapping <- survivoR::tribe_mapping
viewers <- survivoR::viewers
vote_history <- survivoR::vote_history


castaways %>% 
  filter(castaway == c("Victoria", "Michelle", "Michaela"))

castaways %>% 
  filter(season == 4) %>% 
  arrange(desc(day)) %>% 
  select(c(season_name, full_name, day, result)) 

tmp <- castaways %>% 
  select(c(season_name, full_name, day, result)) %>% 
  print(n=800)

tmp <- castaway_details %>% 
  select(c(full_name, occupation, personality_type))

  
