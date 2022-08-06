# get data
billboard <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-09-14/billboard.csv')
audio_features <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-09-14/audio_features.csv')

# data wrangling - date formatting
billboard$week_id <- as.Date(billboard$week_id, format = "%m/%d/%Y")

# General Information

range(billboard$week_id) # date range: "1958-08-02" to "2021-05-29"

date_unique_values <- billboard %>% 
  distinct(week_id, .keep_all = FALSE) %>% 
  arrange(week_id)


# filter by data range
filter_by_date_range <- function(start, end){
  songs <- billboard[(billboard$week_id >= start & billboard$week_id <= end),]
  return(songs)
}

weekly_top100 <- function(date){
  last_week <- billboard %>% 
    filter(week_id == date) %>% 
    arrange(week_position)
  return(last_week)
}


last_month <- filter_by_date_range("2017-08-09", "2017-09-09")
last_week <- weekly_top100("2017-09-09")

