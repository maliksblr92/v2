#from Public_Data_Acquisition_Unit.acquistion_manager import *
from Public_Data_Acquisition_Unit.mongo_models import *


#first need to create all the supported sites reffernce in db

supported_sites_content = [{
'website':
{'name':'Facebook',
 'url':'www.facebook.com',
 'website_type':'social',
 'target_type':['profile',
                'page',
                'group'
                ],
'recursive_crawling':True

}},{'website':
{'name':'Twitter',
 'url':'www.twitter.com',
 'website_type':'social',
 'target_type':['profile'],
 'recursive_crawling':True

}},{'website':
        {'name': 'Instagram',
         'url': 'www.instagram.com',
         'website_type': 'social',
         'target_type': ['profile'],
'recursive_crawling':True

}},{'website':
    {'name':'Linkedin',
     'url':'www.linkedin.com',
     'website_type':'social',
     'target_type':['profile','company'],
'recursive_crawling':False

}},{'website':
    {'name':'custom',
     'url':'',
     'website_type':'fake',
     'target_type':['keybase_crawling','dynamic_crawling'],
'recursive_crawling':False

}},{'website':
    {'name':'Reddit',
     'url':'',
     'website_type':'social',
     'target_type':['profile','subreddit'],
'recursive_crawling':False
    }
},{'website':
    {'name':'Youtube',
     'url':'',
     'website_type':'blog',
     'target_type':['channel'],
'recursive_crawling':False

    }
}]



for website in supported_sites_content:
    #print(website)
    website = website['website']
    #print(website['name'],website[''],website['name'],website['name'])
    sw = Supported_Website(name=website['name'],url=website['url'],website_type=website['website_type'],target_type=website['target_type'],recursive_crawling=website['recursive_crawling'])
    sw.save()
    print('social site created')