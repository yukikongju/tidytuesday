# install packages

install.packages("devtools")
devtools::install_github("averyrobbins1/appa")


atla <- appa::appa

characters <- atla$character %>% unique()
main_characters <- c("Aang", "Katara", "Zuko", "Sokka", "Toph", "Iroh")

## Character Dialogue

dialogue <- atla %>% 
  filter(!(character == "Scene Description")) %>% 
  select(book_num, chapter_num, character, character_words)


## get num of words talked by episode

num_episodes_per_season <- atla %>% 
  select(book_num, chapter_num) %>% 
  unique() %>% 
  group_by(book_num) %>% 
  summarise(num_episodes = n())

get_characters_num_interventions_by_episode <- function(name){
  # get character num interventions by episode
  interventions <- dialogue %>% 
    filter(character == name) %>% 
    group_by(book_num, chapter_num) %>% 
    summarise(count = n())
  
  # add episode number
  interventions <- add_episode_num(interventions)
  
  return(interventions)
}

add_episode_num <- function(df){
  # create buffer
  book_num <- c(1,2,3)
  start_indices <- c(0,20,40)
  buffer <- data.frame(book_num, start_indices)
  
  # create episode num column based on book and chapter num
  df <- df %>%
    # mutate(episode_num = buffer$start_indices[seasons] + chapter_num)
    full_join(buffer, by = "book_num") %>% 
    mutate(episode_num = start_indices + chapter_num) %>% 
    select(!start_indices) %>% 
    relocate(episode_num, .before = count)
  
  return(df)
}


katara <- get_characters_num_interventions_by_episode("Katara")

### TODO: plot

