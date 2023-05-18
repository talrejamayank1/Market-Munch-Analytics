library(psych)
library(car)
library(dummies)

data = read.csv('mydata.csv', header = T)

pr_dummy = dummy(data$PriceRange, sep = '_')
colnames(pr_dummy) = c('pr_Expensive', 'pr_low', 'pr_medium', 'pr_veryexpensive')

pr_dummy = as.data.frame(pr_dummy)
data1 = data.frame(data, pr_dummy)

data1 = na.omit(data1)

data_reg1 = lm(data1$Rating ~ data1$PaymentType + data1$pr_low + data1$pr_medium + data1$pr_Expensive + data1$pr_veryexpensive)
print(summary(data_reg1))
