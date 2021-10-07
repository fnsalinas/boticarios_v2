"""
Created on 06/10/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

import json

def GetScrapingConfig(store, json_path = "scripts/web_scraping/assets/scraping_config_data.json"):
    """
    DOCUMENTATION PENDING...
    """

    with open(json_path, "r") as jsonData:
        data = json.load(jsonData)
    
    final_data = (
        data["chromedriver"],
        data["urls"][store]
        )
    
    return final_data