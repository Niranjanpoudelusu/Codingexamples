#packages
library(readxl)
library(tidyverse)
library(support.BWS)
library(crossdes)
library(dfidx)
library(mlogit)
library(gmnl)

# data
Data <- read_excel(" Data v1(8166).xlsx")
sum(is.na(Data))

## Taking the design from the slot of first respondent
Data %>% 
  .[1:12,] %>%
  select(Slot_1: Slot_8) %>%
  rename_with(~gsub("Slot_","V", .)) %>%
  as.matrix(.) -> Design

# wide data with most preferred and least preferred
Data %>%
  rename(b = Most_Appealing_Message ) %>%
  rename(w = Least_Appealing_Message) %>%
  pivot_wider(id_cols = c("Respondent","Physician_Type", "Country"),
              names_from = SETID, values_from = c("b", "w")) %>%
  rename_with(~   gsub("_", "", .)) %>%
  as.data.frame(.)-> Response


# wrangling
Response <- Response[,c(1,4,16, 5, 17, 6, 18, 7, 19,8,20,
                        9,21, 10,22, 11,23, 12,24, 13,25,
                        14,26, 15, 27, 2,3)]

# M relates to respective messages
response.vars <- colnames(Response)[2:25]
item.message <- c("M1","M2","M3","M4","M5","M6","M7","M8",
                  "M9","M10", "M11", "M12","M13", "M14","M15", "M16")


# make data suitable for package
md.data <- bws.dataset(
  data = Response,
  response.type = 2,
  choice.sets = Design,
  design.type = 2,
  item.names = item.message,
  id = "Respondent",
  response = response.vars,
  model = "maxdiff")

# simple count analysis
## Running the analysis
cs <- bws.count(md.data, cl =2)

#plot
plot(x =cs,
     score = "bw", 
     pos =4, 
     xlim = c(-2,2.5),
     ylim = c(1, 2))

# bar plot
par(mar = c(5, 4, 4, 2))
barplot(
  height = cs,
  score = "bw",
  mfrow = c(6, 3))

par(mar = c(5, 7, 1, 1))
barplot(
  height = cs,
  score = "sbw", # Standardized BW scores are used
  mean = TRUE,   # Bar plot of mean scores is drawn
  las = 1)


#overall sum
sum(cs) # M is respectuve message 

summary(cs) 

# conditional logit and random parameter mixed logit
md.data %>%
  mutate(Physician1 = ifelse(PhysicianType == 1, 1, 0)) %>%
  mutate(USA = ifelse(Country == 1, 1, 0)) %>%
  mutate(CANADA = ifelse(Country ==2, 1, 0)) -> md.dat

# data set
ml <- mlogit.data(data = md.dat, choice = "RES", shape = "long",
                  alt.var = "PAIR", chid.var = "STR", id.var = "Respondent")


# use base refrences
md.out <- mlogit::mlogit(formula = RES ~ M1 + M2 + M3 + M4 + M5 + M6 + M7 +M8 + 
                           M9 + M10 + M11 + M12 + M13 + M14 + M16 -1, 
                         data = ml, method = "nr") 
summary(md.out)


# relative preferences
sp.md <- bws.sp(md.out, base = "M15")
sp.md

# Mixed logit
rpl <- gmnl(RES ~ M1 + M2 + M3 + M4 + M5 + M6 + M7 + M8 +
              M9 + M10 + M11 + M12 + M13 + M14 + M16|0|0|USA + CANADA + Physician1 -1,
            data = ml, 
            ranp = c(M1 = "n", M2 = "n", M3 = "n",
                     M4 = "n", M5 = "n", M6 = "n",
                     M7 = "n", M8 = "n", M9 = "n",
                     M10 = "n",M11 = "n",M12 = "n",
                     M13 = "n",M14 = "n",M16 = "n"),
            mvar = list(M1 = c("USA","CANADA", "Physician1"),
                        M2 = c("USA","CANADA", "Physician1"),
                        M3 = c("USA","CANADA", "Physician1"),
                        M4 = c("USA","CANADA", "Physician1"),
                        M5 = c("USA","CANADA", "Physician1"),
                        M6 = c("USA","CANADA", "Physician1"),
                        M7 = c("USA","CANADA", "Physician1"),
                        M8 = c("USA","CANADA", "Physician1"),
                        M9 = c("USA","CANADA", "Physician1"),
                        M10 = c("USA","CANADA", "Physician1"),
                        M11 = c("USA","CANADA", "Physician1"),
                        M12 = c("USA","CANADA", "Physician1"),
                        M13 = c("USA","CANADA", "Physician1"),
                        M14 = c("USA","CANADA", "Physician1"),
                        M16 = c("USA","CANADA", "Physician1")) ,
            model = "mixl",
            R = 10, halton = NA, panel = TRUE)


summary(rpl)

# latent calss model with three classes, taking panel nature into account
lcm <- gmnl(RES ~ M1 + M2 + M3 + M4 + M5 + M6 + M7 + M8 +
              M9 + M10 + M11 + M12 + M13 + M14 + M16|0|0|0|USA + CANADA + Physician1,
            data = ml,
            model = "lc",
            Q = 3,
            panel = TRUE,
            method = "bfgs")

summary(lcm)


