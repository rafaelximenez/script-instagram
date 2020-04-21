import requests
import json
import time
from endpoints import endpoints
from credentials import credentials

class instaBot:
    def __init__(self):
        self.like_per_day = 1000
        self.time_in_day = 24*60*60
        self.like_delay = self.time_in_day / self.like_per_day
        self.more_than_likes = 10
        self.max_like_for_one_tag = 5
        self.log_mod = 0
        self.login_status = None
        self.media_by_tag = ['bjj']

        self.session = requests.Session()
        r = self.session.get(endpoints['base'])
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        
    
    def login(self, credentials):
        r = self.session.post(endpoints['login'], data=credentials, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        r = json.loads(r.content.decode('utf-8')) 
        if r['authenticated']:
            self.login_status = True
            self.user_id = r['userId']
        return r
    
    def get_userid(self, username):
        url = endpoints['user_info'] % username
        r = self.session.get(url)
        if r.status_code == 200:
            r = json.loads(r.content.decode('utf-8'))
            return r['graphql']['user']['id']
        return None

    def get_media_id_by_tag (self, tag):
        if (self.login_status):
            if (self.login_status):
                url_tag = endpoints['url_tag'] + tag + '/'
                try:
                    r = self.session.get(url_tag)
                    text = r.text

                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]                    
                    all_data = json.loads(json_str)
                    self.media_by_tag = list(all_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'])
                except Exception as e:
                    print('Erro ' + str(e))
                    time.sleep(3)
            else:
                return False
    
    def like_all_exist_media (self, media_size=-1):        
        if (self.login_status):
            if self.media_by_tag != 0:                
                i=0                
                for d in self.media_by_tag:       
                    url = endpoints['likes_photos'] % self.media_by_tag[i]['node']['id']
                    print(url)
                    r = self.session.post(url)
                    print(r.status_code)
                    i+=1                        
            else:
                print("Nenhuma foto curtida")


r = instaBot()
r.login(credentials)
#print(r.get_userid('bjj'))
r.get_media_id_by_tag('bjj')
r.like_all_exist_media()



