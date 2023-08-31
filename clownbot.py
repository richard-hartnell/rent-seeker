#!/usr/bin/python
import praw
import pdb
import re
import os
import time

print("Running.")

commentIterator = 0
searchTerm = "clown"
subs = ['funny',
        'todayilearned',
        'music',
        'movies',
        'pics',
        'askreddit',
        'gaming',
        'videos',
        'books',
        'IAmA',
        'nottheonion',
        'explainlikeimfive',
        'lifeprotips',
        'futurology',
        'history',
        'nosleep',
        'documentaries',
        'tifu',
        'personalfinance',
        'technology',
        'unexpected',
        'travel',
        'facepalm',
        'mildlyinfuriating',
        # ban list below here
        # 'politics',
        # 'news',
        # 'worldnews',
        # 'memes',
        # 'gifs',
        # 'wallstreetbets',
        # 'therewasanattempt',
        ]
comments_found = []
reply_text = "Hi! Circus performer here. Just dipping in to clear up this too-frequent comparison between clowns and stupid people:\n \n" \
             "1. Clowns are very diligent and work very hard at refining their art.\n \n"\
             "2. Clowns are generally very kind and well-intentioned people.\n \n" \
             "3. Clowns are only *pretending* they are completely stupid.\n \n" \
             "-- \n \n" \
             "^(For a clownish rabbit hole, please enjoy this play written by Dario Fo, the only clown to win a Nobel Prize in Literature. https://www.youtube.com/watch?v=TqKfwC70YZI )"

reddit = praw.Reddit('bot1')
with open("comments_found.txt", "r") as f:
    comments_found = f.read()
    comments_found = comments_found.split("\n")
    comments_found = list(filter(None, comments_found))

with open("authors_found.txt", "r") as g:
    authors_found = g.read()
    authors_found = authors_found.split("\n")
    authors_found = list(filter(None, authors_found))

with open("skip_threads.txt", "r") as h:
    skip_threads = h.read()
    skip_threads = skip_threads.split("\n")
    skip_threads = list(filter(None, skip_threads))

while True:
    for sub in subs:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.hot(limit=20):
            time.sleep(2)
            commentIterator = 0
            submission.comments.replace_more(limit=3)
            for comment in submission.comments.list():
                if submission.id in skip_threads:
                    break
                # time.sleep(2)
                if commentIterator <= 12 and (str(searchTerm) in str(comment.body.lower())):
                    if "class clown" in str(comment.body.lower()):
                        break
                    commentIterator += 1
                    thisComment = reddit.comment(comment.id)
                    time.sleep(2)
                    if comment.id not in comments_found:
                        if str(comment.author) != 'clown_b0t':
                            print("\n From post in /r/" + subreddit.display_name + ": " + submission.title)
                            print("Comment " + str(commentIterator) + ": " + comment.body.lower())
                            if str(comment.author) in authors_found:
                                print('**************************Author found')
                            print("Author: " + str(comment.author))
                            prompt = input("Clownish reply? \n ('y' to reply, 'n' to ignore comment, '!' to ignore post, anything else to skip): ")
                            if prompt == "y":
                                try:
                                    thisComment.reply(reply_text)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "n":
                                comments_found.append(comment.id)
                                print("Comment ignored.")
                            if prompt == "!":
                                skip_threads.append(submission.id)
                                print("Post ignored.")
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
        with open("skip_threads.txt", "w") as h:
            for thread in skip_threads:
                h.write(thread + "\n")