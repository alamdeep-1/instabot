import requests
from acctoken import APP_ACCESS_TOKEN
import matplotlib.pyplot as plt






def hash_tag():
    a = 0
    tag_list = []
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




explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(hash_tag(), autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


