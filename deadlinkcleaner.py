import praw
from googleapiclient.discovery import build
import requests

# Two variables--one to hold your api key and another to hold a youtube access

api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
youtube = build("youtube", "v3", developerKey=api_key)

# Two variables--one to hold website credentials and another to hold website access

creds = {"client_id": "xxxxxxxxxxxxxx",
         "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "user_agent": "Remove dead links",
         "username": "bot_flairy"}

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

# Make a list called submissions and fill it with submissions from the movie group

submissions = []
for submission in reddit.subreddit("name_of_the_subreddit").__getattribute__("new")(limit=1000):

    # Only add submissions that include a youtube link

    if "youtu" in submission.url:
        submissions.append(submission)

for submission in submissions:

    # Make a variable to hold submission.url

    url = submission.url

    # Inspect if the url is a youtube.com, m/youtube.com, or youtu.be link and get the 11 character id

    if "=" in url:
        url = url.split("=")
        url = url[1]
    else:
        url = url.split("/")
        url = url[3]

    # Clip off anything after the 11 character id

    url = url[:11]

    # Using your developer key, get the status of the video's id

    url = f'https://www.googleapis.com/youtube/v3/videos?id={url}&key={api_key}&part=status'
    url_get = requests.get(url)

    # Clean up and parse the output

    url_get = str(url_get.json())
    url_get = url_get.split("'items': [")
    url_get = url_get[1]

    # Videos that have been removed  will have the "]" character in the sequence

    if url_get[0] == "]":

        # Print the submission title and a short message that video has been removed

        print(submission.title + "\nNot here anymore.")

        # Take the submission with the dead link and as a mod, remove it

        submission.mod.remove()






