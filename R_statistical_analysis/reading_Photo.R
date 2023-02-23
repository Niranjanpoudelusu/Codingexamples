# Loading the required packages required
library(tesseract)
library(OpenImageR)
library(tidyverse)


# Extracting the text from images
list.files("Photos") %>%
  paste0("Photos/", .) %>%
  lapply(ocr) %>%
  toString() %>%
  strsplit("\n") %>%
  lapply(tolower) %>%
  unlist() %>%
  str_extract(".*(station|university|museum).*") %>%
  .[!is.na(.)] %>%
  str_extract(".*\\b\\w{3,}\\b") %>%
  str_extract("\\b\\w{3,}\\b.*")
