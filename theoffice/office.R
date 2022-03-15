# Getting the data
install.packages("schrute")
install.packages("easypackages")
library("schrute")
library("easypackages")
libraries(c("ggplot2", "dplyr", "plotly", "hrbrthemes"))

# data wrangling
office <- schrute::theoffice
office_episodes <- schrute::theoffice %>% 
  select(!c("character", "text", "text_w_direction", "index")) %>% 
  unique()

# EDA - writers

## Which episode did Toby, Kelly, Ryan and Moses wrote?

get_episodes_by_writers <- function(writers) {
episodes <- office_episodes %>% 
  filter(writer %in% writers)
return(episodes) 
}

get_episodes_by_directors <- function(directors){
episodes <- office_episodes %>% 
  filter(director %in% directors)
return(episodes) 
}

get_episodes_by_writers(c("Paul Lieberstein", "Mindy Kalling", "B.J. Novak", "Michael Schur"))
get_episodes_by_writers(c("Steve Carell", "Rainn Wilson", "John Krasinski"))
get_episodes_by_directors(c("Steve Carell", "Rainn Wilson", "John Krasinski"))

# EDA - Episodes Rating


## Which episode is above the average score

median_score <- median(ratings$imdb_rating)
average_score <- mean(ratings$imdb_rating)
ratings <- ratings %>% 
  mutate(is_above_average=ifelse(imdb_rating >= median_score, TRUE, FALSE))


## Season Rating Average

ratings_by_season <- schrute::theoffice %>% 
  select(season, episode_name, imdb_rating) %>% 
  unique() %>% 
  group_by(season) %>%
  summarise(season_rating = mean(imdb_rating)) %>% 
  arrange(desc(season_rating))
 

## How many episodes by season are above average?

ratings_above_average_count_by_seasons <- schrute::theoffice %>% 
  select(season, episode_name, imdb_rating) %>% 
  unique() %>% 
  group_by(season) %>% 
  mutate(is_above_average=ifelse(imdb_rating >= median_score, TRUE, FALSE)) %>% 
  summarise(Episodes_count = n(), above_average_count = sum(is_above_average == TRUE)) %>% 
  mutate(Perc = above_average_count / Episodes_count * 100)


## Time Series IMDB_Rating

ratings <- schrute::theoffice %>% 
  select(air_date, season, episode, episode_name, imdb_rating) %>% 
  unique() %>% 
  rename(date=air_date)

annotations <- ratings %>% 
  filter(date %in% c("2009-02-01", "2010-01-21", "2011-04-28", "2012-03-15", "2013-05-16"))

ratings$date <- as.Date(ratings$date)


p <- ratings %>% 
  ggplot(aes(x=date, y=imdb_rating)) +
  geom_line(color = "#69b3a2") + 
  geom_hline(yintercept = median_score, color = "red", size = .4) +
  theme_ipsum_es() +
  ggtitle("The Office IMDB Rating") + 
  ylab("IMDB Rating (/10)") + 

p
ggplotly(p)


