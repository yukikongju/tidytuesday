# load dataset

install.packages("friends")
library("friends")
library("dplyr")
library("")

dialogue <- friends::friends
scenes_emotions <- friends_emotions
friends_entities
episodes_info <- friends_info

# EDA - Episodes

## Directors episode count

director_count <- table(friends_info$directed_by) %>% 
  sort(decreasing = TRUE) %>% 
  as.data.frame()
  

## EDA - Dialogue

### TODO: Which friends has the most dialogue?

### 


## EDA - Entities

### Which characters appear the most scenes

scences_appearances <- friends_entities

## EDA - Emotions

### What emotions are felt during viewing?

emotions_perc <-  table(emotions = friends_emotions$emotion) %>% 
  as.data.frame() %>% 
  mutate(Perc = Freq/nrow(friends_emotions) * 100) %>% 
  arrange(desc(Freq))
