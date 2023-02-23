library(httr)
library(XML)
library(janitor)

# Getting the top 10 movie directors
GET("https://www.imdb.com/chart/top") %>%
  htmlParse() %>%
  xpathSApply("//a", xmlGetAttr, "title") %>%
  unlist() %>%
  .[1:10] %>%
  gsub("dir.*", "", .) %>%
  gsub(" (", "", ., fixed = TRUE) %>%
  kbl(col.names = "Top-10 movie directors",
      align = "clc", valign = "t",
      caption = "IMDB top 10 movie directors") %>%
  kable_styling(latex_options = c("striped", "hold_position"))


# Directors who appear more than once in top 250
GET("https://www.imdb.com/chart/top") %>%
  htmlParse() %>%
  xpathSApply("//a", xmlGetAttr, "title") %>%
  unlist() %>%
  .[1:250] %>%
  gsub("dir.*", "", .) %>%
  gsub(" (", "", ., fixed = TRUE) %>%
  tabyl(var1 = "Director") %>%
  select(1, 2) %>%
  arrange(desc(n)) %>%
  filter(n > 1) %>%
  kbl(col.names = c("Directors", "Number of movies"),
      longtable = TRUE,
      caption = "Number of movies per dircetor in IMDB top 250") %>%
  kable_styling(latex_options = c("striped", "hold_position",
                                  "repeat_header"))

# First creating regex for prepositions
regex1 <- c(" [Dd]e+$| [Dd]el+$| [Dd]e la+$| Mc+$|")
regex2 <- c( "O'+$| [Vv]an+$| [Vv]on+$")
regex <- paste0(regex1, regex2)
# Arranging the names of the directors
GET("https://www.imdb.com/chart/top") %>%
  htmlParse() %>%
  xpathSApply("//a", xmlGetAttr, "title") %>%
  unlist() %>%
  .[1:250] %>%
  gsub("dir.*", "", .) %>%
  gsub(" (", "", ., fixed = TRUE) %>%
  paste(str_extract(., "\\S+$"), ., sep = ", ") %>%
  gsub(" \\S+$", "", .) %>%
  paste(gsub(" ", "", str_extract(., regex)), .) %>%
  gsub("NA ", "", .) %>%
  gsub(regex, "", .) %>%
  unique() %>%
  sort()

