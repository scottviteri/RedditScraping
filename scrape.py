import requests
import time
import csv
from bs4 import BeautifulSoup

subreddit_name = "datascience" #"science"
num_posts_desired = 100

def getNextPage(soup, num_posts):
    next_button = soup.find("span", class_="next-button")
    if not next_button: #if cannot get next_button, just pattern match on the url
        print "Next button not found"
        guessed_url = "https://old.reddit.com/r/" \
                        + subreddit_name + "/?count=" \
                        + str(num_posts) + "&after=t3_9opdvw"
        return requests.get(guessed_url, headers={'User-Agent': 'Mozilla/5.0'})
    next_page_link = next_button.find("a").attrs['href']
    time.sleep(1) #avoid spamming reddit's servers
    return requests.get(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})

def removeDuplicates(lst):
    return [x for x in lst if lst.count(x)==1]

def scrapePosts(url, num_posts_desired):
    posts = []
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    while len(posts) < num_posts_desired:
        soup = BeautifulSoup(page.text, 'html.parser')
        if len(posts) != 0:
            page = getNextPage(soup, len(posts))    
        print(len(posts))
        posts_including_promoted = soup.find_all("div", class_="thing")
        non_promotion_posts = filter(lambda post : 'promoted' not in post.get("class"), posts_including_promoted)
        posts.extend(non_promotion_posts)
    return removeDuplicates(posts)[:num_posts_desired]

def checkInbound(post):
    ## Make sure that post is local to the current subreddit
    title = post.find("p", class_="title")
    child_a = title.findChild(name="span", attrs={"class":"domain"}).a 
    if child_a is None: 
        return False
    child_text = child_a.text
    return (child_text is not None) and (child_text == "self."+subreddit_name) 

url = "https://old.reddit.com/r/"+subreddit_name+"/"
posts = scrapePosts(url, num_posts_desired)
#inbound_posts = filter(checkInbound, posts) #optional filter
inbound_posts = posts[::]
titles = map(lambda post : post.find('p', class_="title").text.encode('utf-8'), inbound_posts)
authors = map(
            lambda post : post.find('a', class_="author").text.encode('utf-8') \
                            if post.find('a', class_="author") else "Deleted", 
            inbound_posts)
num_comments_strings = map(lambda post : post.find('a', class_="comments").text, inbound_posts)

def convertCommentCountStringToNum(num_comments_string):
    """ Example inputs -> outputs:
    u'130 comments' -> 130
    u'17 comments' -> 17
    u'comment' -> 0
    u'1 comment' -> 1
    """
    words = num_comments_string.split(' ')
    return int(words[0]) if len(words) == 2 else 0

num_comments = map(convertCommentCountStringToNum, num_comments_strings)
string_likes = map(lambda post : post.find("div", attrs={"class": "score likes"}).text, inbound_posts) 

def convertLikesStringToNum(string_like):
    """Example inputs -> outputs
    u'272' -> 272
    u'o' -> 0
    u'30.6k' -> 30600
    """
    if not string_like[0].isdigit(): return 0
    if 'k' in string_like:
        before_decimal, after_decimal = string_like[:-1].split('.')
        string_like = before_decimal + after_decimal + '0'*(3-len(after_decimal)) 
    return int(string_like) 

num_likes = map(convertLikesStringToNum, string_likes)
results = zip(titles, authors, num_comments, num_likes)

with open('scraped.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title","Author","Number of Comments","Number of Likes"])
    for result in results: 
        writer.writerow(result)
