import requests
from acctoken import APP_ACCESS_TOKEN
import matplotlib.pyplot as plt






def hash_tag():
    a = 0
    tag_list = {}
    while a < 3:
        hashtag = raw_input("your hashtag: ")
        request_url = ('https://api.instagram.com/v1/tags/%s?access_token=%s') % (hashtag, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        show_hash = requests.get(request_url).json()
        if show_hash['meta']['code'] == 200:
            if len(show_hash['data']):
                print hashtag+":"+" "+ str(show_hash['data']['media_count'])
                tag_list.append(show_hash['data']['media_count'])
                a = a + 1
            else:
                print 'Status code other than 200 received!'
        else:
            exit()
    return tag_list



print hash_tag()



