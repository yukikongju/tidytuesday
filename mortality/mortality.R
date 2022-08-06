# load librairies
library(easypackages)
libraries(c("tidyr", "dplyr", "ggplot"))
libraries((c("corrplot", "Hmisc", "correlation")))

# read data
mortality <- readxl::read_xlsx("Projects/tidytuesday/mortality/global_mortality.xlsx")
# mortality <- readxl::read_xlsx("global_mortality.xlsx")

# Classic EDA

mortality_summary <- summary(mortality)

# get unique values
get_col_unique_values <- function(df){
  num_columns <- ncol(df)
  data <- vector(mode = "list", length = num_columns)
  # iterate through all columns and get unique values
  for( i in 1:num_columns) {
    data[i] <- df[i] %>% unique()
  }
  return(data)
}


countries <- get_col_unique_values(mortality[,1]) %>% unlist()

########## Check Correlation ###########
# https://statsandr.com/blog/correlation-coefficient-and-correlation-test-in-r/
# https://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html

df_numeric <- mortality %>% 
  select(-c(country, country_code))

tmp <- mortality[,c(4,5,6,7,8,9,10)]

corrplot(cor(tmp), method = "number", type = "upper")
corrplot(cor(tmp), method = "number")


pairs(tmp)

res <- rcorr(as.matrix(tmp))$r
res <- rcorr(as.matrix(tmp))$P

mortality_correlation <- correlation(df_numeric, include_factors = TRUE, method = "auto")
mortality_correlation <- correlation(tmp, include_factors = TRUE, method = "auto")

############### Make Linear Regression ################333





############### Global Mortality Evolution #################

global_mortality_by_year <- mortality %>% 
  group_by(year) %>% 
  summarise(across("Cardiovascular diseases (%)": "Terrorism (%)", ~ mean(.x, na.rm = TRUE)))
  
get_mortality_evolution_by_country <- function(name){
  evolution <- mortality %>% 
  filter(country == name) %>% 
  group_by(year) %>% 
  summarise(across("Cardiovascular diseases (%)": "Terrorism (%)", ~ mean(.x, na.rm = TRUE)))
  return(evolution)
}

get_mortality_evolution_by_country('Afghanistan')
get_mortality_evolution_by_country('Canada')










