# loading the required packages
library(RSQLite)

# Defining the database driver
driver <- dbDriver("SQLite")

# parliaments and Goverments data from https://www.parlgov.org/#data
file <- "parlgov-development.db"

# Defining a connection to the database file
parlcon <- dbConnect(driver, dbname = file)

# Tables in the database
dbListTables(parlcon)

# Loading first 5 countries
sql <- "SELECT * FROM country LIMIT 5;"
query <- dbSendQuery(parlcon, statement = sql)
qdata <- fetch(query, n = -1)
qdata

# Loading all country name and abbreviations with sorting
sql <- "SELECT name, name_short FROM country ORDER BY name;"
query <- dbSendQuery(parlcon, statement = sql)
qdata <- fetch(query, n = -1)
qdata

# Earliest and latest time span from election table
sql <- "SELECT MIN(date), MAX(date) FROM election;"
query <- dbSendQuery(parlcon, statement = sql)
qdata <- fetch(query, n = -1)
qdata

# Early election in Sweden, Latvia, Austria and
# United Kingdom
sql <- "SELECT E.country_id, E.date, C.name AS country_name, E.early
          FROM country AS C, election AS E
          WHERE E.country_id = C.id AND
          E.early = 1 AND
          (C.name = 'Sweden' OR
          C.name = 'Latvia' OR
          C.name = 'Austria' OR
          C.name = 'United Kingdom')
          ORDER BY country_name, date;"
query <- dbSendQuery(parlcon, statement = sql)
qdata <- fetch(query, n = -1)
qdata

# Getting the most recent early election of United Kingdom
sql <- "SELECT E.country_id, MAX(E.date) AS date, C.name, E.wikipedia
          FROM country AS C, election AS E
          WHERE E.country_id = C.id AND
          E.early = 1 AND
          C.name = 'United Kingdom';"
query <- dbSendQuery(parlcon, statement = sql)
qdata <- fetch(query, n = -1)
qdata

# Getting country with cabinets lead by Menzies.
sql <- "SELECT C.name AS country_name, Ca.name AS cabinet_name,
          Ca.start_date
          FROM country AS C, cabinet AS Ca
          WHERE C.id = Ca.country_id AND
          Ca.name LIKE '%Menzies%'
          ORDER BY Ca.start_date;"
query <- dbSendQuery(parlcon, statement = sql)
qdata<- fetch(query, n = -1)
qdata

# Getting the cabinet lead by Marin
sql <- "SELECT C.name AS country_name, Ca.start_date
          FROM country AS C, cabinet AS Ca
          WHERE C.id = Ca.country_id AND
          Ca.name LIKE '%Marin%'
          ORDER BY Ca.start_date;"
query <- dbSendQuery(parlcon, statement = sql)
qdata<- fetch(query, n = -1)
qdata

# Getting the cabinet immediately followed by cabinet lead by Martens.
sql <- "SELECT C.name AS country_name, Ca.name AS cabinet_name,
          Min(Ca.start_date) AS start_date
          FROM country AS C, cabinet AS Ca
          WHERE c.id = Ca.country_id AND
          Ca.start_date > (SELECT MAX(Ca.start_date)
          FROM country AS C, cabinet as Ca
          WHERE C.id = Ca.country_id AND
          Ca.name LIKE '%Martens%' );"
query <- dbSendQuery(parlcon, statement = sql)
qdata<- fetch(query, n = -1)
qdata

# Disconnecting the SQL database
dbDisconnect(parlcon)


# XML example
# Loading the required packages
library(XML)
library(xml2)
library(anytime)
library(ggplot2)


list.files("XML") %>%
  paste0("XML/", .) %>%
  lapply(xmlParse) %>%
  lapply(xmlRoot) %>%
  lapply(function(x) getChildrenStrings(x)[c("RecordingEndTime",
                                             "RecordingStartTime")]) %>%
  do.call("rbind", .) %>%
  as.data.frame() %>%
  mutate(RecordingEndTime = anytime(RecordingEndTime)) %>%
  mutate(RecordingStartTime = anytime(RecordingStartTime)) %>%
  mutate(TimeDiff = difftime(RecordingEndTime, RecordingStartTime)) %>%
  arrange(RecordingStartTime) ->
  XML
head(XML)

# plot 
ggplot(data = XML, aes(as.numeric(TimeDiff))) +
  geom_histogram(breaks = seq(45, 83, by = 2.5),
                 col = "red", fill = "blue") +
  ggtitle("Histogram") +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab("Duration (in mins)") +
  ylab("Count") +
  scale_x_continuous(breaks = seq(45, 83, by = 5))

#plot
ggplot(data = XML, aes(x = as.Date(RecordingStartTime),
                       y = as.numeric(TimeDiff))) +
  geom_point(col = "blue") +
  ggtitle("Scatterplot of Date vs Recording lengths") +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab("Recording date") +
  ylab("Recording lengths (in mins)") +
  scale_x_date(date_labels = "%Y (%b)")


