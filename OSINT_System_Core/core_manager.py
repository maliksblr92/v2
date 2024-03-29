from django_eventstream import send_event
import random
from bs4 import BeautifulSoup
import requests
from Public_Data_Acquisition_Unit.mongo_models import Global_Target_Reference

class Update_Bigview():

    def update_hashtag_charts(self):
        values=Global_Target_Reference.target_count_for_all_sites()
        json_data = values
        send_event('bigview_streams', 'hashtag_charts', json_data)

    def update_youtube_charts(self):

        values=Global_Target_Reference.target_count_for_all_sites()
        json_data = values
        send_event('bigview_streams', 'youtube_charts', json_data)

    def update_reddit_trends(self):
        print("core manager function called in view")
        json_data = {
            "trend_type": "reddit_trends",
            "trend_graph": [],
            "popular_hashtag": "",
            "top_trends": [
                {
                    "author_fullname": "t2_2bfojune",
                    "selftext": "We post dark, demented memes and we're looking for people to join our community. \n\nr/Dark_Demented_Memes",
                    "title": "Join our new subreddit r/Dark_Demented_Memes !",
                    "count": 6
                },
                {
                    "author_fullname": "Jt2_4qqy8cha",
                    "selftext": "We remodeled the subreddit",
                    "title": "r/adults",
                    "count": 3
                }
            ],
            "country": "",
            "common_words": [],
            "spelling_variants": []
        }
        send_event('bigview_streams', 'reddit_trends', json_data)

    def update_hashtag_trends(self):
        url = 'https://trends24.in/';
        page = requests.get(url);
        status_code = page.status_code;
        dic = {};
        hashtag_name = [];
        hashtag_href = [];
        hashtag_count = [];
        if (status_code == 200):
            data = BeautifulSoup(page.text, 'lxml')
            new = data.find('ol', class_="trend-card__list");
            li = data.find_all('li')
            for i in li:
                hashtag_name.append(i.a.text)
                hashtag_href.append(i.a.attrs['href'])
                if (i.find('span')):
                    hashtag_count.append(i.span.text)
                else:
                    hashtag_count.append("count unavalible")
        dic = []
        for i in range(len(hashtag_name)):
            dic.append(
                {"name": hashtag_name[i],
                 "count": hashtag_count[i],
                 "href": hashtag_href[i]
                 })

        print(dic)
        json_data = dic
        send_event('bigview_streams', 'twitter_trends', json_data)

    def update_youtube_toptrends(self):
        youtube_trends = {
            "trends": [
                {
                    "video_name": "Kahin Deep Jalay - EP 26 Teaser - 12th Mar 2020 - HAR PAL GEO DRAMAS",
                    "video_link": "https://www.youtube.com/watch?v=uGO7lwgHDsc",
                    "channel_name": "HAR PAL GEO",
                    "channel_link": "https://www.youtube.com/user/harpalgeo",
                    "thumbnail_directory": "https://i.ytimg.com/vi/uGO7lwgHDsc/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCnzg6MGsqesxceBTNwuimmtLXmow",
                    "video_duration": "1:11",
                    "partial_description": "Kahin Deep Jalay - EP 26 Teaser - 12th Mar 2020 - HAR PAL GEO DRAMAS\n\nThis is the story of a beautiful girl named Rida, who is the beloved sister of her three brothers and blue-eyed child of...",
                    "views": "2,840,760",
                    "timestamp": "3 days ago"
                },
                {
                    "video_name": "Drama Ehd-e-Wafa | Last Episode - 15 Mar 2020 (ISPR Official)",
                    "video_link": "https://www.youtube.com/watch?v=7wYnw3yUI3k",
                    "channel_name": "ISPR Official",
                    "channel_link": "https://www.youtube.com/channel/UCEwlPFzuck7KyNAnsujkkFg",
                    "thumbnail_directory": "https://i.ytimg.com/vi/7wYnw3yUI3k/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDPLNTfr9CwryhnRJEA8vcBAZFcng",
                    "video_duration": "1:25:52",
                    "partial_description": "Ehd-e-Wafa is a 2019 Pakistani military drama television series co produced by Inter-Services Public Relations and Momina Duraid under MD Productions.It has an ensemble cast with Ahad Raza...",
                    "views": "2,371,013",
                    "timestamp": "13 hours ago"
                },
                {
                    "video_name": "Ye Dil Mera Episode 21 Promo HUM TV Drama",
                    "video_link": "https://www.youtube.com/watch?v=chkLuksaH7U",
                    "channel_name": "HUM TV",
                    "channel_link": "https://www.youtube.com/user/HumNetwork",
                    "thumbnail_directory": "https://i.ytimg.com/vi/chkLuksaH7U/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLC1SKu96qNyBXCbrD-nS7z7_pGA_A",
                    "video_duration": "1:10",
                    "partial_description": "Ye Dil Mera Episode 21 Promo HD Full Official video - 11 March 2020 at Hum TV official YouTube channel.  Subscribe to stay updated with new uploads. https://goo.gl/o3EPXe \n\n#YeDilMera #HUMTV...",
                    "views": "1,937,959",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Khatron Ke Khiladi 14th March 2020 Full Episode 7",
                    "video_link": "https://www.youtube.com/watch?v=LwISjw5rX2Y",
                    "channel_name": "ZD HD",
                    "channel_link": "https://www.youtube.com/channel/UCDt2WSg61hP15J5bGKJsKJA",
                    "thumbnail_directory": "https://i.ytimg.com/vi/LwISjw5rX2Y/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLD_WLlnnZeQswpAR9_KKdBz2M76RA",
                    "video_duration": "1:25:50",
                    "partial_description": "",
                    "views": "602,597",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Thora Sa Haq Episode 21 | Teaser |  ARY Digital Drama",
                    "video_link": "https://www.youtube.com/watch?v=5eOZyhs5waA",
                    "channel_name": "ARY Digital",
                    "channel_link": "https://www.youtube.com/channel/UC4JCksJF76g_MdzPVBJoC3Q",
                    "thumbnail_directory": "https://i.ytimg.com/vi/5eOZyhs5waA/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDPdeAU4oJnTIM-3j0MVLes4goWkQ",
                    "video_duration": "1:06",
                    "partial_description": "Subscribe: https://bit.ly/2PN1K08\n\nDownload ARY Zap: https://l.ead.me/bb9zI1\n\nThora Sa Haq\u2013A Tale Of Compromises\n\nThora Sa Haq tells the story of three individuals; Zamin, Seher and Hareem....",
                    "views": "1,431,915",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Outbreak of Coronavirus in Pakistan | Headlines 12 AM | 14 March 2020 | Dunya News",
                    "video_link": "https://www.youtube.com/watch?v=VWGzEDrxQKA",
                    "channel_name": "Dunya News",
                    "channel_link": "https://www.youtube.com/user/dunyanews1",
                    "thumbnail_directory": "https://i.ytimg.com/vi/VWGzEDrxQKA/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCjMJhVgE589VFIRXOy7MRZyptMYA",
                    "video_duration": "13:42",
                    "partial_description": "Outbreak of Coronavirus in Pakistan | Headlines 12 AM | 14 March 2020 | Dunya News\n\nDunya News is famous and one of the most credible news channels of Pakistan. Watch the latest National, Internati...",
                    "views": "296,399",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Latest South indian Dubbed Movie 2020 | South Indian Hindi Dubbed Movie",
                    "video_link": "https://www.youtube.com/watch?v=XnA4BM2ENnI",
                    "channel_name": "\u092a\u094d\u0930\u0940\u092e\u093f\u092f\u092e \u0926\u093f\u0917\u0940\u092a\u094d\u0932\u0947\u0915\u094d\u0938 \u092e\u0942\u0935\u0940\u091c",
                    "channel_link": "https://www.youtube.com/channel/UCsWZswe3poQmdb2E7WVrkpQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/XnA4BM2ENnI/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDrNzdPJWo2Z5V_HRjS-hkloALnIg",
                    "video_duration": "2:00:54",
                    "partial_description": "",
                    "views": "15,061,183",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Exclusive Footage of PAF F-16 Down in Islamabad",
                    "video_link": "https://www.youtube.com/watch?v=AXrHSz9_l0M",
                    "channel_name": "The Info Light",
                    "channel_link": "https://www.youtube.com/channel/UCZ9P5rK4gGE-dTKg47gxiOQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/AXrHSz9_l0M/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBP7deS42-BDfRLiSU-YTDE6wvRgA",
                    "video_duration": "5:03",
                    "partial_description": "Exclusive Footage of PAF F -16 Down in Islamabad\n#PAF #F-16 #The_info_light",
                    "views": "594,191",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Multan Sultans & Zalmi Friends at my house | Dinner & Fun time | Shahid Afridi",
                    "video_link": "https://www.youtube.com/watch?v=Ex0x_8HVnTc",
                    "channel_name": "Shahid Afridi",
                    "channel_link": "https://www.youtube.com/channel/UCIhGXeOeWeEPxMLbCrUvf-g",
                    "thumbnail_directory": "https://i.ytimg.com/vi/Ex0x_8HVnTc/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLB3HqRNPYa2u-nmlE4paGuif3kuqA",
                    "video_duration": "13:06",
                    "partial_description": "Includes interviews of Mohammad Irfan, Darren Sammy, Rilee Rossouw, Mohammad Ilyas, Shan Masood, Moeen Ali\n\nSpecial thanks to Danish Shivani - CEO, HASHTAG Network for conducting interviews...",
                    "views": "1,353,092",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Mera Jism Meri Marzi | Gharida Farooqi Vs Kashif Abbasi | News Eye With Mehar Bukhari | Dawn News",
                    "video_link": "https://www.youtube.com/watch?v=zfiLM5bQHAc",
                    "channel_name": "Top Pakistani News",
                    "channel_link": "https://www.youtube.com/channel/UCky4jqybV5XHnLg0egiBCkg",
                    "thumbnail_directory": "https://i.ytimg.com/vi/zfiLM5bQHAc/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLAnBN2b3xb7J_WIxo4rt2E-Ft59cA",
                    "video_duration": "18:52",
                    "partial_description": "Mera Jism Meri Marzi | Gharida Farooqi Vs Kashif Abbasi | News Eye With Mehar Bukhari | Dawn News\n\nTop Pakistani News is Pakistan Most Loved and most watched Talk Shows and Entertainment channel...",
                    "views": "2,186,476",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Champions With Waqar Zaka Episode 21 | Champions BOL House | Waqar Zaka Show",
                    "video_link": "https://www.youtube.com/watch?v=4pW9qwSZxM0",
                    "channel_name": "BOL Network",
                    "channel_link": "https://www.youtube.com/channel/UCV6-CUNsfe2-STYfYkd7bBQ",
                    "thumbnail_directory": "",
                    "video_duration": "1:16:37",
                    "partial_description": "Champions With Waqar Zaka Episode 21 | Champions BOL House | Waqar Zaka Show\n#Champions #BOLHouse #WaqarZaka\n\nSubscribe our Youtube Channel: https://bit.ly/2OkzAK7\n\nVisit our Website: https://bit.l...",
                    "views": "1,591,781",
                    "timestamp": "6 days ago"
                },
                {
                    "video_name": "Resham Laughing During Fight Between Khalil Ur Rehman And Amir Liaquat in Live Show | Desi Tv",
                    "video_link": "https://www.youtube.com/watch?v=_e9m8aOj0kk",
                    "channel_name": "Desi Tv",
                    "channel_link": "https://www.youtube.com/channel/UCDwJWkIRoHVTtzR9tJZbP-A",
                    "thumbnail_directory": "",
                    "video_duration": "14:38",
                    "partial_description": "Resham Laughing During Fight Between Khalil Ur Rehman And Amir Liaquat in Live Show | Desi Tv\n\nHaven't had a fun moment today? Seem out of touch of what is happening in the entertainment world?...",
                    "views": "1,651,510",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Sajal Ali & Ahad Raza Mir Nikah | Complete Video | Celeb Tribe",
                    "video_link": "https://www.youtube.com/watch?v=EcnCYCH9rh4",
                    "channel_name": "Celeb Tribe",
                    "channel_link": "https://www.youtube.com/channel/UC_0XA3RER41AtjOUsTaM2tQ",
                    "thumbnail_directory": "",
                    "video_duration": "1:20",
                    "partial_description": "Watch Sajal Ali's Wedding video, \nSajal Ali & Ahad Raza Mir Nikah | Complete Video | Celeb Tribe\n#SajalAli #Ahad #Nikah\nSubscribe Us Here https://goo.gl/PmRj9u\nCeleb Tribe is a 1st Pakistani...",
                    "views": "244,528",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Yeh Rishta Kya Kehlata Hai 14th March 2020 Full Episode",
                    "video_link": "https://www.youtube.com/watch?v=KVzofRJx2e8",
                    "channel_name": "TC Entertainment TV",
                    "channel_link": "https://www.youtube.com/channel/UCDEQu6mtxeNb9vm0-1Fnx_g",
                    "thumbnail_directory": "",
                    "video_duration": "23:32",
                    "partial_description": "Yeh Rishta Kya Kehlata Hai 14th March 2020 \n\nYeh Rishta Kya Kehlata Hai 14 March 2020",
                    "views": "556,205",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "\u0932\u0947\u091f\u0947\u0938\u094d\u091f \u0938\u093e\u0909\u0925 \u0907\u0902\u0921\u093f\u092f\u0928 \u0921\u092c\u0947\u0921 \u0939\u093f\u0902\u0926\u0940 \u092e\u0942\u0935\u0940 2020 | Vijay Latest Movie",
                    "video_link": "https://www.youtube.com/watch?v=qr1usTuFsBY",
                    "channel_name": "Sur Movies",
                    "channel_link": "https://www.youtube.com/channel/UCCYIEiTDpn6F0qZYtwJx-sw",
                    "thumbnail_directory": "",
                    "video_duration": "1:52:34",
                    "partial_description": "",
                    "views": "12,806,799",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Lahore Qalandars Vs Multan Sultans | Full Match Highlights | Match 29 | HBL PSL 5 | 2020",
                    "video_link": "https://www.youtube.com/watch?v=baYSfQPZac0",
                    "channel_name": "Sports Central",
                    "channel_link": "https://www.youtube.com/channel/UC-fzWbU1zavz77kP1gPPdSg",
                    "thumbnail_directory": "",
                    "video_duration": "21:40",
                    "partial_description": "Lahore Qalandars Vs Multan Sultans | Full Match Highlights | Match 29 | HBL PSL 5 | 2020\n\nSubscribe to our channel and stay updated with the latest happenings in HBL PSL 2020! http://bit.ly/Pakista...",
                    "views": "336,770",
                    "timestamp": "16 hours ago"
                },
                {
                    "video_name": "VIDEO: Wing Commander Noman Akram Embraces Martyrdom",
                    "video_link": "https://www.youtube.com/watch?v=cyu7Q-pmnJs",
                    "channel_name": "Lahore News HD",
                    "channel_link": "https://www.youtube.com/channel/UC0CbUVRC1d1RvunYbp3w2qQ",
                    "thumbnail_directory": "",
                    "video_duration": "0:40",
                    "partial_description": "VIDEO: Wing Commander Noman Akram Embraces Martyrdom \n\nSubscribe to our channel:  https://bit.ly/2KGSTIK\n\nVisit our website: http://lahorenews.tv\n\nTo watch news live, visit: http://lahorenews.tv/li...",
                    "views": "1,082,002",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "China successfully defeats Coronavirus l 14 March 2020",
                    "video_link": "https://www.youtube.com/watch?v=N4a0EaUT9nE",
                    "channel_name": "GNN",
                    "channel_link": "https://www.youtube.com/channel/UC35KuZBNIj4S5Ls0yjY-UHQ",
                    "thumbnail_directory": "",
                    "video_duration": "1:18",
                    "partial_description": "From News Headlines to Bulletins, Talkshow Programs, Inside Stories and Breaking News of Pakistan and around the world, stay ahead of the news always with GNN, G News Network.\r\n\r\nWith the likes...",
                    "views": "962,442",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "A Untold Story of Marvi Sarmad - Shan Ali TV",
                    "video_link": "https://www.youtube.com/watch?v=GfvyE1cF8GE",
                    "channel_name": "Shan Ali TV",
                    "channel_link": "https://www.youtube.com/channel/UCaR0gQX0pEMunAtwGzhfkHA",
                    "thumbnail_directory": "",
                    "video_duration": "10:03",
                    "partial_description": "A Untold Story of Marvi Sarmad - Shan Ali TV\nIn this video all about marvi sarmad.\n\n#khalilurrehmanqamar #marvisarmad\n\nCopyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance...",
                    "views": "1,096,324",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "Mere Angne Mein | Jacqueline F, Asim Riaz | Neha K, Raja H, Tanishk B | Radhika - Vinay | Bhushan K",
                    "video_link": "https://www.youtube.com/watch?v=miALiNbU0wY",
                    "channel_name": "T-Series",
                    "channel_link": "https://www.youtube.com/user/tseries",
                    "thumbnail_directory": "",
                    "video_duration": "5:00",
                    "partial_description": "Gulshan Kumar and T-Series presents Bhushan Kumar's \u201cMere Angne Mein \" song, featuring Jacqueline Fernandez and Asim Riaz in the video. This holi special track is sung by Neha Kakkar & Raja...",
                    "views": "33,582,126",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "BHAI - BEHAN ON HOLI || Rachit Rojha",
                    "video_link": "https://www.youtube.com/watch?v=P1jR-nVffXA",
                    "channel_name": "Rachit Rojha",
                    "channel_link": "https://www.youtube.com/channel/UCwBlZvRTu3vasTWUE9U5wPw",
                    "thumbnail_directory": "",
                    "video_duration": "14:30",
                    "partial_description": "#VMateAsliHolibaaz #VMate #VMateHoliSapnaDance \n\nWatch VMate Asli Holibaaz short movie air on March 8th only on VMate app and check out who\u2019s the Asli Holibaaz!\nFriends, stay tuned for VMate...",
                    "views": "12,384,872",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Maulana's condolences to Corona virus | Molana Tariq Jamil | Latest Friday Special",
                    "video_link": "https://www.youtube.com/watch?v=9O1S9ZYRJv0",
                    "channel_name": "Tariq Jamil Official",
                    "channel_link": "https://www.youtube.com/channel/UCct5L-DaVYK8UtmqGU8gJtw",
                    "thumbnail_directory": "",
                    "video_duration": "3:35",
                    "partial_description": "#Coronavirus #MolanaTariqJamil\nThis is The Official YouTube Channel of Tariq Jamil, commonly referred to as Molana Tariq Jameel, is a Pakistani religious and Islamic scholar, preacher, and...",
                    "views": "2,355,416",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Sajal Ali and Ahad Raza Nikkah (Exclusive Video and Pictures)",
                    "video_link": "https://www.youtube.com/watch?v=7yoCn5SsCPI",
                    "channel_name": "Reviewitpk",
                    "channel_link": "https://www.youtube.com/channel/UCCuwoIgz6aFORXjvd-PdspQ",
                    "thumbnail_directory": "",
                    "video_duration": "1:03",
                    "partial_description": "Ahad and Sajal are finally getting married today: 14th March 2020. People have been waiting for their wedding for a long time, and finally, IT\u2019S HAPPENING! \n\nThe stunning couple is having...",
                    "views": "843,515",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Kundali Bhagya 13th March 2020 Full Episode",
                    "video_link": "https://www.youtube.com/watch?v=H3WxuoN7uBk",
                    "channel_name": "MOON TV",
                    "channel_link": "https://www.youtube.com/channel/UC91VLwygqFOrY-5F8juBTjw",
                    "thumbnail_directory": "",
                    "video_duration": "22:17",
                    "partial_description": "",
                    "views": "755,254",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Lahore Qalandars vs Multan Sultans | Full Match Instant Highlights | Match 29 | 15 March | HBL PSL 5",
                    "video_link": "https://www.youtube.com/watch?v=Np5vXtZVHwc",
                    "channel_name": "Pakistan Super League",
                    "channel_link": "https://www.youtube.com/channel/UCpNzXJ5jpcJojC5mHQvGA8w",
                    "thumbnail_directory": "",
                    "video_duration": "16:03",
                    "partial_description": "Lahore Qalandars vs Multan Sultans | Full Inning Instant Highlights | Match 29 | 15 March | HBL PSL 2020\n\nSubscribe to Official HBL Pakistan Super League Channel and stay updated with the latest...",
                    "views": "803,788",
                    "timestamp": "16 hours ago"
                },
                {
                    "video_name": "Final Exams | Ashish Chanchlani",
                    "video_link": "https://www.youtube.com/watch?v=J-zn8PdvZOU",
                    "channel_name": "ashish chanchlani vines",
                    "channel_link": "https://www.youtube.com/user/ashchanchlani",
                    "thumbnail_directory": "",
                    "video_duration": "15:03",
                    "partial_description": "Hello all aap sab ke lie aa chuki hai humari special\nFINAL EXAMS KI VIDEO\nGo and watch now and let us know your favorite scene and dialogue from the video\n\n#FinalExams #AshishChanchlani #VMateAsliH...",
                    "views": "18,583,848",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "First look of bride and groom",
                    "video_link": "https://www.youtube.com/watch?v=reG__LHIl68",
                    "channel_name": "green parrot",
                    "channel_link": "https://www.youtube.com/channel/UCPMlyDn5U8ZP1iiKFgeIkPQ",
                    "thumbnail_directory": "",
                    "video_duration": "2:53",
                    "partial_description": "In this video, beautiful bride and dashing groom at their Nikah and Mehndi. This video has educational purpose only.\nThanks for watching.\r\nGreen Parrot\r\nJoin us on FaceBook:     fb.me/greenparrot10...",
                    "views": "155,843",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "BEAUTY vs DARE - 30 Seconds Challenge | Anaysa",
                    "video_link": "https://www.youtube.com/watch?v=6PGvsePDYp4",
                    "channel_name": "Anaysa",
                    "channel_link": "https://www.youtube.com/user/iloveindianmakeup",
                    "thumbnail_directory": "",
                    "video_duration": "9:33",
                    "partial_description": "Today we are presenting a video with lots of comedy with some challenges so watch the complete video to know who wins the challenges. Hope you all will enjoy the video. Do Comments which challenge...",
                    "views": "1,292,810",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Salman Khan Latest Hindi Full Movie | Sonam Kapoor, Neil Nitin Mukesh",
                    "video_link": "https://www.youtube.com/watch?v=ZiBxcQNSBn8",
                    "channel_name": "RG Entertainment",
                    "channel_link": "https://www.youtube.com/channel/UCgfO009hB_847kwL6NQnn-w",
                    "thumbnail_directory": "",
                    "video_duration": "2:38:34",
                    "partial_description": "Directed by: Sooraj R. Barjatya\n\nScreenplay by: Sooraj R. Barjatya\n\nStarring: Salman Khan\nSonam Kapoor\n\n\u00a9 RG Entertainment India Pvt. Ltd 2019\r\n----------------------------------------------------...",
                    "views": "4,628,372",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "The Kapil Sharma Show Season 2 - Ep 121 - Full Episode - 8th March, 2020",
                    "video_link": "https://www.youtube.com/watch?v=I3xkPnuWwek",
                    "channel_name": "SET India",
                    "channel_link": "https://www.youtube.com/user/setindia",
                    "thumbnail_directory": "https://i.ytimg.com/vi/I3xkPnuWwek/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLAoKgic3TscHM4Rcf_EVxzlDYxqUw",
                    "video_duration": "55:37",
                    "partial_description": "Click here to Subscribe to SET India: https://www.youtube.com/channel/UCpEhnqL0y41EpW2TvWAHD7Q?sub_confirmation=1\n\nClick here to watch the full episodes of The Kapil Sharma Show: \nhttps://www.youtu...",
                    "views": "1,702,039",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "Geo Headlines 08 AM | 15th March 2020",
                    "video_link": "https://www.youtube.com/watch?v=zWF43DOpfnQ",
                    "channel_name": "Geo News",
                    "channel_link": "https://www.youtube.com/user/geonews",
                    "thumbnail_directory": "https://i.ytimg.com/vi/zWF43DOpfnQ/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCwVbTc4dohmTeLq4QxAN0YGesZBA",
                    "video_duration": "10:32",
                    "partial_description": "#GeoHeadlines 08 AM | 15th March 2020 | #GEONEWS\n\n\nFor More Videos Subscribe - https://www.youtube.com/geonews\nVisit our Website for More Latest Update - https://www.geo.tv/",
                    "views": "285,680",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Why Ehd e Wafa Episode 25 Not Telecast On Hum Tv Drama",
                    "video_link": "https://www.youtube.com/watch?v=u4LsyG_B5c0",
                    "channel_name": "Promo tv",
                    "channel_link": "https://www.youtube.com/channel/UCyCNWjK-96ulRreoOINPoxQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/u4LsyG_B5c0/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCQlkiN7-fsNW9_jATR4Hkp-KC2Dg",
                    "video_duration": "1:21",
                    "partial_description": "Why Ehd e Wafa Episode 25 Not Telecast On Hum Tv Drama \n\nDisclaimer/Disclaimers: I have use Some Images From Hum Tv Channel Drama Under The Fair Usage Policy For Review Of Drama That Allows...",
                    "views": "428,888",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Ben Dunk Thrilling Sixes Against Karachi | Karachi Kings vs Lahore Qalandars | Match 23 | PSL 2020",
                    "video_link": "https://www.youtube.com/watch?v=sNfO7OKCY7Y",
                    "channel_name": "Talk Shows Central",
                    "channel_link": "https://www.youtube.com/user/GirlsPk1",
                    "thumbnail_directory": "https://i.ytimg.com/vi/sNfO7OKCY7Y/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDhtDMV_tZMdCORtjT8HZClzz-r7Q",
                    "video_duration": "11:58",
                    "partial_description": "Ben Dunk Thrilling Sixes Against Karachi | Karachi Kings vs Lahore Qalandars | Match 23 | PSL 2020\n\n#PMIMRANKHAN # TALKSHOWSCENTRAL #PAKISTANI#1CHANNEL\n\nTalk Shows Central is Pakistan Most...",
                    "views": "622,212",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Naagin 4 - 14th March 2020 - \u0928\u093e\u0917\u093f\u0928 4 - Full Episode",
                    "video_link": "https://www.youtube.com/watch?v=pv74i01CSKA",
                    "channel_name": "Colors TV",
                    "channel_link": "https://www.youtube.com/user/colorstv",
                    "thumbnail_directory": "https://i.ytimg.com/vi/pv74i01CSKA/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCwon6JXFF6iYqFgiHXvrxPAaTFtQ",
                    "video_duration": "42:12",
                    "partial_description": "Brinda realises that she has to become the most powerful Naagin in the world in order to defeat Vishaka. On the other hand, Vishaka uses magic to give a new face to Nayantara and joins hands...",
                    "views": "235,691",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Types of PSL Fans | Karachi Vynz Official",
                    "video_link": "https://www.youtube.com/watch?v=bETfYUftM4k",
                    "channel_name": "Karachi Vynz Official",
                    "channel_link": "https://www.youtube.com/user/karachivinesofficial",
                    "thumbnail_directory": "https://i.ytimg.com/vi/bETfYUftM4k/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCGwGwtEoBhB8yivbEiPqujnVurEg",
                    "video_duration": "6:21",
                    "partial_description": "#DilSeCricketBola #KarachiVynz #ComedySketch #PakistaniYoutuber\n\nIf there\u2019s one thing Pakistanis take seriously, that\u2019s their love for cricket!\nWhat type of PSL fan are you? Tag your friends...",
                    "views": "293,181",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Ishqiya Episode 7 | Teaser | Feroze Khan & Hania Amir | Top Pakistani Drama",
                    "video_link": "https://www.youtube.com/watch?v=cKPKnyVWlas",
                    "channel_name": "Top Pakistani Dramas",
                    "channel_link": "https://www.youtube.com/channel/UCQ5a6t32eTalvd-n2jQN1QQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/cKPKnyVWlas/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCP3_oN3OMXsG78YvYHwPcPfrW_bw",
                    "video_duration": "0:58",
                    "partial_description": "#HaniaAmir #FerozeKhan #RamshaKhan\n\nDownload ARY Digital App:http://l.ead.me/bauBrY\n\nDownload  ARY ZAP APP :https://l.ead.me/bb9zI1\n\nIshqiya | The Story Of Love, Trust & Betrayal\n\nNot everyone...",
                    "views": "349,979",
                    "timestamp": "6 days ago"
                },
                {
                    "video_name": "Aas | Episode 24 |  TV One Drama | Zain Baig - Hajra Yamin",
                    "video_link": "https://www.youtube.com/watch?v=ORJXFH0wu18",
                    "channel_name": "TV One",
                    "channel_link": "https://www.youtube.com/channel/UCatkw-24OJitQmOVKPhQk1g",
                    "thumbnail_directory": "https://i.ytimg.com/vi/ORJXFH0wu18/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDtdZ_Fx8zDnVfIYEVzAS5cxopIBQ",
                    "video_duration": "36:04",
                    "partial_description": "Aas Episode 24 TV One Drama \n\nSubscribe to stay updated with new uploads. \nhttp://tiny.cc/d78xdz\n\n#Aas #HajraYamin #TVOneDrama \n\nAnother powerful script\nfrom Sarwat Nazir\n\nSafeer desperately...",
                    "views": "273,558",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Scientists of Israel Likely to Announce Development of Vaccine",
                    "video_link": "https://www.youtube.com/watch?v=is9pcTmW_bk",
                    "channel_name": "Haqeeqat TV",
                    "channel_link": "https://www.youtube.com/channel/UCR6yfDK_u5EXby7CnG9-rYw",
                    "thumbnail_directory": "https://i.ytimg.com/vi/is9pcTmW_bk/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBn8dJjlDDNzlX7-fQgd_676BXikQ",
                    "video_duration": "6:04",
                    "partial_description": "Scientists in Israel are working hard to develop new Vaccine for the humanity. They are cable to control and develop anything which is the requirement of this world. China and other countries...",
                    "views": "406,721",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Ehd e Wafa All Cast Interview | FUCHSIA Coverage | FUCHSIA Live",
                    "video_link": "https://www.youtube.com/watch?v=MjiYi7RGNFM",
                    "channel_name": "FUCHSIA Magazine",
                    "channel_link": "https://www.youtube.com/channel/UC_1rczc2lkkpeDnkvCQLZzQ",
                    "thumbnail_directory": "",
                    "video_duration": "22:42",
                    "partial_description": "Ehd e Wafa Live Show | FUCHSIA Coverage | All Cast Interview\n\nWatch & enjoy as we go live & behind the scenes on the set of your favourite drama seriel Ehd E Wafa and have gupshup with its...",
                    "views": "568,067",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "Now its Reached in Lahore. Whats next???",
                    "video_link": "https://www.youtube.com/watch?v=b7IDibgfI_4",
                    "channel_name": "Mubasher Lucman Official",
                    "channel_link": "https://www.youtube.com/channel/UCslugpmYWJiZK5rbvtcaV7Q",
                    "thumbnail_directory": "",
                    "video_duration": "10:07",
                    "partial_description": "#MubasherLucman #Pakistan \n\nMubasher Lucman is currently on the top of anchorpersons index in Pakistan & specializes in Investigative Journalism. He currently hosts program Khara Sach.\n\nFacebook...",
                    "views": "230,802",
                    "timestamp": "1 day ago"
                },
                {
                    "video_name": "Match 29 - Lahore Qalandars Vs Multan Sultans - Second Innings Highlights",
                    "video_link": "https://www.youtube.com/watch?v=NF2vxG2gS0k",
                    "channel_name": "Cricingif",
                    "channel_link": "https://www.youtube.com/channel/UCp0QbQP61tvyLYjUN4afUUQ",
                    "thumbnail_directory": "",
                    "video_duration": "10:05",
                    "partial_description": "Match 29 - Lahore Qalandars Vs Multan Sultans - Second Innings Highlights\n\n#HBLPSLV #CricketForAll",
                    "views": "158,536",
                    "timestamp": "17 hours ago"
                },
                {
                    "video_name": "CCTV footage of the F-16 plane crash",
                    "video_link": "https://www.youtube.com/watch?v=iqxZ1FLm9E8",
                    "channel_name": "ARY News",
                    "channel_link": "https://www.youtube.com/user/ARYNEWSofficial",
                    "thumbnail_directory": "",
                    "video_duration": "1:50",
                    "partial_description": "#F16Plane #NomanAkram #CCTVFootage\n\nOfficial Facebook: https://www.fb.com/arynewsasia\n\nOfficial Twitter: https://www.twitter.com/arynewsofficial\n\nOfficial Instagram: https://instagram.com/arynewstv...",
                    "views": "265,654",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Fiza Ali Revealed The Relation With Her Ex Husband And How She Got Divorced | EPK | Celeb City",
                    "video_link": "https://www.youtube.com/watch?v=WIQfQzAquO0",
                    "channel_name": "Celeb City Official",
                    "channel_link": "https://www.youtube.com/channel/UC5fEui9AMRGGPN1M29Fpzfg",
                    "thumbnail_directory": "",
                    "video_duration": "10:11",
                    "partial_description": "Fiza Ali Revealed The Relation With Her Ex Husband And How She Got Divorced | EPK | Celeb City\n\nHaven't had a fun moment today? Seem out of touch of what is happening in the entertainment world?...",
                    "views": "255,508",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "Jo Log Sajiday Main Aankhain Band Kr Lety Hain | Spread Knowledge",
                    "video_link": "https://www.youtube.com/watch?v=WpvBtTfp0uA",
                    "channel_name": "Spread Knowledge",
                    "channel_link": "https://www.youtube.com/channel/UCtnSmaSii8CXCEWkKUcl-_Q",
                    "thumbnail_directory": "",
                    "video_duration": "10:24",
                    "partial_description": "#SpreadKnowledge\n\nJo Log Namaz Main Aankhain Band Kr Lety Hain | Spread Knowledge \n\n\n\nSubscribe Now\nhttps://goo.gl/CNzCEk\n\n------------------------------------------------------\nCopyright Disclaime...",
                    "views": "505,561",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "Dua-e-Reem | Shoaib Mansoor | Mahira Khan | Damiah Farooq | Shehnaz | Mehak Ali | English Subtitles",
                    "video_link": "https://www.youtube.com/watch?v=QcON6vmP9no",
                    "channel_name": "Yousaf Salli",
                    "channel_link": "https://www.youtube.com/channel/UCvny6uQhQtE5fDROfVbbWdw",
                    "thumbnail_directory": "",
                    "video_duration": "7:45",
                    "partial_description": "Subscribe to the official channel of Mian Yousaf Salahuddin and remain updated about the new upload. Click to subscribe: https://goo.gl/fJknAq\n\nTrack: Dua-e-Reem\nSingers: Damiah Farooq, Shehnaz,...",
                    "views": "761,904",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "26 PRICELESS HACKS FOR PARENTS",
                    "video_link": "https://www.youtube.com/watch?v=93dIviz82JU",
                    "channel_name": "5-Minute Crafts",
                    "channel_link": "https://www.youtube.com/channel/UC295-Dw_tDNtZXFeAPAW6Aw",
                    "thumbnail_directory": "",
                    "video_duration": "13:56",
                    "partial_description": "PARENTING TRICKS TO HELP YOU WITH YOUR KIDS\r\n\r\nBeing a parent isn\u2019t an easy task. So, in this video I show you some easy tricks to get your kids to behave and make your life easier. \r\nIf...",
                    "views": "5,657,430",
                    "timestamp": "4 days ago"
                },
                {
                    "video_name": "Cricket is in Danger | The World is at High Risk | Shoaib Akhtar",
                    "video_link": "https://www.youtube.com/watch?v=ayQMz--OK2A",
                    "channel_name": "Shoaib Akhtar",
                    "channel_link": "https://www.youtube.com/channel/UCeWqACGRU5gT0BXeFhrixWA",
                    "thumbnail_directory": "",
                    "video_duration": "7:18",
                    "partial_description": "Cricket is in Danger | The World is at High Risk | Shoaib Akhtar\n\nMy Take on the Ongoing issue that has Jolted Everything around us. My Prayers for the World .\n\n#PindiExpress #PSL2020 #Ipl2020...",
                    "views": "616,207",
                    "timestamp": "2 days ago"
                },
                {
                    "video_name": "Mera Jism Meri Marzi | Mushahid Ullah Khan Speech in Senate | Aurat March 2020",
                    "video_link": "https://www.youtube.com/watch?v=OYwqqsXyEwM",
                    "channel_name": "Public News",
                    "channel_link": "https://www.youtube.com/channel/UCElJZvY_RVra6qjD8WSQYog",
                    "thumbnail_directory": "",
                    "video_duration": "11:05",
                    "partial_description": "Mera Jism Meri Marzi | Mushahid Ullah Khan Speech in Senate | Aurat March 2020\n\nPublic News Pakistan keeps you fully updated of the latest and major happenings in Pakistan and around the globe...",
                    "views": "1,114,717",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "BAARISH - Mahira Sharma & Paras Chhabra | Sonu Kakkar | Nikhil D\u2019Souza | Tony Kakkar | Anshul Garg",
                    "video_link": "https://www.youtube.com/watch?v=mhOkHwCH73g",
                    "channel_name": "Desi Music Factory",
                    "channel_link": "https://www.youtube.com/channel/UCLtNvbkqea8wN_kGtfgx_Mw",
                    "thumbnail_directory": "",
                    "video_duration": "5:07",
                    "partial_description": "Anshul Garg presents Baarish By Sonu Kakkar & Nikhil D\u2019Souza ft. Mahira Sharma & Paras Chhabra .\n\n\nListen to Baarish On Gaana!\nhttps://gaana.com/album/baarish-hindi-1-2\n\nSinger: Sonu Kakkar...",
                    "views": "11,819,201",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "I AM LOOKING FOR A GIRL !!!",
                    "video_link": "https://www.youtube.com/watch?v=cuVDRGD0SDY",
                    "channel_name": "Ducky Bhai",
                    "channel_link": "https://www.youtube.com/channel/UC_c-RTowPbIlzMkIa_O7s6Q",
                    "thumbnail_directory": "https://i.ytimg.com/vi/cuVDRGD0SDY/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLChIxHBcqRtv-nVMsB2WOK9H1OcxQ",
                    "video_duration": "8:20",
                    "partial_description": "Thanks for watching and don't forget to subscribe :D\n\nWatch VMate Asli Holibaaz short movie air on March 8th and check out who\u2019s the Asli Holibaaz! Friends, stay tuned for VMate Asli Holibaaz...",
                    "views": "913,162",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Chal Mera Putt 2 | Official Trailer | Amrinder Gill | Simi Chahal | Releasing 13 March 2020",
                    "video_link": "https://www.youtube.com/watch?v=N1l670JGSlo",
                    "channel_name": "Rhythm Boyz",
                    "channel_link": "https://www.youtube.com/channel/UC8KlAzFi-luP2jo_gRgQk7A",
                    "thumbnail_directory": "https://i.ytimg.com/vi/N1l670JGSlo/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLAOLz2yiFZUiEVNQryh72szzrEHwA",
                    "video_duration": "3:20",
                    "partial_description": "Rhythm Boyz Entertainment, Gillz Network, Omjee Star Studios And Phantasy Films Ltd Productions Presents \"Chal Mera Putt 2\"\n\nDirected By Janjot Singh\nWritten By Rakesh Dhawan \n\nProduced By...",
                    "views": "9,635,363",
                    "timestamp": "3 weeks ago"
                },
                {
                    "video_name": "Khalil Ul Rehman Qamar Aur Marvi Sarmad Main Garma Garmi",
                    "video_link": "https://www.youtube.com/watch?v=iELn7ZVnPv0",
                    "channel_name": "Neo Tv Network - Official",
                    "channel_link": "https://www.youtube.com/channel/UCAsvFcpUQegneSh0QAUd64A",
                    "thumbnail_directory": "https://i.ytimg.com/vi/iELn7ZVnPv0/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCtOyob-qZo7pjmukEk9owbHo7m_w",
                    "video_duration": "14:23",
                    "partial_description": "Khalil Ul Rehman Qamar Aur Marvi Sarmad Main Garma Garmi\n\nNeo News with a slogan Pakistanio Ki Awaaz is addressing and communicating the latest and accurate Happenings In Pakistan and around...",
                    "views": "1,188,745",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Geo Headlines 12 AM | 10th March 2020",
                    "video_link": "https://www.youtube.com/watch?v=zlxvbU72rMM",
                    "channel_name": "Geo News",
                    "channel_link": "https://www.youtube.com/user/geonews",
                    "thumbnail_directory": "https://i.ytimg.com/vi/zlxvbU72rMM/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDfE0F-7L-lj6ve0KMfCIcJTABbzA",
                    "video_duration": "9:25",
                    "partial_description": "#GeoHeadlines 12 AM | 10th March 2020 | #GEONEWS\n\nFor More Videos Subscribe - https://www.youtube.com/geonews\nVisit our Website for More Latest Update - https://www.geo.tv/",
                    "views": "626,232",
                    "timestamp": "6 days ago"
                },
                {
                    "video_name": "The Kapil Sharma Show Season 2 - Ep 119 - Full Episode - 1st March, 2020",
                    "video_link": "https://www.youtube.com/watch?v=vZx-PUqei68",
                    "channel_name": "SET India",
                    "channel_link": "https://www.youtube.com/user/setindia",
                    "thumbnail_directory": "https://i.ytimg.com/vi/vZx-PUqei68/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDFN0yiS5vY6k_JfuHmmZDgGh8nJg",
                    "video_duration": "1:01:55",
                    "partial_description": "Click here to Subscribe to SET India: https://www.youtube.com/channel/UCpEhnqL0y41EpW2TvWAHD7Q?sub_confirmation=1\n\nClick here to watch the full episodes of The Kapil Sharma Show: \nhttps://www.youtu...",
                    "views": "3,370,525",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Salman Khan NEW Hindi Movie 2020 - Bollywood Latest Movie",
                    "video_link": "https://www.youtube.com/watch?v=DdW2FW5li1w",
                    "channel_name": "DFM TV",
                    "channel_link": "https://www.youtube.com/channel/UCYr2nqqpQabyXpREePef2zA",
                    "thumbnail_directory": "https://i.ytimg.com/vi/DdW2FW5li1w/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLC_UGEOUFOe_ADZuodtQ7lFd8J9Rw",
                    "video_duration": "2:02:47",
                    "partial_description": "#newhindimovies2020\nWatch Salman khan new movie 2020\n\nNEW south Dubbed Movie 2020\n\n\nNeed Your Support Just Click to Subscribe us :https://goo.gl/5320vn",
                    "views": "3,289,706",
                    "timestamp": "2 weeks ago"
                },
                {
                    "video_name": "Vidyut Jamwal New Bollywood Hindi Movie 2020",
                    "video_link": "https://www.youtube.com/watch?v=xaZwleNYUHQ",
                    "channel_name": "HiT Movies",
                    "channel_link": "https://www.youtube.com/channel/UCfLwW-F4P_BSFXU7R2VFSDw",
                    "thumbnail_directory": "https://i.ytimg.com/vi/xaZwleNYUHQ/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLD-_Bc2zZKnNwysyhpqTkV5jGdQZA",
                    "video_duration": "1:54:25",
                    "partial_description": "",
                    "views": "15,367,415",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Sooryavanshi | Official Trailer | Akshay K, Ajay D, Ranveer S, Katrina K | Rohit Shetty | 24th March",
                    "video_link": "https://www.youtube.com/watch?v=u5r77-OQwa8",
                    "channel_name": "Reliance Entertainment",
                    "channel_link": "https://www.youtube.com/user/bigpictures",
                    "thumbnail_directory": "https://i.ytimg.com/vi/u5r77-OQwa8/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCRQYUbo9K1TBnXOy4StvedqyfjEw",
                    "video_duration": "4:16",
                    "partial_description": "Rohit Shetty's Cop Universe!\n\nPresenting the official trailer of Sooryavanshi.\nReliance Entertainment presents \nRohit Shetty Picturez\nIn association with Dharma Productions and Cape Of Good...",
                    "views": "68,766,490",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "Waseem Badami's Masoomana Sawal with Senior Actor Humayun Saeed",
                    "video_link": "https://www.youtube.com/watch?v=ffitANVH9f4",
                    "channel_name": "Har Lamha Purjosh",
                    "channel_link": "https://www.youtube.com/channel/UCOtNchTkC6QgZ3i1LtJejtQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/ffitANVH9f4/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBpTlQLkgyyqrImRr-J33b-qWO-Fg",
                    "video_duration": "20:04",
                    "partial_description": "#MasoomanaSawal #HumayunSaeed #WaseemBadami\n\nPakistan''s Biggest Cricket Show Ever - Har Lamha Purjosh (PSL Season 5) Special.\n\nHosted by Waseem Badami along with  Syed Atif, Ahmed Shah, Basit...",
                    "views": "345,160",
                    "timestamp": "5 days ago"
                },
                {
                    "video_name": "BB Ki Vines- | Business Call |",
                    "video_link": "https://www.youtube.com/watch?v=QQF4Uz4CZMg",
                    "channel_name": "BB Ki Vines",
                    "channel_link": "https://www.youtube.com/channel/UCqwUrj10mAEsqezcItqvwEw",
                    "thumbnail_directory": "https://i.ytimg.com/vi/QQF4Uz4CZMg/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLAaJxu2cP_-E2NvPKEex3z0DUN0Vw",
                    "video_duration": "7:44",
                    "partial_description": "Babloo ji has an important video call with an American client today. What's going to happen?\n\nWatch VMate Asli Holibaaz Video air on March 8th only on VMate app and check out who\u2019s the Asli...",
                    "views": "10,538,763",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "WATCH!! Khalil ur Rehman First Response After Marvi Sarmad Fight",
                    "video_link": "https://www.youtube.com/watch?v=lRDt7iZubTQ",
                    "channel_name": "24 News HD",
                    "channel_link": "https://www.youtube.com/channel/UCcmpeVbSSQlZRvHfdC-CRwg",
                    "thumbnail_directory": "https://i.ytimg.com/vi/lRDt7iZubTQ/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCK2Zl4Dt-v0n_10BE_e4UXvR8H7g",
                    "video_duration": "10:02",
                    "partial_description": "WATCH!! Khalil ur Rehman First Response After Marvi Sarmad Fight\n\nKhalil ur Rehman First Response After Marvi Sarmad Fight On Live TV Show | Khalil ur Rehman First Response After Marvi Sarmad...",
                    "views": "787,928",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "\u0915\u0942\u0932 \u092b\u093c\u0942\u0921 \u0939\u0948\u0915\u094d\u0938 \u0914\u0930 \u092e\u091c\u093c\u093e\u0915\u093f\u092f\u093e \u091f\u094d\u0930\u093f\u0915\u094d\u0938\u0964\u0964 \u0906\u0938\u093e\u0928 DIY \u0916\u093e\u0928\u0947 \u0915\u0947 \u091f\u093f\u092a\u094d\u0938 \u0914\u0930 \u091c\u093c\u093f\u0928\u094d\u0926\u0917\u0940 \u0915\u0947 \u0939\u0948\u0915\u094d\u0938 123 GO \u0915\u0940 \u0924\u0930\u092b \u0938\u0947!",
                    "video_link": "https://www.youtube.com/watch?v=FZbdGSILU_8",
                    "channel_name": "123 GO! Hindi",
                    "channel_link": "https://www.youtube.com/channel/UCClG8Br9HvIlgJEnP0GiJbQ",
                    "thumbnail_directory": "https://i.ytimg.com/vi/FZbdGSILU_8/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLC4JAzwmk28BFkXuQvzrHvrgLdS6A",
                    "video_duration": "10:01",
                    "partial_description": "\u092d\u0942\u0916 \u0932\u0917 \u0930\u0939\u0940 \u0939\u0948? \u092f\u0947 \u0915\u093f\u091a\u0928 \u092e\u0947 \u0915\u0941\u091b \u092b\u0947\u0902\u091f\u0928\u0947 \u0915\u093e \u0938\u092e\u092f \u0939\u0948!\u0932\u0947\u0915\u093f\u0928 \u0907\u0938\u0938\u0947 \u092a\u0939\u0932\u0947 \u0906\u092a \u0915\u0930\u0947 \u0939\u092e \u0915\u0941\u091b...",
                    "views": "2,668,440",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "HOLI Pranks - Types Of People In Holi | MyMissAnand",
                    "video_link": "https://www.youtube.com/watch?v=o9wbkcXbfvE",
                    "channel_name": "MyMissAnand",
                    "channel_link": "https://www.youtube.com/user/mymissanand",
                    "thumbnail_directory": "https://i.ytimg.com/vi/o9wbkcXbfvE/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBgqDMZJVyh9ZAh080Y_eBtFvLFig",
                    "video_duration": "7:47",
                    "partial_description": "Bura na Mano Holi Hai....\n\nHoli is just around the corner, the one festival where you can play some fun tricks, tease your friends & no one would mind. so here's the video full of fun, entertainmen...",
                    "views": "4,446,046",
                    "timestamp": "1 week ago"
                },
                {
                    "video_name": "\u090f\u0915\u0932\u0935\u094d\u092f (2020) \u0928\u094d\u092f\u0942 \u0930\u093f\u0932\u0940\u091c\u093c \u0939\u093f\u0902\u0926\u0940 \u0921\u092c \u092b\u093f\u0932\u094d\u092e | \u0928\u0908 \u0938\u093e\u0909\u0925 \u092e\u0942\u0935\u0940 \u0939\u093f\u0902\u0926\u0940 2020 | \u0939\u093f\u0902\u0926\u0940 \u092b\u093f\u0932\u094d\u092e 2020",
                    "video_link": "https://www.youtube.com/watch?v=UJp-nZjLMFw",
                    "channel_name": "Movies World",
                    "channel_link": "https://www.youtube.com/channel/UCMGjMeJknicOWxmZA_qADyA",
                    "thumbnail_directory": "https://i.ytimg.com/vi/UJp-nZjLMFw/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDC5ijdtsrAuXpChGVrxwek6VjDmg",
                    "video_duration": "2:00:46",
                    "partial_description": "",
                    "views": "24,496,804",
                    "timestamp": "1 week ago"
                }
            ],
            "target_type": "youtube_trends"
        }
        json_data = youtube_trends
        send_event('bigview_streams', 'youtube_trends', json_data)