#!/usr/bin/python
import praw
import pdb
import re
import os
import time

print("Running.")

commentIterator = 0
searchTerms = ("the rent",
               "rents",
               "rent control",
               "housing provider",
               "free house",
               "housing crisis",
               "slumlord",
               "slum lord",)
exempt_terms = ["parents"]
subs = ['funny',
        'todayilearned',
        'music',
        'movies',
        'pics',
        'askreddit',
        'gaming',
        'books',
        'IAmA',
        'nottheonion',
        'explainlikeimfive',
        'lifeprotips',
        'history',
        'nosleep',
        'documentaries',
        'tifu',
        'personalfinance',
        'unexpected',
        'travel',
        'facepalm',
        'mildlyinfuriating',
        # prospective ban list below here
        'futurology',
        'technology',
        'politics',
        'news',
        'videos',
        'worldnews',
        'memes',
        'gifs',
        'wallstreetbets',
        'therewasanattempt',
        ]
comments_found = []
reply_text = ""
housing_provider_reply = ""
property_tax_reply = ""
rent_control_reply = ""
free_housing_reply = ""

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
                comment_body = str(comment.body.lower())
                if submission.id in skip_threads:
                    break
                # time.sleep(2)
                if commentIterator <= 12 and any(term in comment_body for term in searchTerms): #here is where we are searching searchTerm in the comment body
                    # for term in exempt_terms:
                    #     if term in str(comment.body.lower()):
                    #         print("Exempt comment skipped")
                    #         break
                    commentIterator += 1
                    thisComment = reddit.comment(comment.id)
                    time.sleep(2)
                    if comment.id not in comments_found:
                        if str(comment.author) != 'more_housing_co-ops':
                            print("\n From post in /r/" + subreddit.display_name + ": " + submission.title)
                            print("Comment " + str(commentIterator) + ": " + comment_body)
                            if str(comment.author) in authors_found:
                                print('**************************Author found')
                            print("Author: " + str(comment.author))
                            prompt = input("Clown? \n: ") #TODO: change this prompt and give numbered responses for various replies
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
                            if prompt == "d":
                                try:
                                    comment.downvote()
                                    print("Downvoted and ignored.")
                                    comments_found.append(comment.id)
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
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