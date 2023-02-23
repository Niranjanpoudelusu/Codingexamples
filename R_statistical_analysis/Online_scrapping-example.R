GetUSPop <- function(){
  # Reads the current US population from a Web-page:
  # https://www.livepopulation.com/country/united-states.html
  #
  # Args:
  # None (not required)
  #
  # Returns:
  # Current US population in numbers
  clockHTML <-
    readLines("https://www.livepopulation.com/country/united-states.html")
  unlink("https://www.livepopulation.com/country/united-states.html")
  popLineNum <- grep("<b class=\"current-population\">", clockHTML)
  popLine <- clockHTML[popLineNum]
  text1 <- "\t\t\t<p class=\"text-18 text-bold c-666 text-center\""
  text2 <- "><b class=\"current-population\">|</b></p>"
  text <- paste0(text1, text2)
  popText <- gsub(text, "", popLine)
  pop <- as.numeric(gsub(",", "", popText))
  return(pop)
}

GetUSPop()
Sys.sleep(10) # wait for 10sec
GetUSPop()

EstimateUSPopGrowthOnce <- function (delay = 10){
  # Computes one estimate of the current annual growth
  # of the US population reading the current population from
  # https://www.livepopulation.com/country/united-states.html
  #
  # Args:
  # delay: Time in seconds between two population readings
  #
  # Returns:
  # The estimate of current annual growth of US population
  if(delay < 10) {
    warning("Time interval is too short to obtain meaningful estimate")
    return(NA)
  } else {
    first <- GetUSPop() # Calling previous function
    Sys.sleep(delay) # Default value is in seconds
    second <- GetUSPop() # Calling function again
    diff <- second - first # Difference between two calls
    growth <- diff * (31536000 / delay) # Annual growth
    return(growth)
  }
}
  
EstimateUSPopGrowthOnce(30)

EstimateUSPopGrowthNTimes <- function(N = 1, inbetween = 10,
                                      delay = 10, returnValue = "All") {
  # Computes N estimates of the US population growth
  #
  # Args:
  # N: Number of estimates to be calculated.
  # inbetween: Time between consecutive estimates of population growth.
  # delay: Time in seconds between two population readings from webpage.
  # returnValue: One of 'Mean', "Median' or 'All" based on what value
  # is to be returned.
  #
  # Returns:
  # Either of mean, median or all of N estimates based on the argument.
  # returnValue.
  vec <- vector() # Empty vector
  for (i in 1:N) {
    vec[i] <- EstimateUSPopGrowthOnce(delay) # Estimates growth
    Sys.sleep(inbetween) # Time inbetween estimates
  }
  if (returnValue == "Median") {
    return(median(vec))
  } else if (returnValue == "Mean") {
    return(mean(vec))
  } else if (returnValue == "All") {
    return(sort(vec))
    # Error handling
  } else {
    text1 <- "Error: The returnValue argument should contain"
    text2 <- "one of either 'Mean', 'Median' or 'All'"
    text <- paste(text1, text2)
    cat(text)
    return(NA)
  }
}

EstimateUSPopGrowthNTimes(5, returnValue = "Mean")

FinalGrowthEstimate <- EstimateUSPopGrowthNTimes(10, inbetween = 180,
                                                 delay = 120, returnValue = "All")




  
  
