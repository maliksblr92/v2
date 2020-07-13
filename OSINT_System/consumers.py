#this dile is created by ahmed 
import json
from channels.generic.websocket import WebsocketConsumer
import random
from bs4 import BeautifulSoup
import requests


class ChartConsumers(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        print(text_data)

        n1 = random.randint(0, 400)
        n2 = random.randint(0, 400)
        n3 = random.randint(0, 400)
        n4 = random.randint(0, 400)

        list1 = [n1, n2, n3, n4]
        self.send(text_data=json.dumps({
            'message': list1
        }))


class HashtagConsumers(WebsocketConsumer):
    def connect(self):
         self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        print(text_data)
        url = 'https://trends24.in/';
        page = requests.get(url);
        status_code = page.status_code;
        dic = {};
        hashtag_name = [];
        hashtag_href = [];
        hashtag_count = [];
        if(status_code == 200):
            data = BeautifulSoup(page.text, 'lxml')
            new = data.find('ol', class_="trend-card__list");
            li = data.find_all('li')
            for i in li:
                hashtag_name.append(i.a.text)
                hashtag_href.append(i.a.attrs['href'])
                if(i.find('span')):
                    hashtag_count.append(i.span.text)
                else:
                    hashtag_count.append("count unavalible")
        dic = []
        for i in range(len(hashtag_name)):
                 dic.append(
                {"name":hashtag_name[i],
                "count":hashtag_count[i],
                "href":hashtag_href[i]
                    })
        self.send(text_data=json.dumps({
            'message': dic
        }))
        print(dic)
        
        #this dile is created by ahmed 