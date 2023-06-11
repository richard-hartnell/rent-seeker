#!/usr/bin/python
import praw
import pdb
import re
import os

#inits
commentIterator = 0
searchTerm = "i hope your own bot programming is going great"
subredditOfInterest = 'pythonforengineers'

# the reply
reply_text = "Hi! I'm clown_b0t, part of the circus. I roam Reddit trying to clear up three important things about this too-frequent comparison:\n \n" \
             "1. Clowns are very diligent and work exceedingly hard at refining their art.\n \n"\
             "2. Clowns are generally very kind and well-intentioned people.\n \n" \
             "3. Clowns are only *pretending* they are completely stupid.\n \n" \
             "I'm a bot! If anything's wrong, just reply to this comment."
    "[Dario Fo](https://en.wikipedia.org/wiki/Dario_Fo), " + "the only clown to win a Nobel Prize in Literature." + "https://www.youtube.com/watch?v=TqKfwC70YZI")

# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
#reddit.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# let's pull comments from some subs!
subreddit = reddit.subreddit(subredditOfInterest)
for submission in subreddit.hot(limit=10):
    commentIterator = 0
    print("Scanning post in /r/" + subreddit.display_name + ": " + submission.title)
    submission.comments.replace_more(limit=4)
    for comment in submission.comments.list():
        if commentIterator <= 12 and (str(searchTerm) in str(comment.body.lower())):
            commentIterator += 1
            print("Comment " + str(commentIterator) + ": " + comment.body.lower())
            thisComment = reddit.comment(comment.id)
            thisComment.reply(body="It's still working!")
            print("I think it worked.")
        else:
            pass

#     if submission.id not in posts_replied_to:
#             # submission.reply(reply_text)
#             print("Found: ", submission.title)
#             # Store the current id into our list
#             posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
