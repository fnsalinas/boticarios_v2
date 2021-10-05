"""
Created on 04/10/2021
Author: Fabio Salinas (fabio.salinas1982@gmail.com)
Version: 1.0
"""

import json

def GetCredentials(user, json_path = "scripts/web_scraping/assets/private/gcp_boticarios//convertidos/log-in.json"):
    """
    DOCUMENTATION PENDING...
    """

    with open(json_path, "r") as jsonData:
        data = json.load(jsonData)
    
    final_data = (
        data["users"][user]["pass"],
        data["connections"][0]["gcp01"]["host"],
        data["connections"][0]["gcp01"]["port"],
        data["connections"][0]["gcp01"]["database"]
        )
    
    return final_data