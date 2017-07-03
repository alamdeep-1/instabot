
import requests,pylab

from acctoken import APP_ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()






def analyse_hashtag(insta_username):
    hash_item = {

    }
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s' % (user_id, APP_ACCESS_TOKEN))
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for x in range(0, len(user_media['data'])):
                my_tag_len = len(user_media['data'][x]['tags'])
                for y in range(0, my_tag_len):
                    # values of hashtag if coming twice in dictionary it will be updated to 2 as per its count value
                    if user_media['data'][x]['tags'][y] in hash_item:
                        hash_item[user_media['data'][x]['tags'][y]] += 1
                    else:
                        hash_item[user_media['data'][x]['tags'][y]] = 1
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

    print hash_item

    pylab.figure(1)
    # range is given to pylab which takes all the values in the dictionary
    x = range(len(hash_item))
    pylab.xticks(x, hash_item.keys())
    # 'g' adds color to the graph line
    pylab.plot(x, hash_item.values(), 'g')
    # pylabshow is used to finally display the graph
    pylab.show()


analyse_hashtag("deep.1_singh")