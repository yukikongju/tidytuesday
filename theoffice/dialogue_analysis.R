# Dialogue Analysis
# install.packages("stopwords")
libraries("stopwords", "tidyr")

## Name Wrangling

characters_to_remove <- c("Everyone", "Hostess", "Kid", "Actress", "All", "Both",
  "Liquor Store Clerk", "Girl acting Pregnant", "Improv Teacher", "Doctor", 
  "Lab Tech", "Delivery man", "Group chant", "Guy", "Men", "Women", "Kids", 
  "The Kids", "Office Staff", "Delivery Woman", "Delivery Boy", "Actor", 
  "Ad guy 1", "Ad guy 2", "All but Oscar", "All Girls", "All Men", "Audience", 
  "Attendant", "Bar Manager", "Bartender", "Bass Player", "Blogger", "Blogger 2", 
  "Blonde", "Boat Guy", "Blood Drive Worker", "Blood Girl", "Buyer", "Camera Crew", 
  "Cameraman", "Camera Man", "Chef", "Check-in guy", "Child", "Children", 
  "Client", "Cleaning Lady", "Co-Worker", "Crowd", "CPR Trainer", "Employee", 
  "Employees except Dwight", "Entire Office", "Entire Prince Family", 
  "Female Applicant", "Female intern", "Female Intern", "Female Worker", 
  "Financial Guy", "Guy at Bar", "Guy at bar", "Gym Instructor", "Athlead", 
  "Lady", "Moderator", "Instructor", "Narrator", "Paramedic", "Parent in audience",
  "Parent in audience #1", "Parent in audience #2", "Pastor", "Passor-by", 
  "Phone Salesman", "Phone", "Photographer", "Pretzel Guy", "Prince", 
  "Promo Announcer", "Promo Voice", "Receptionist", "Radio", "Realtor", 
  "Registar", "Rehab Nurse", "Rep", "Reporter", "Reporter #1", "Reporter #2", 
  "School Official", "Secretary", "Security", "Server", "Shareholder", 
  "Solder", "Student", "Son", "Student #1", "Student #2", "Student #3", 
  "Tatoo Artist", "Teacher", "Tall Girl #1", "Tall Girl #2", "Teamates", 
  "Tech Guy", "Woman", "Woman 1", "Woman 2", "Woman 3", "Woman 4", "Younger Man", 
  "Woman in line", "Archivist", "Artist", "Ballerinas", "Athlead Coworker", 
  "Athlead Employee", "Bookstore Employee", "All the Men", "Dealer", 
  "Businessman #1", "Businessman #2", "Businessman #3", "Cleaning Lady", 
  "Co-worker", "Co-Worker 1", "Co-Worker 2", "Co-Worker 3", "Co-worker #2", 
  "Church Congregation", "Man", "Group", "Waiter", "Waitress", "Officer", 
  "Officer 1", "Officer 2")

office <- office %>% 
  filter(!(character %in% characters_to_remove))

characters <- office %>% 
  arrange(character) %>% 
  distinct(character) %>% 
  filter(!(character %in% characters_to_remove))

primary_characters <- c("Michael", "Jim", "Pam", "Dwight", "Kevin", "Angela", 
  "Creed", "Oscar", "Andy", "Erin")
secondary_characters <- c("Gabe", "Jan", "David", "Ryan", "Kelly", "Toby", "Mose",
  "Holly", "Darryl", "Roy", "Phyllis")

## Character Dialogue

get_character_dialogue_by_season <- function(name, season_num){
  dialogue <- office %>% 
    select(season, episode, episode_name, character, text) %>% 
    filter(character == name, season == season_num)
  return(dialogue)
}

get_character_dialogue <- function(name){
  dialogue <- office %>% 
    select(season, episode, episode_name, character, text) %>% 
    filter(character == name)
  return(dialogue)
}

get_favorite_words <- function(name, n){
  # get all the dialogues as list of strings
  words <- get_character_dialogue(name) %>% 
    unnest_tokens(word, text)
  
  # words_filtered <- remove_stop_words(words)
  # words_occurences <- count_words_occurence(words_filtered)
  
  # remove stop words and punctuation
  words_filtered <- words %>%
   filter(!(word %in% stopwords(source = "smart")))
  
  # count words occurrence
  words_occurences <- table(words_filtered$word) %>%
    as.data.frame() %>%
    arrange(desc(Freq)) %>%
    rename(word = Var1) %>%
    top_n(n)
  
  return(words_occurences)
}

remove_stop_words <- function(words){
  # remove stop words and punctuation
  words_filtered <- words %>% 
   filter(!(word %in% stopwords(source = "smart")))
  
  return(words_filtered)
}

count_words_occurence <- function(words){
  # count words occurrence
  words_occurence <- table(words$word) %>% 
    as.data.frame() %>% 
    arrange(desc(Freq)) %>% 
    rename(word = Var1) %>% 
    top_n(n)
  
  return(words_occurence)
}

dwight <- get_character_dialogue("Dwight")
dwight <- get_favorite_words("Dwight", 100)
jim <- get_favorite_words("Jim", 100)
pam <- get_favorite_words("Pam", 100)

# TODO: plot main cast favorite words by season

## Character Appearances

### get character appearance by season

appearances_by_season <- office %>% 
  select(season, character) %>% 
  unique() %>% 
  mutate(has_appeared = TRUE)

total_appearances <- appearances_by_season %>% 
  group_by(character) %>% 
  summarise(total = sum(has_appeared == TRUE)) %>% 
  arrange(desc(total))

season_appearances <- appearances_by_season %>% 
  pivot_wider(names_from = season, values_from = has_appeared, values_fill = FALSE,
              names_glue = "season_{season}") %>% 
  full_join(total_appearances, by="character") %>% 
  arrange(desc(total))
  

### character appearance count by season

num_episodes_by_season <- office %>% 
  select(season, episode) %>% 
  unique() %>% 
  group_by(season) %>% 
  summarise(count=n())

appearances_count <- office %>% 
  select(season, episode, character) %>% 
  unique() %>% 
  group_by(season, character) %>% 
  summarise(count = n()) %>% 
  pivot_wider(names_from = season, values_from = count, values_fill = 0, 
              names_glue = "season_{season}") %>% 
  mutate(total = rowSums(.[2:ncol(.)])) %>% 
  arrange(desc(total))

# TODO: appearances_perc
