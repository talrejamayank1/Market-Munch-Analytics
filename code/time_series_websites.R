options(digits=4)
library(forecast)
library(ggplot2)

# plot errors function
plotForecastErrors = function(forecasterrors,forecasttitle) {
  #Function provided by Avril Coghlan
  forecasterrors = na.omit(forecasterrors)
  # make a histogram of the forecast errors:
  mybinsize = IQR(forecasterrors) / 4
  mysd = sd(forecasterrors)
  mymin = min(forecasterrors) - mysd * 5
  mymax = max(forecasterrors) + mysd * 3
  # generate normally distributed data with mean 0 and standard deviation mysd
  mynorm <- rnorm(10000, mean = 0, sd = mysd)
  mymin2 <- min(mynorm)
  mymax2 <- max(mynorm)
  if (mymin2 < mymin) { mymin <- mymin2 }
  if (mymax2 > mymax) { mymax <- mymax2 }
  # make a red histogram of the forecast errors, with the normally distributed data overlaid:
  mybins <- seq(mymin, mymax, mybinsize)
  hist(forecasterrors, col = "red", freq = FALSE, breaks = mybins, main=forecasttitle)
  # freq=FALSE ensures the area under the histogram = 1
  # generate normally distributed data with mean 0 and standard deviation mysd
  myhist <- hist(mynorm, plot = FALSE, breaks = mybins)
  # plot the normal curve as a blue line on top of the histogram of forecast errors:
  points(myhist$mids, myhist$density, type = "l", col = "blue", lwd = 2)
}

# set up the working directory
workingdirectory = "C:\\Users\\14057\\Documents\\SPRING 2022\\DATA SCIENCE PROGRAMMING AND ANALYTICS II\\PROJECT\\msis-5223-deliverable-1-nsms\\data"

# read data and create time series object
temptable1 = paste(workingdirectory, "\\doordash_revenue.txt", sep = "")
temptable2 = paste(workingdirectory, "\\grubhub_revenue.txt", sep = "")
temptable3 = paste(workingdirectory, "\\postmates_revenue.txt", sep = "")
temptable4 = paste(workingdirectory, "\\ubereats_revenue.txt", sep = "")

data_doordash = read.table(temptable1, sep = '\t', header = TRUE)
data_doordash_ts = ts(data_doordash['Annual_Revenue'], frequency = 1, start = c(2017, 1))
data_doordash_ts
data_grubhub = read.table(temptable2, sep = '\t', header = TRUE)
data_grubhub_ts = ts(data_grubhub['Annual_Revenue'], frequency = 1, start = c(2017, 1))
data_grubhub_ts
data_postmates = read.table(temptable3, sep = '\t', header = TRUE)
data_postmates_ts = ts(data_postmates['Annual_Revenue'], frequency = 1, start = c(2017, 1))
data_postmates_ts
data_ubereats = read.table(temptable4, sep = '\t', header = TRUE)
data_ubereats_ts = ts(data_ubereats['Annual_Revenue'], frequency = 1, start = c(2017, 1))
data_ubereats_ts

# Holt Winters modelling for doordash data
hw1 = HoltWinters(data_doordash_ts, beta = FALSE, gamma = FALSE)
hw1
#plot(hw1)
hw1_fore = forecast(hw1, h=4)
#plot(hw1_fore)
#plot(hw1_fore$residuals)
#lines(c(2017, 2021), c(0, 0), col = 'red')
#plotForecastErrors(hw1_fore$residuals,'Assessing Normal Distribution for Doordash')

# Holt Winters modelling for grubhub data
hw2 = HoltWinters(data_grubhub_ts, beta = FALSE, gamma = FALSE)
hw2
#plot(hw2)
hw2_fore = forecast(hw2, h=4)
#plot(hw2_fore)
#plot(hw2_fore$residuals)
#lines(c(2017, 2021), c(0, 0), col = 'red')
#plotForecastErrors(hw2_fore$residuals,'Assessing Normal Distribution for Grubhub')

# Holt Winters modelling for postmates data
hw3 = HoltWinters(data_postmates_ts, beta = FALSE, gamma = FALSE)
hw3
#plot(hw3)
hw3_fore = forecast(hw3, h=4)
#plot(hw3_fore)
#plot(hw3_fore$residuals)
#lines(c(2017, 2021), c(0, 0), col = 'red')
#plotForecastErrors(hw3_fore$residuals,'Assessing Normal Distribution for Postmates')

# Holt Winters modelling for ubereats data
hw4 = HoltWinters(data_ubereats_ts, beta = FALSE, gamma = FALSE)
hw4
#plot(hw4)
hw4_fore = forecast(hw4, h=4)
#plot(hw4_fore)
#plot(hw4_fore$residuals)
#lines(c(2017, 2021), c(0, 0), col = 'red')
plotForecastErrors(hw4_fore$residuals,'Assessing Normal Distribution for Ubereats')