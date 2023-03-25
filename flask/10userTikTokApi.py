from TikTokApi import TikTokApi

# Initialize the TikTokAPI object
api = TikTokApi()

# Set the username of the content creator whose latest posts we want to retrieve
username = "gin3344"

# Get the TikTok user object for the specified username
# user = api.getUser(username)

# # Get the list of the user's latest posts
# latest_posts = api.byUsername(username, count=10)

# Loop through each post and print its view count
for post in api.user(username="therock").videos():
    print(f"Post ID: {post['id']}")
    print(f"Views: {post['stats']['playCount']}")
    print("------------")
