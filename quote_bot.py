# bot that makes showerthoughts
from typing import List
import pytumblr
import dotenv
import openai

# OpenAI
openai.api_key = dotenv.get_key("keys.env", "OPENAI_KEY")

gpt3prompt = """
Shower Thoughts
1. Telling someone to “turn the AC down” can be interpreted as both make it hotter or make it colder.
2. If you're carrying a pizza, you can get into almost any building.
3. The olympic pool probably have the lowest pee/water ratio of any public owned pool.
4. Professors are human programmers. Psychologists are human debuggers.
5. Being a woman on the internet is half convincing people you’re not a bot and half convincing people you’re not a prostitute.
6. The smarter you get by reading and experience, the lonlier and crazier you become as you see more stupidity in your midst.
"""

def generateQuotes(num: int) -> List[str]:
    # Max num of 4. This is an expensive API.
    num = max(0, min(num, 4))
    if num == 0:
        return []
    response = openai.Completion.create(
        engine="davinci",
        prompt=gpt3prompt,
        temperature=0.75,
        max_tokens=32 * num,
        top_p=1,
        frequency_penalty=0.32,
        presence_penalty=0.66,
        stop=[f"{6 + num + 1}."]
    )
    data = response["choices"][0]
    text: str = data["text"]
    lines = text.splitlines()
    lines = [line.split(". ", maxsplit=1)[1] for line in lines]
    # If we didn't get enough text, cut off the end and request the rest as new quotes.
    if data["finish_reason"] == "length":
        lines.pop()
        lines.extend(generateQuotes(num - len(lines)))
    return lines
print(generateQuotes(4))
quit()
# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    # insert keys here
)

# Make the request
client.info()

trigger_words = {
    "gun": "gun tw",
    "death": "death tw",
    "kill": "death tw",
    "food": "food tw",
    "life": "unreality tw",
    "dream": "unreality tw"
}

# Generate text
generate = int(input('Number of posts to generate (max 4 at a time): '))
print("Waiting...")
quotes = generateQuotes(generate)

# Prepare the text posts
class stPost:
    def __init__(self, quote: str, tags: List[str] = []):
        self.quote = quote
        self.tags = set(['bot thoughts', 'shower thoughts', 'bot generated post', 'thoughts from the shower'])
        self.tags.update(tags)
    def send(self):
        client.create_text('just-bot-shower-thoughts', state='queue', body=self.quote, tags=self.tags)
    def __str__(self):
        return f"'{self.quote}' | {self.tags}"
posts: List[stPost] = []
for quote in quotes:
    post = stPost(quote)
    for word in quote.split(' '):
        if word in trigger_words:
            post.tags.append(trigger_words[word])
    # Allow user to modify tags or delete
    print("\nModify tags and trigger warnings before posting for quote:")
    print(quote)
    print(" To continue: READY")
    print(" To delete post (suggested if very offensive): DELETE")
    print(" To list existing tags: TAGS")
    print(" To add/remove tags, just type them and press enter.")
    while True:
        command = input("> ").strip()
        if command == "":
            continue
        elif command == "READY":
            posts.append(post)
            break
        elif command == "DELETE":
            print("Deleted post. It will not be included during upload.")
            break
        elif command == "TAGS":
            print(post.tags)
        else:
            if command in post.tags:
                post.tags.remove(command)
                print(f"Removed tag '{command}'. New tag list: {post.tags}")
            else:
                post.tags.add(command)
                print(f"Added tag '{command}'. New tag list: {post.tags}")
print("\nConfirm sending posts:")
for post in posts:
    print(post)
if input("(y/n): ").lower() in ["y", "yes"]:
    for post in posts:
        post.send()
else:
    print("Modification at this stage has not been implemented. You may manually post quotes if this was a mistake.")