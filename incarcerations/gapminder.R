install.packages(c("gifski", "av", "ffmpeg"))
library(gapminder)
library(ggplot2)
#use devtools::install_github('thomasp85/gganimate') to install as it is not on CRAN
library(gganimate)

# ggplot from the github README
p <- gapminder::gapminder_unfiltered %>% 
  ggplot(aes(gdpPercap, lifeExp, size = pop, colour = country)) +
  geom_point(alpha = 0.7, show.legend = FALSE) +
  scale_colour_manual(values = country_colors) +
  scale_size(range = c(2, 12)) +
  scale_x_log10() +
  facet_wrap(~continent) +
  # Here comes the gganimate specific bits
  labs(title = 'Year: {frame_time}', x = 'GDP per capita', y = 'life expectancy') +
  transition_time(year) +
  ease_aes('linear')

animate(p, renderer = ffmpeg_renderer())

## second example


p <- ggplot(airquality, aes(Day, Temp)) + 
  geom_line(size = 2, colour = 'steelblue') + 
  transition_states(Month, 4, 1) + 
  shadow_mark(size = 1, colour = 'grey')
animate(p, renderer = ffmpeg_renderer())

## Third Example
ggplot(mtcars) + 
  geom_boxplot(aes(factor(cyl), mpg)) + 
  transition_manual(gear)
