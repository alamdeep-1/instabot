import requests
from acctoken import APP_ACCESS_TOKEN
import matplotlib.pyplot as plt




def hash_tag():
    a=0
    labels=[]
    numbers=[]
    while a<5:

        hashtag = raw_input("your hashtag: ")
        request_url = ('https://api.instagram.com/v1/tags/%s?access_token=%s') % (hashtag, APP_ACCESS_TOKEN)

        print 'GET request url : %s' % (request_url)
        show_hash = requests.get(request_url).json()
        if show_hash['meta']['code'] == 200 :
            if len(show_hash['data']) :
                print "total hashtags of tag " + hashtag +": " + str(show_hash['data']['media_count'])
                labels .append((show_hash['data']['name']))
                numbers.append(show_hash["data"]["media_count"])
                #colors = ['gold', 'green']
                #explode = (0.1, 0)  # explode 1st slice
                # Plot

                a=a+1

            else:
                print 'no post with this tag'
        else:
            print 'Status code other than 200 received!'


    plt.pie(numbers, labels=labels, autopct='%1.1f%%', shadow=True,
            startangle=140)

    plt.axis('equal')
    plt.show()

hash_tag()