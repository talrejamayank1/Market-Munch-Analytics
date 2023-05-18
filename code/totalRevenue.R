library(dplyr)
options(digits=4)
library(tseries)
library(forecast)
library(lmtest)


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
    hist(forecasterrors, ylab = "Revenue", col = "red", freq = FALSE, breaks = mybins, main=forecasttitle)
    # freq=FALSE ensures the area under the histogram = 1
    # generate normally distributed data with mean 0 and standard deviation mysd
    myhist <- hist(mynorm, plot = FALSE, breaks = mybins)
    # plot the normal curve as a blue line on top of the histogram of forecast errors:
    points(myhist$mids, myhist$density, type = "l", col = "blue", lwd = 2)
}


file = read.csv('Revenue_net-Table 1.csv', header = T)
data = select(file, 2)
colnames(data) = 'Revenue'
data_ts = ts(data, frequency = 12, start = c(2012, 1))
#plot(data_ts)

# layout(1:2)
# plot(aggregate(data_ts))
# boxplot(data_ts ~ cycle(data_ts), col = 'skyblue', border = 'black')
# #homoscedasticity
# layout(1::1)
# plot()

data_ts_dc = decompose(data_ts)
#plot(data_ts_dc)

#SD
# print(paste("Standard Deviation with seasonal component", sd(data_ts), sep = " "))
# print(paste("Standard deviation without seasonal component", sd(data_ts - data_ts_dc$seasonal), sep = " "))

revenue_ts_trend = data_ts - data_ts_dc$seasonal
data_trend_es = HoltWinters(revenue_ts_trend, gamma = F)
data_es = HoltWinters(data_ts)
data_trend_fore = forecast(data_trend_es, h=8)
data_fore = forecast(data_es, h= 8)
#plot(data_trend_fore, main = "Without Seasonal Component")
#plot(data_fore, main ="With Seasonal Component")

#NORMALDISTRIBUTION
# layout(1:2)
# plotForecastErrors(data_trend_fore$residuals, 'TotalRevenue: No Seasonal Component')
# plotForecastErrors(data_fore$residuals, 'TotalRevenue: With Seasonal Component')



revenue_trend_data = data.frame(trend = c(data_ts_dc$trend), time = c(time(data_ts_dc$trend)))

revenue_trend_reg = lm(revenue_trend_data$trend ~ revenue_trend_data$time)
#print(summary(revenue_trend_reg))            ###       NON STATIONARITY

# print(adf.test(revenue_ts_trend, k = 20, alternative = "stationary"))
# print(kpss.test(revenue_ts_trend))

#print("After differencing time series object")
revenue_ts_diff1 = diff(revenue_ts_trend, differences = 3)
#print(adf.test(revenue_ts_diff1, k = 20, alternative = "stationary"))
#print(kpss.test(revenue_ts_diff1))

#plot(revenue_ts_diff1)

#acf(revenue_ts_diff1, lag.max=40)
#pacf(revenue_ts_diff1, lag.max = 40)

#print(auto.arima(revenue_ts_diff1))

revenue_arima1 = arima(revenue_ts_diff1, order = c(0,0,0), method = "ML")
#print(revenue_arima1)
revenue_arima2 = arima(revenue_ts_diff1, order = c(2,0,0), method = "ML")
revenue_arima_bic = AIC(revenue_arima1, k = log(length(revenue_ts_diff1)))
#print(revenue_arima_bic)
revenue_arima_bic2 = AIC(revenue_arima2, k = log(length(revenue_ts_diff1)))            ## selected model (2,0,0)
#print(revenue_arima_bic2)


revenue_fore = forecast(revenue_arima2, h = 48)
print(revenue_fore)
#print(accuracy(revenue_fore))