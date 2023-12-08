import pymongo
from pymongo import MongoClient
import logging
from main.Logger import Logger

# Start log config
Logger.setup_logging()


class MongoDBHandler:
    def __init__(self):
        """
        Initialize MongoDBHandler to interact with a MongoDB database.
        Connects to the local MongoDB instance and sets up the database.
        """
        try:
            self.client = MongoClient("mongodb://localhost:27017")
            self.db = self.client["mustafa_oncu"]
            logging.info("MongoDBHandler connected to MongoDB successfully.")
        except pymongo.errors.ConnectionFailure as e:
            logging.error(f"Failed to connect to MongoDB: {e}")

    def save_news(self, news_data):
        """
        Save news data to the 'news' collection in MongoDB.
        :param news_data: List of dictionaries containing news items.
        """
        try:
            news_collection = self.db["news"]
            news_collection.insert_many(news_data)
            logging.info("News data saved to MongoDB successfully.")
        except Exception as e:
            logging.error(f"Error saving news data to MongoDB: {e}")

    def save_word_frequency(self, word_freq_data):
        """
        Save word frequency data to the 'word_frequency' collection in MongoDB.
        :param word_freq_data: Dictionary containing word frequency data.
        """
        try:
            word_freq_collection = self.db["word_frequency"]
            word_freq_collection.insert_one(word_freq_data)
            logging.info("Word frequency data saved to MongoDB successfully.")
        except Exception as e:
            logging.error(f"Error saving word frequency data to MongoDB: {e}")

    def save_stats(self, stats_data):
        """
        Save scraping statistics to the 'stats' collection in MongoDB.
        :param stats_data: Dictionary containing scraping statistics.
        """
        try:
            stats_collection = self.db["stats"]
            stats_collection.insert_one(stats_data)
            logging.info("Scraping statistics saved to MongoDB successfully.")
        except Exception as e:
            logging.error(f"Error saving scraping statistics to MongoDB: {e}")
