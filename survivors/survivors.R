# installing the package
install.packages("survivoR")
install.packages("plotly")
install.packages("maptools")
install.packages("rgdal") 

library(plotly)

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

