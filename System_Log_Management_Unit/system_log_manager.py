from django.http import JsonResponse
import random
import time
import json
from datetime import datetime,timezone



TIME_FACTOR = int((datetime.now()-datetime(2019,12,17)).total_seconds())
ADDITION_FACTOR = random.randint(200, 400)
SUBTRACTION_FACTOR = 1000
MULTIPLICATION_FACTOR = random.randint(2, 4)

class System_Log_Manager(object):

    def __init__(self):
        pass



    def refresh_fake_prams(self):

        global ADDITION_FACTOR
        global SUBTRACTION_FACTOR
        global MULTIPLICATION_FACTOR

        ADDITION_FACTOR = random.randint(200, 400)
        SUBTRACTION_FACTOR = 100000
        MULTIPLICATION_FACTOR = random.randint(10, 20)

    def article_stat_for_slo(self):
        self.refresh_fake_prams()

        data = {
            'Article Select Count ':25+int(((TIME_FACTOR)*1+ADDITION_FACTOR)),
            'Article Reviewed Count':6+int(((TIME_FACTOR)*0.6+ADDITION_FACTOR)),
            'Requested By PCO Count':3+int(((TIME_FACTOR)*0.3+ADDITION_FACTOR)),
            'Rejected By RPO Count':2+int(((TIME_FACTOR)*0.2+ADDITION_FACTOR)),

            }

        return data

    def article_stat_overview(self):
        self.refresh_fake_prams()

        data = {
            'New Article Count': 50 + int(((TIME_FACTOR) * 3 + ADDITION_FACTOR)),
            'Author Count': 6 + int(((TIME_FACTOR) * 0.1 + ADDITION_FACTOR)),
            'Hashtag Count': 3 + int(((TIME_FACTOR) * 0.2 + ADDITION_FACTOR)),


        }

        return data


    def my_article_stat(self):
        self.refresh_fake_prams()

        data = {
            'Selected Count': 5 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Revised Count': 3 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To PCO ': 3 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To RPO ': 2 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'To DSO': 4 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    def ticket_stat(self):
        self.refresh_fake_prams()

        data = {
            'Read Tickets': 50 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'New Coming Tickets': 34 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Total Inbox Count': 87 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Replied Tickets': 22 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Tickets With New Reply': 29 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }
        return data


    def fetch_stat(self):
        self.refresh_fake_prams()

        data = {
            'Fetched Author': 536 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Fetched Content': 985 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    #......................................STATS FOR WORKLOAD PAGE......................................................

    def extracted_article(self):
        self.refresh_fake_prams()

        data = {
            'Social': 506 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 300 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 99 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 46 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),

        }

        return data

    def extracted_selected_all_sites(self):
        self.refresh_fake_prams()

        data = {
        'extracted':{
            'Social': 606 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Search': 400 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 199 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Blog': 146 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Image': 106 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 82 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 99 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        },
        'selected':{
            'Social': 352 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Search': 156 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'News': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Blog': 21 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Image': 22 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Video': 88 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Page': 45 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        }
        return data

    def extracted_selected_all_social_sites(self):
        self.refresh_fake_prams()

        data = {
            'extracted': {
                'Twitter': 609 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 400 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 199 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 146 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            },
            'selected': {
                'Twitter': 356 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 256 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 7 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            }

        }

        return data

    def processed_article(self):
        self.refresh_fake_prams()

        data = {
            'Image': 506 + int(((TIME_FACTOR) * 0.32 + ADDITION_FACTOR)),
            'Instagram': 300 + int(((TIME_FACTOR) * 0.68  + ADDITION_FACTOR)),

        }

        return data

    def article_trend(self):
        self.refresh_fake_prams()

        data = {
            '12-12-2019': 78 + int(((TIME_FACTOR) * 0.5 + ADDITION_FACTOR)),
            '13-12-2019': 34 + int(((TIME_FACTOR) * 0.6 + ADDITION_FACTOR)),
            '14-12-2019': 87 + int(((TIME_FACTOR) * 0.8 + ADDITION_FACTOR)),
            '15-12-2019': 22 + int(((TIME_FACTOR) * 0.6 + ADDITION_FACTOR)),
            '16-12-2019': 29 + int(((TIME_FACTOR) * 0.68 + ADDITION_FACTOR)),
            '17-12-2019': 22 + int(((TIME_FACTOR) * 0.52 + ADDITION_FACTOR)),
            '18-12-2019': 29 + int(((TIME_FACTOR) * 0.85 + ADDITION_FACTOR)),
        }

        return data

    def send_to_pco(self):
        self.refresh_fake_prams()

        data = {
            'Twitter': 356 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Facebook': 256 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Instagram': 48 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
                'Other': 7 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        return data

    def send_to_rpo(self):
        self.refresh_fake_prams()

        data = {
            'Twitter': 128 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Facebook': 102 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Instagram': 18 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
            'Other': 19 + int(((TIME_FACTOR) * 0 + ADDITION_FACTOR)),
        }

        return data
