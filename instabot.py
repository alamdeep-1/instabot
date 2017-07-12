#INSTABOT 7.
import requests,urllib,pylab,colorama
from textblob import TextBlob
from termcolor import *
from textblob.sentiments import NaiveBayesAnalyzer

# matplotlib is used to draw graph and wordcloud is used to draw  word image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from acctoken import APP_ACCESS_TOKEN
colorama.init()

BASE_URL = 'https://api.instagram.com/v1/'

#defining function for getting users own details
def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print 'Username: %s' % (user_info['data']['username'])
      print 'Name: %s' % (user_info['data']['full_name'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'User does not exist!'
  else:
    print 'Status code other than 200 received!'

#defining function searching a user & getting its id.
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

#getting information of other user.
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Full Name: %s' % (user_info['data']['full_name'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

#for downloading own post.
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            n_th_photo = int(raw_input("which photo"))
            image_name = own_media['data'][n_th_photo]['id'] + '.jpeg'
            image_url = own_media['data'][n_th_photo]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#function for downloading other users post.
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            n_th_photo = int(raw_input("which photo: "))
            image_name = user_media['data'][n_th_photo]['id'] + '.jpeg'
            image_url = user_media['data'][n_th_photo]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'



#Function for liking users post.
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'



#defining fuction for making comment on users post.
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#Function to get the list of users who liked post.
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    users_info = requests.get(request_url).json()
    i = 0
    if users_info['meta']['code'] == 200:
        if len(users_info['data']):
            for ele in users_info['data']:
                print (users_info['data'][i]['username'])
                i = i + 1
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



#Function to get list of users who commented in post.
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print "get request url: %s" % (request_url)
    comment_info = requests.get(request_url).json()
    i = 0
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for ele in comment_info['data']:
                print (comment_info['data'][i]['text'])
                print (comment_info['data'][i]['from']['username'])
                i = i+1
            else:
                print 'user does not exist'
        else:
            print 'status code other than 200 is recieved!'


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'



#No of images with popular hashtag.
def analyse_hashtag(insta_username):
    hash_item = {}
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

#plotting hastags using malplotlib.
    pylab.figure(1)
    # range is given to pylab which takes all the values in the dictionary
    x = range(len(hash_item))
    pylab.xticks(x, hash_item.keys())
    # 'g' adds color to the graph line
    pylab.plot(x, hash_item.values(), 'g')
    # pylabshow is used to finally display the graph
    pylab.show()
    # this code will create a wordcloud of hashtags stores in dictionary
    wordcloud = WordCloud(background_color='white', mode='RGB', width=2000, height=1000).generate_from_frequencies(
        hash_item)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

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

#organising all calling functions.
def start_bot():
    a=True
    while a:
        print '\n'
        cprint ('Hey! Welcome to instaBot!',"red")
        cprint ('Here are your menu options:\n',"blue")
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.like users post"
        print "f.Make a comment on the recent post of a user"
        print "g.Get a list of people who have liked the recent post of a user"
        print "h.Get a list of people who have commented on recent post of a user"
        print "i.Delete negative comments from the recent post of a user"
        print "j.Show hashtag of user & plot it,"
        print "k.show popular hashtag"
        cprint ("l.EXIT\n","red")

        choice = raw_input("Enter you choice: ")
        if choice == "a":
          self_info()

        elif choice == "b":
          insta_username = raw_input("Enter the username of the user: ")
          if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
              cprint('Username not valid in instagram!!!', "red")
          else:
              get_user_info(insta_username)

        elif choice == "c":
          get_own_post()

        elif choice == "d":
          insta_username = raw_input("Enter the username of the user: ")
          if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
              cprint('Add a valid name!', 'green')
          else:
              get_user_post(insta_username)


        elif choice == "e":
          insta_username = raw_input("Enter the username of the user: ")
          if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
              cprint('Add a valid name!', 'blue')
          else:
              like_a_post(insta_username)

        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Add a valid name!', 'green')
            else:
                post_a_comment(insta_username)


        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Add a valid name!', 'green')
            else:
                get_like_list(insta_username)


        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Add a valid name!', 'red')
            else:
                get_comment_list(insta_username)


        elif choice == "j":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Add a valid name!', "green")
            else:
                analyse_hashtag(insta_username)


        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                cprint('Add a valid name!', "red")
            else:
                delete_negative_comment(insta_username)

        elif choice == "k":
            hash_tag()

        elif choice == "l":
          exit()

        else:
            a=False
            print "wrong choice"

start_bot()