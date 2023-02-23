set.seed(50) # Setting seed before writing function

SimulateNDie <- function(n = 2) {
  # Simulates a n sided die roll and computes the sum of
  # k dice rolls of the same n-sided die.
  #
  # Args:
  # n: Number of sides for the die
  #
  # Returns
  # The sum of k dice rolls of the same n-sided die
  #
  # Error handling
  if (n < 2) {
    stop("Argument n must be greater than or equal to 2.")
  }
  else {
    die <- c(1:n)
    value <- sample(die, 1)
    ksum <- sum(sample(die, value, replace = TRUE))
  }
  return(ksum)
}

SimulateNDie(4) # n = 4

SimulateMExperiments = function(n, m) {
  # Simulates the m experiments for a n sided die to calculate
  # the sum of k dice rolls of the same n-sided die.
  #
  # Args:
  # n: Number of side of the die
  # m: Number of simulations of the experiment
  #
  # Returns
  # A vector of length m showing sum of k-dice rolls
  ksum <- c()
  for (i in 1:m) {
    die <- c(1:n)
    value <- sample(die, 1)
    ksum[i] <- sum(sample(die, value, replace = TRUE))
  }
  return(ksum)
}

SimulateMExperiments(4, 10) 

exp <- SimulateMExperiments(2, 10000) # Calling function
prop.table(table(exp)) # Can be viewed as probability as well

#plots
par(mfrow = c(2, 2)) # Four plots together

# First of all lets plot for n = 4
sim4 <- SimulateMExperiments(4, 10000) # Calling function

# Plotting the box-plot initially
boxplot(sim4, main = "Boxplot for n = 4",
        ylim = c(0, 17), ylab = "K-sum",
        col = "cadetblue2", border = "red")

# Next we plot the histogram
# First lets assign histogram values to a list, makes it easy to work around
hst <- hist(sim4, breaks = c(0:16), plot = FALSE)

# Plotting histogram
plot(hst, xaxt = "n", xlab = "K-sum",
     ylab = "Counts", col = "cadetblue2", border = "red",
     ylim = c(0, 1350), main = "Histogram for n = 4")

axis(1, hst$mids, labels = c(1:16), # For proper x-axis labeling
     padj = - 1.5, tick = FALSE)

abline(v = mean(sim4), col = "blue") # Just to show the mean line

# Next we use similar coding for plotting n = 6.
sim6 <- SimulateMExperiments(6, 10000)

#Box-pot
boxplot(sim6, main = "Boxplot for n = 6",
        ylim = c(0, 37), ylab = "K-sum",
        col = "cadetblue2", border = "red")

# Next histogram similarly as for n = 4
hst <- hist(sim6, breaks = c(0:36), plot = FALSE)
plot(hst, xaxt = "n", xlab = "K-sum",
     ylab = "Counts", col = "cadetblue2", border = "red",
     ylim = c(0, 700), main = "Histogram for n = 6")
axis(1, hst$mids, labels = c(1:36),
     padj = - 1.5, tick = FALSE)
abline(v = mean(sim6), col = "blue")


