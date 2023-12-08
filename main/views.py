from django.shortcuts import render
from main.Scraper import Scraper
from main.Analyser import Analyser
from main.MongoDBHandler import MongoDBHandler
from django.conf import settings


def home(request):
    """
    Home view to handle scraping and displaying data.
    :param request: HTTP request object.
    :return: Rendered HTML page with context data.
    """
    content = {'new_items': []}

    if 'scraper' in request.POST:
        # Scrape the news data
        scraper = Scraper("https://turkishnetworktimes.com/kategori/gundem/", 50)
        all_new_items, stats = scraper.scrape_all_pages_concurrently()

        # Analyse the scraped data
        analyser = Analyser(all_new_items)
        path = settings.MEDIA_URL + 'wordcloud.png'
        bar_chart_path, most_common_words = analyser.create_word_frequency_bar_chart()
        bar_chart_url = settings.MEDIA_URL + 'word_freq_bar_chart.png'

        # Save data to MongoDB
        mongodb_handler = MongoDBHandler()
        mongodb_handler.save_news(all_new_items)
        mongodb_handler.save_word_frequency({'words': most_common_words})
        mongodb_handler.save_stats(stats)

        # Group data by update date
        grouped_data = analyser.group_by_update_date()

        # Update content for the template
        content.update({
            'elapsed_time': stats['elapsed_time'],
            'path': path,
            'bar_path': bar_chart_url,
            'stats': stats,
            'grouped_data': grouped_data.items(),
        })

    return render(request, 'index.html', content)


def read_me(request):
    """
    View to display the README page.
    :param request: HTTP request object.
    :return: Rendered README HTML page.
    """
    return render(request, 'readme.html')
