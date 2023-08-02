#!/usr/bin/python
import praw
import pdb
import re
import os

#inits
commentIterator = 0
searchTerm = "clown"
subs = ['news',
        # 'politics',
        # 'worldnews',
        'askreddit',
        'gaming',
        'videos',
        'memes',
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
        # 'therewasanattempt',
        'travel',
        'facepalm',
        'mildlyinfuriating',
        ]
comments_found = []
 
# the reply
reply_text = "Hi! Circus performer here. Just dipping in to clear up this too-frequent comparison between clowns and stupid people:\n \n" \
             "1. Clowns are very diligent and work very hard at refining their art.\n \n"\
             "2. Clowns are generally very kind and well-intentioned people.\n \n" \
             "3. Clowns are only *pretending* they are completely stupid.\n \n" \
             "-- \n \n" \
             "^(For a clownish rabbit hole, please enjoy this play written by Dario Fo, the only clown to win a Nobel Prize in Literature. https://www.youtube.com/watch?v=TqKfwC70YZI )"
test_comment = "Test comment."

# Create the Reddit instance
reddit = praw.Reddit('bot1')

with open("comments_found.txt", "r") as f:
    comments_found = f.read()
    comments_found = comments_found.split("\n")
    comments_found = list(filter(None, comments_found))

with open("authors_found.txt", "r") as g:
    authors_found = g.read()
    authors_found = authors_found.split("\n")
    authors_found = list(filter(None, authors_found))

# let's pull comments from some subs!
while True:
    for sub in subs:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.hot(limit=20):
            time.sleep(2)
            commentIterator = 0
            print("\n Scanning post in /r/" + subreddit.display_name + ": " + submission.title)
            submission.comments.replace_more(limit=3)
            for comment in submission.comments.list():
                time.sleep(2)
                if commentIterator <= 12 and (str(searchTerm) in str(comment.body.lower())):
                    commentIterator += 1
                    thisComment = reddit.comment(comment.id)
                    time.sleep(2)
                    if comment.id not in comments_found:
                        if str(comment.author) != 'clown_b0t':
                            print("Comment " + str(commentIterator) + ": " + comment.body.lower())
                            if str(comment.author) in authors_found:
                                print('Author found')
                            print("Author: " + str(comment.author))
                            prompt = input("Clownish reply? \n ('y' to comment, 'n' to never comment, anything else to skip): ")
                            if prompt == "y":
                                thisComment.reply(reply_text)
                                print("Comment left.")
                                comments_found.append(comment.id)
                                authors_found.append(str(comment.author))
                            if prompt == "n":
                                comments_found.append(comment.id)
                                print("Comment ignored.")
                            else:
                                continue
                else:
                    pass
        with open("comments_found.txt", "w") as f:
            for comment_id in comments_found:
                f.write(comment_id + "\n")
        with open("authors_found.txt", "w") as g:
            for author in authors_found:
                g.write(author + "\n")