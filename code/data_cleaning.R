library(stringr)                                                                   
library(descriptr)                                                              
myfile = read.csv('filesgrubhubdata.csv') 
    
#Rating
myfile$Rating = as.numeric(myfile$Rating)
myfile$Rating[is.na(myfile$Rating)] = 0        
     
#DeliveryFee
myfile$Delivery.Fee <- gsub(" delivery","",as.character(myfile$Delivery.Fee))
myfile$Delivery.Fee <- gsub("\\$","",as.character(myfile$Delivery.Fee))             
myfile$Delivery.Fee = as.numeric(myfile$Delivery.Fee)                               
myfile$Delivery.Fee[is.na(myfile$Delivery.Fee)] = 0                                

#DeliveryTime
myfile$DeliveryTime <- gsub(" minutes","",as.character(myfile$DeliveryTime))    
myfile$DeliveryTime = str_extract_all(myfile$DeliveryTime, "[0-9][0-9]$")     
myfile$DeliveryTime = as.numeric(myfile$DeliveryTime)
time_mean = mean(myfile$DeliveryTime, na.rm = TRUE)                                	
myfile$DeliveryTime[is.na(myfile$DeliveryTime)] = time_mean                 

#PriceRange
myfile$PriceRange <- factor(myfile$PriceRange,
levels = c('$', '$$', '$$$', '$$$$'),
labels = c("low", "medium", "expensive", "very expensive"))                       
myfile$PriceRange[is.na(myfile$PriceRange)] = "medium"                      

#Cuisine
myfile$Cuisine<-gsub(",", "", as.character(myfile$Cuisine))                     

#Distance
myfile$Distance <- gsub(" mi","",as.character(myfile$Distance))
myfile$Distance <- as.numeric(myfile$Distance)
distance_mean = mean(myfile$Distance, na.rm = TRUE)                               	
myfile$Distance[is.na(myfile$Distance)] = distance_mean                          

names(myfile) <- str_replace_all(names(myfile), c(" " = "_"))
print(ds_screener(myfile))                                              

write.csv(myfile, "Cleaned_Grubhub.csv", row.names  = FALSE )       