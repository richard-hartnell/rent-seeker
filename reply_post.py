#!/usr/bin/python
import praw
import pdb
import re
import os

#inits
commentIterator = 0
searchTerm = "clown"
subs = ['news',
        'politics',
        'worldnews',
        'askreddit',
        'gaming',
        'videos',
        'memes',
        'food',
        'books',
        'IAmA',
        'nottheonion',
        'explainlikeimfive',
        'lifeprotips',
        'gifs',
        'documentaries',
        'tifu',
        'personalfinance',
        'technology',
        'wallstreetbets',
        'unexpected',
        'therewasanattempt',
        'travel',
        'facepalm',
        'mildlyinfuriating',
        ]
comments_found = []
 
# the reply
reply_text = "Hi! Circus performer here. This account is for roaming around Reddit trying to clear up three important things about this too-frequent comparison between clowns and stupid people:\n \n" \
             "1. Clowns are very diligent and work very hard at refining their art.\n \n"\
             "2. Clowns are generally very kind and well-intentioned people.\n \n" \
             "3. Clowns are only *pretending* they are completely stupid.\n \n" \
             "-- \n \n" \
             "^For a clownish rabbit hole, please enjoy this play written by [Dario Fo](https://en.wikipedia.org/wiki/Dario_Fo), " + "the only clown to win a Nobel Prize in Literature." + "https://www.youtube.com/watch?v=TqKfwC70YZI"
test_comment = "Test comment."

# Create the Reddit instance
reddit = praw.Reddit('bot1')

with open("comments_found.txt", "r") as f:
    comments_found = f.read()
    comments_found = comments_found.split("\n")
    comments_found = list(filter(None, comments_found))

# let's pull comments from some subs!
while True:
    for sub in subs:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.hot(limit=20):
            commentIterator = 0
            print("\n Scanning post in /r/" + subreddit.display_name + ": " + submission.title)
            submission.comments.replace_more(limit=4)
            for comment in submission.comments.list():
                if commentIterator <= 12 and (str(searchTerm) in str(comment.body.lower())):
                    commentIterator += 1
                    thisComment = reddit.comment(comment.id)
                    if comment.id not in comments_found:
                        print("Comment " + str(commentIterator) + ": " + comment.body.lower())
                        prompt = input("Clownish reply? \n ('y' to comment, 'n' to never comment, anything else to skip): ")
                        if prompt == "y":
                            thisComment.reply(reply_text)
                            print("Comment left.")
                            comments_found.append(comment.id)
                        if prompt == "n":
                            comments_found.append(comment.id)
                            print("Comment ignored.")
                        else:
                            continue
                else:
                    pass

        # Write our updated list back to the file
        with open("comments_found.txt", "w") as f:
            for comment_id in comments_found:
                f.write(comment_id + "\n")