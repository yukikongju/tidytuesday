##

library(dplyr)
library(ggplot2)
library(tidyr)

## read csv
data <- read.csv("~/Projects/Emaww/emaww_data.csv")
head(data)

# 1. Find State most commonly displayed by user

#
state_count <- data %>% 
  na.omit("state") %>% 
  select(user, state) %>% 
  group_by(user, state) %>% 
  summarise(count = n(), .groups = 'drop') %>% 
  pivot_wider(names_from = state, values_from = count) %>% 
  mutate_if(is.numeric, ~replace(., is.na(.), 0))

ggplot(stack(state_count[,-1]), aes(ind, fill = values)) + geom_bar(position = "dodge")

stack(state_count[,-1])

#
tmp <- data %>% na.omit("state") %>% select(user, state)
grouped_df <- group_by(tmp, user)
freq_df <- summarise(grouped_df, state = names(which.max(table(state))))
tmp <- freq_df %>% 
  group_by(state) %>% 
  summarise(count = n())
tmp

# YESS
library(forcats)
ggplot(tmp, aes(x=reorder(state, -count), y=count, fill = state)) +
  geom_col(colour = 'black') + 
  xlab("") + 
  ggtitle("State most commonly displayed by users") + 
  geom_text(aes(label = count), vjust = -0.5) 
  
# making a pie chart (NO)
library(scales)
n <- sum(tmp['count'])
ggplot(tmp, aes(x="", y=count, fill=state)) +
  geom_bar(stat = "identity") + 
  coord_polar("y", start=0) +
  scale_fill_brewer(palette = 'Blues') +
  geom_text(aes(y = count/4 + c(0, cumsum(count)[-length(count)]), 
              label = percent(count/n)), size=5)
  # geom_text(aes(y = count / n, label = percent(y/100)), size=5)

# 2. Investigate the state of users just before they perform an action

data %>% 
  group_by(user) %>% 
  reorder(state, -date_time)

summary(data)

df <- data
df$date_time <- as.POSIXct(df$date_time, format = "%m/%d/%Y %H:%M:%S")
df <- df[order(df$date_time), ]
df$prev_state <- c(NA, df$state[-nrow(df)])
df_filtered <- df[!is.na(df$action), ]
grouped_df <- group_by(df_filtered, user)
freq_df <- summarise(grouped_df, prev_state = names(which.max(table(prev_state))))
print(freq_df)


# 3. Find a correlation between state and any of the other variables

chisq.test(data$state, data$url)
chisq.test(data$state, data$device)

tmp <- data %>% 
  na.omit(state, device, url) %>% 
  group_by(state, device) %>% 
  summarise(count = n(), .groups = 'drop') 
tmp

  
# making a mosaic plot
library(vcd)
# tmp <- data 
tmp$state <- as.factor(tmp$state)
tmp$device <- as.factor(tmp$device)

# NO
mosaicplot(table(data$state, data$device))

# YES
library(ggmosaic)
ggplot(data = data %>% na.omit(state, device)) +
  geom_mosaic(color='black', aes(x=product(device, state), fill = device)) + 
  scale_fill_discrete(name='Device') + 
  scale_fill_brewer(palette = 'Spectral') + 
  ggtitle("Mosaic Plot for user's state and device") 


library(RColorBrewer)
par(mar=c(3,4,2,2))
display.brewer.all()

