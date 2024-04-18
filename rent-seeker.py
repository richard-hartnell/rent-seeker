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
        'aboringdystopia',
        'lostgeneration',
        'democraticsocialism',
        'askaliberal',
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
housing_provider_reply = "Someone who buys housing at cost and returns it to the market for 2x the price isn't 'providing' anything."
property_tax_reply = "Casual reminder that property tax usually only makes up around 10 percent of market-rate rent, compared to the ~fifty percent of rent that goes toward paying off the landlord's mortgage for them"
rent_control_reply = "Most economists might argue against rent control, but if you actually read the most commonly cited anti-rent-control papers, they find that rent control typically protects tenants from displacement and reduces homelessness -- and that when net rent increases result, they come about from scalpers going elsewhere in the market to gouge unprotected tenants *worse*."
free_housing_reply = "Landlords love to accuse housing advocates of trying to 'give away free housing' every time they suggest that landlords should pay their own purchase price and not charge 2x the real cost of housing."
GDP_reply = "Another good place to note that exploding rent costs are included in GDP, even though nothing is produced by scalping a home."

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
                    if any(term in comment_body for term in exempt_terms):
                        print("Exempt comment skipped")
                        break
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
                            prompt = input("1: 'Housing provider' \n 2: 'Property tax' \n 3: 'Rent control doesn't work' \n 4: 'Free house' \n 5: 'GDP' \n n: No reply \n d: Downvote, no reply \n !: ignore thread \n c: Custom reply \n Action?: ") #TODO: change this prompt and give numbered responses for various replies
                            if prompt == "1":
                                try:
                                    thisComment.reply(housing_provider_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "2":
                                try:
                                    thisComment.reply(property_tax_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "3":
                                try:
                                    thisComment.reply(rent_control_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "4":
                                try:
                                    thisComment.reply(free_housing_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "5":
                                try:
                                    thisComment.reply(GDP_reply)
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
                            if prompt == "c":
                                custom_reply = input("Custom reply: ")
                                try:
                                    thisComment.reply(custom_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
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