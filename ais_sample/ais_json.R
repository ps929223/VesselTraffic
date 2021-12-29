

# install.packages("RcppSimdJson")
# install.packages("jsonlite")
# install.packages("bench")


library(tidyverse)
library(jsonlite)
library(RcppSimdJson)

file_list <- dir(pattern = "[.]json")


# benchmark results
res <- bench::mark(
  RcppSimdJson = RcppSimdJson::fload(file_list[2]),
  jsonlite = jsonlite::fromJSON(file_list[2]),
  check = FALSE
)

res



# `fload()` faster than `fromJSON()`

ais_df <- fload(file_list[1]) %>%
  unlist %>% t %>%
  as.data.frame


ocean_weather2 <- fload(file_list[2]) %>%
  as.data.frame
