#!/usr/bin/python
import praw
import pdb
import re
import os

#inits
commentIterator = 0
searchTerm = "meatbag"
subs = ['pythonforengineers']
comments_found = []

# the reply
reply_text = "Hi! Circus performer here. This account roams Reddit trying to clear up three important things about this too-frequent comparison:\n \n" \
             "1. Clowns are very diligent and work very hard at refining their art.\n \n"\
             "2. Clowns are generally very kind and well-intentioned people.\n \n" \
             "3. Clowns are only *pretending* they are completely stupid.\n \n" \
             "^Your comment was searched for automatically, but this post was made manually." \
             "^For a clownish rabbit hole, please enjoy an antifascist play by [Dario Fo](https://en.wikipedia.org/wiki/Dario_Fo), " + "the only clown to win a Nobel Prize in Literature." + "https://www.youtube.com/watch?v=TqKfwC70YZI"
reply_text_2 = "Test comment."

# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
# with open("creds.txt", "r") as f:
#     reddit.login(f[0], f[1])

# if not os.path.isfile("comments_found.txt"):
#     comments_found = []

with open("comments_found.txt", "r") as f:
    comments_found = f.read()
    comments_found = comments_found.split("\n")
    comments_found = list(filter(None, comments_found))

# let's pull comments from some subs!
for sub in subs:
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.hot(limit=10):
        commentIterator = 0
        print("\n Scanning post in /r/" + subreddit.display_name + ": " + submission.title)
        submission.comments.replace_more(limit=4)
        for comment in submission.comments.list():
            if commentIterator <= 12 and (str(searchTerm) in str(comment.body.lower())):
                commentIterator += 1
                print("Comment " + str(commentIterator) + ": " + comment.body.lower())
                thisComment = reddit.comment(comment.id)
                if comment.id not in comments_found:
                    # thisComment.reply(reply_text_2)
                    # print("Test submission")
                    print("Comment id:" + comment.id)
                    comments_found.append(comment.id)
                # thisComment.reply(body="It's still working!") // here's the reaction
            else:
                pass

    # Write our updated list back to the file
    with open("comments_found.txt", "w") as f:
        for comment_id in comments_found:
            f.write(comment_id + "\n")