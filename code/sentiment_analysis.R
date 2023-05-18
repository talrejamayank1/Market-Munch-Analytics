library(tidyverse)
library(tidytext)

#Stemming packages
library(SnowballC)
library(tm)


#####################################################
#============Setup the Working Directory============#
# Set the working directory to the project folder by#
# running the appropriate code below.               #
#####################################################

wd = "C:\\Users\\14057\\Documents\\PYTHON\\Online Food Industry\\CLEANED DATA"
setwd(wd)
temptable = paste(wd, "\\cleaned_data3.csv", sep = "")
reviews_data = read.csv(temptable, header = TRUE)
summary(reviews_data)
customer_reviews = select(reviews_data, Reviews)
tidy_dataset = unnest_tokens(customer_reviews, word, Reviews)
counts = count(tidy_dataset, word)
result1 = arrange(counts, desc(n)) %>%
  ungroup %>%
  slice(1:15)

#==============================
# Plot the the words with a
# proportion greater than 0.5
#==============================
frequency = tidy_dataset %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(proportion = (n / sum(n)*100)) %>%
  filter(proportion >= 0.5)

library(scales)

ggplot(frequency, aes(x = proportion, y = word)) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Word', x = 'Proportion')


#=======================================
# Using the SnowballC package, run the
# function wordStem() on the data to
# apply stemming to the data
#=======================================
tidy_dataset2 = mutate_at(tidy_dataset, "word", funs(wordStem((.), language="en")))
counts = count(tidy_dataset2, word)
arrange(counts, desc(n)) %>%
  ungroup %>%
  slice(1:15)

tidy_dataset2 %>%
  count(word) %>%
  arrange(desc(n)) %>%
  ungroup %>%
  slice(1:15)
# Result: flight is now #1, not #2

frequency2 = tidy_dataset2 %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(proportion = (n / sum(n)*100)) %>%
  filter(proportion >= 0.5)

ggplot(frequency2, aes(x = proportion, y = word)) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Word', x = 'Proportion')


# Generate a new variable assessing the difference between positive and negative
nrc_pos_neg = get_sentiments('bing') %>%
  filter(sentiment == 'positive' | 
           sentiment == 'negative')
newjoin = inner_join(tidy_dataset2, nrc_pos_neg)
counts = count(newjoin, word, sentiment)
spread = spread(counts, sentiment, n, fill = 0)
content_data = mutate(spread, contentment = positive - negative, linenumber = row_number())
tweet_pos_neg = arrange(content_data, desc(contentment))
((nrow(tweet_pos_neg)))

#Generating sentiments for a new csv file to implement sentiment analysis
write.csv(newjoin, "C:\\Users\\14057\\Documents\\PYTHON\\Online Food Industry\\CLEANED DATAsentiments.csv", row.names=FALSE)

# Create a plot for the top 20 values for positive and negative; copy this to your Word document
(tweet_pos_neg2 = tweet_pos_neg %>%
    slice(1:10, 670:680))

ggplot(tweet_pos_neg2, aes(x=linenumber, y=contentment, fill=word)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Index Value',
    y='Contentment'
  ) +
  theme(
    legend.position = 'bottom',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10)
  ) +
  geom_col()


# Generate a new variable assessing the difference between disgust and surprise
nrc_disgust_surprise = get_sentiments('nrc') %>%
  filter(sentiment == 'disgust' | 
           sentiment == 'surprise')
newjoin2 = inner_join(tidy_dataset2, nrc_disgust_surprise)
counts2 = count(newjoin2, word, sentiment)
spread2 = spread(counts2, sentiment, n, fill = 0)
content_data2 = mutate(spread2, contentment = disgust - surprise, linenumber = row_number())
tweet_disgust_surprise = arrange(content_data2, desc(contentment))
((nrow(tweet_disgust_surprise)))

# Create a plot for the top 20 values for positive and negative; copy this to your Word document
(tweet_disgust_surprise2 = tweet_disgust_surprise %>%
    slice(1:10, 181:191))

ggplot(tweet_disgust_surprise2, aes(x=linenumber, y=contentment, fill=word)) +
  coord_flip() +
  theme_light(base_size = 15) +
  labs(
    x='Index Value',
    y='Contentment'
  ) +
  theme(
    legend.position = 'bottom',
    panel.grid = element_blank(),
    axis.title = element_text(size = 10),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10)
  ) +
  geom_col()

