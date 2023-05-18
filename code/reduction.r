final_data = read.csv('cleaned_data.csv', header = TRUE)
#print(ect_data)
#final_data[final_data$Rating == "Null"] = NA
final_data$Rating = na.omit(final_data$Rating)
final_data$DeliveryFees = na.omit(final_data$DeliveryFees)
final_data$DeliveryTime = na.omit(final_data$DeliveryTime)
final_data$Distance = na.omit(final_data$Distance)

cat("\nSummary of Dataframe before reduction\n\n")
print(str(final_data))

final_data$Rating = as.numeric(final_data$Rating)
final_data$DeliveryFees = as.numeric(final_data$DeliveryFees)
final_data$DeliveryTime = as.numeric(final_data$DeliveryTime)
final_data$Distance = as.numeric(final_data$Distance)

##PCA
half1 = sample(nrow(final_data), nrow(final_data)/2)
reduction_data = final_data[half1, ]
reduction_data1 = final_data[-half1, ]

reduction_data.pca = reduction_data[c("Rating", "DeliveryFees", "DeliveryTime", "Distance")]
pcamodel_reduc = princomp(reduction_data.pca,cor=FALSE)
cat("\nResults of PCA\n")
print(pcamodel_reduc$sdev^2) 
##ScreePlot     
plot(pcamodel_reduc, main="Screeplot")

##FA
reduction_data.FA = factanal(~Rating+DeliveryFees+DeliveryTime+Distance,
	factors=1,
	rotation="varimax",
	scores="none",
	data=reduction_data1)
print(reduction_data.FA)

##DataReduction
cat("\nSummary of DataFrame after reduction \n\n")
final_data = subset(final_data, select = -c(Distance))
str(final_data)

##ExportFile
restuarant_data = write.csv(final_data, "Restaurants_data.csv")
