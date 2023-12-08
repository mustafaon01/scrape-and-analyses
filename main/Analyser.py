import re
from collections import Counter
import nltk
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib
# Use Agg backend for non-GUI environment
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from django.conf import settings
import os
from main.Logger import Logger
from collections import defaultdict

# Start log config
Logger.setup_logging()

# Ensure the necessary NLTK packages are downloaded
nltk.download('stopwords')
nltk.download('punkt')


class Analyser:
    def __init__(self, all_news_data):
        """
        Initialize the Analyser with a list of news data.
        :param all_news_data: A list of dictionaries containing news details.
        """
        self.all_news_data = all_news_data
        # Initialize stop words in Turkish
        self.stop_words = set(stopwords.words('turkish'))

    def find_most_common_words(self):
        """
        Find the most common words in all news data.
        :return: A tuple containing a Counter of word frequencies and a list of the 10 most common words.
        """
        try:
            # Combine all text into a single string
            all_text = " ".join(item['text'] for item in self.all_news_data)

            # Tokenize the text
            words = word_tokenize(all_text)

            # Remove non-alphabetic tokens, convert to lower case, and filter out stop words
            words = [word.lower() for word in words if word.isalpha() and word not in self.stop_words]

            # Count the frequency of each word
            word_counts = Counter(words)

            # Get the 10 most common words
            most_common_words = word_counts.most_common(10)

            return word_counts, most_common_words
        except Exception as e:
            logging.error(f"Error in find_most_common_words: {e}")
            return Counter(), []

    def create_word_frequency_bar_chart(self):
        """
        Create a bar chart for the most common words.
        :return: The path to the saved bar chart image and the most common words data.
        """
        try:
            _, most_common_words = self.find_most_common_words()
            words, counts = zip(*most_common_words)

            # Create a bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(words, counts)
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.title('Top 10 Most Frequent Words')
            plt.xticks(rotation=45)

            # Save the bar chart
            bar_chart_path = os.path.join(settings.MEDIA_ROOT, 'word_freq_bar_chart.png')
            plt.savefig(bar_chart_path)
            plt.close()

            logging.info("Word frequency bar chart created successfully.")
            return bar_chart_path, most_common_words
        except Exception as e:
            logging.error(f"Error in create_word_frequency_bar_chart: {e}")
            return None, []

    def create_word_frequency_cloud(self):
        """
        Create a word cloud based on word frequencies.
        :return: The path to the saved word cloud image.
        """
        try:
            word_counts, _ = self.find_most_common_words()

            # Generate word cloud
            wordcloud = WordCloud(width=800, height=800,
                                  background_color='white',
                                  stopwords=self.stop_words,
                                  min_font_size=10).generate_from_frequencies(word_counts)

            # Save the word cloud image
            image_path = os.path.join(settings.MEDIA_ROOT, 'wordcloud.png')
            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(image_path)
            plt.close()

            logging.info("Word cloud created successfully.")
            return image_path
        except Exception as e:
            logging.error(f"Error in create_word_frequency_cloud: {e}")
            return None

    def group_by_update_date(self):
        """
        Groups the news articles by their update dates.
        :return: A dictionary where keys are update dates and values are lists of news articles updated on that date.
        """
        try:
            grouped_data = defaultdict(list)
            for item in self.all_news_data:
                # Group news articles by their 'update_date' field
                grouped_data[item['update_date']].append(item)
            return grouped_data
        except Exception as e:
            logging.error(f"Error in grouping news by update date: {e}")
            return defaultdict(list)
