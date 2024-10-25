import requests
import json
import datetime
import math
import re

def analyze_wikipage_views(view_data):
    daily_views = []
    for day in view_data["items"]:
        daily_views.append(day["views"])
    total_views = sum(daily_views)
    avg_views = math.ceil(total_views / len(daily_views))
    return (total_views, avg_views)

def get_wikipage_views_month(search_title):
    search_title = search_title.replace(" ", "_")  # Use underscores for Wikipedia titles
    date_today = datetime.datetime.today()
    formatted_date_today = date_today.strftime('%Y%m%d')

    date_30_days_ago = date_today - datetime.timedelta(days=30)

    wikistats_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{search_title}/daily/{date_30_days_ago.strftime('%Y%m%d')}/{formatted_date_today}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(wikistats_url, headers=headers)
    
    # Error handling if artist not found and API problems
    if response.status_code == 404:
        print(f"Error! Artist not found. Check spelling and try again.")
        return

    try:
        wikipedia_view_data = response.json()
 
    except:
        print("An error occured, please try again.")
        return

    filename = f"resources/wikipedia/{search_title}_wikipedia_page_views_{formatted_date_today}.json"
    with open(filename, "w") as file:
        json.dump(wikipedia_view_data, file, indent=4)

    return analyze_wikipage_views(wikipedia_view_data)


# Get wikipedia article length
def get_wikipage_info(search_title):
    query = search_title.replace(" ", "%20")
    search_url = f"https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&titles={query}&redirects=true"
    
    response = requests.get(search_url)

    html_content = response.text
    clean_text = re.sub(r'&lt;.*?&gt;|<.*?>', '', html_content)
    clean_text = clean_text.replace("HTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Special:MyLanguage/Extension:TextExtracts#Caveats.\n", "")

    with open(f"resources/wikipedia/{search_title.replace(' ', '_')}_wikitext.txt", "w", encoding="utf-8") as file:
        file.write(clean_text)

    number_words = len(clean_text.split(" "))
    info_dict = {}
    info_dict["total_words"] = number_words
    info_dict["reading_time"] = round(number_words / 280, 2)
    info_dict["wiki_url"] = f"https://en.wikipedia.org/wiki/{search_title.replace(' ', '_')}"
    
    return info_dict


def print_wiki_info_text(artist):

    wiki_info_dict = get_wikipage_info(artist)
    views_info = get_wikipage_views_month(artist)

    wikipedia_template = f"""
=====================================================================
Wikipedia Page Info about {artist}

Open Wiki Page: {wiki_info_dict["wiki_url"]}

Views in the last 30 days: {views_info[0]:>7}
Average views per day: {views_info[1]:>11}

Total number of words: {wiki_info_dict["total_words"]:>11}
An average reader needs {wiki_info_dict["reading_time"]} minutes to read the text (280 WPM).
=====================================================================
"""
    print(wikipedia_template)