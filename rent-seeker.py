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
               "provide housing",
               "providing housing",
               "without landlords",
               "free house",
               "housing crisis",
               "slumlord",
               "slum lord",
               "landlord")
exempt_terms = ["parents",
                "currents",]
subs = ['funny',
        'renters',
        'internationalnews',
        'aboringdystopia',
        'lostgeneration',
        'democraticsocialism',
        'amitheasshole',
        'askaliberal',
        'todayilearned',
        'economics',
        'ezraklein',
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
        'upliftingnews',
        'science',
        'askscience',
        'bestof',
        'dataisbeautiful',
        'gifs',
        'mildlyinteresting',
        'trashy',
        'anythinggoesnews',
        'tiktokcringe',
        # prospective ban list below here
        'futurology',
        # 'technology',
        'politics',
        'news',
        'videos',
        # 'worldnews',
        'memes',
        'gifs',
        'wallstreetbets',
        'therewasanattempt',
        ]

comments_found = []
housing_provider_reply = "Someone who buys housing at cost and returns it to the market for 2x the price isn't 'providing' anything."
property_tax_reply = "Property tax usually only makes up around 10 percent of market-rate rent, compared to the ~fifty percent of rent that goes toward paying off the landlord's mortgage for them"
rent_control_reply = "Most economists might argue against rent control, but when you ask them to explain their argument it's most often 'most economists don't like rent control.' If you actually read the most commonly cited anti-rent-control papers, they show renter protections shielding tenants from displacement, reducing homelessness, and making housing affordable again -- and that if/when net rent increases result, they come about from scalpers going elsewhere in the market to gouge unprotected tenants *worse*."
free_housing_reply = "Landlords love to accuse housing advocates of trying to 'give away free housing' every time they suggest that landlords should pay their own purchase price and not charge 2x the real cost of housing."
GDP_reply = "Another good place to note that exploding rent costs are included in GDP, even though nothing is produced by scalping a home."
without_LLs_reply = "Private landlords love to argue that without scalping, there would be no rental housing. But just because they don't know (or would prefer not to think) about alternative models, many exist that manage to beat private landlords' rates by about 50%: housing coops, land trusts, etc."
property_rights_reply = "Landlords frequently argue that no laws can/should affect what people can do with their private property, as if there aren't already laws on the books saying you can't stab someone with a knife even if it's *your* knife."
vienna_model_reply = "Vienna famously bought back swaths of scalped housing and successfully reduced rent by like 50 percent as a result. https://www.google.com/search?q=vienna+model"
moms_pops_reply = "I don't think it matters much whether 10000 otherwise-affordable units are getting scalped for twice the price by two giant companies or by a couple thousand 'moms' and 'pops.'"
model_reply = "It turns out that cutting out the landlord can reduce rental costs by ~50%. Here's one cooperative model that offers a rebate to tenants for paying off the house: https://www.dissolvingequity.org"
tax_landlords_reply = "Unfortunately, taxes and fees designed to discourage the mass scalping of housing usually just get passed on to tenants. IMO more blanket prohibition and/or public programs like the Vienna Model are key"

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
                comment_body = str(comment.body.lower()) #try .encode('utf-8') maybe
                if submission.id in skip_threads:
                    break
                # time.sleep(2)
                if commentIterator <= 12 and any(term in comment_body for term in searchTerms):
                    if any(term in comment_body for term in exempt_terms):
                        print("Exempt comment skipped")
                        break
                    commentIterator += 1
                    thisComment = reddit.comment(comment.id)
                    time.sleep(2)
                    if comment.id not in comments_found:
                        if str(comment.author) != 'more_housing_co-ops':
                            if str(comment.author) in authors_found:
                                print('**************************Author found')
                            print("Author: " + str(comment.author))
                            print("1: " + housing_provider_reply + "\n")
                            print("2: " + property_tax_reply + "\n")
                            print("3: " + rent_control_reply + "\n")
                            print("4: " + free_housing_reply + "\n")
                            print("5: " + GDP_reply + "\n")
                            print("6: " + property_rights_reply + "\n")
                            print("7: " + tax_landlords_reply + "\n")
                            print("8: " + vienna_model_reply + "\n")
                            print("9: " + without_LLs_reply + "\n")
                            print("0: " + moms_pops_reply + "\n")
                            print("n: No reply \n")
                            print("d: Downvote and ignore\n")
                            print("u: Upvote and ignore\n")
                            print("!: Ignore thread \n")
                            print("c: Custom Reply \n")
                            print("\n From post in /r/" + subreddit.display_name + ": " + submission.title)
                            print("Comment " + str(commentIterator) + ": " + comment_body)
                            prompt = input("Action?: ")
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
                            if prompt == "6":
                                try:
                                    thisComment.reply(property_rights_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "7":
                                try:
                                    thisComment.reply(wealth_redistribution_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "8":
                                try:
                                    thisComment.reply(vienna_model_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "9":
                                try:
                                    thisComment.reply(without_LLs_reply)
                                    print("Comment left.")
                                    comments_found.append(comment.id)
                                    authors_found.append(str(comment.author))
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
                            if prompt == "n":
                                comments_found.append(comment.id)
                                print("Comment ignored.")
                            if prompt == "u":
                                try:
                                    comment.upvote()
                                    print("Upvoted and ignored.")
                                    comments_found.append(comment.id)
                                except Exception as e:
                                    print(e)
                                    comments_found.append(comment.id)
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
                                    if custom_reply == "":
                                        print("No reply left.")
                                    else: 
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