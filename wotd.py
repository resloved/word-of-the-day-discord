import discord, asyncio, requests, datetime

# -- INIT --

POST_TIME_H = 6
POST_TIME_M = 0
POST_TIME_S = 0

BOT_EMAIL = ''
BOT_PASS = ''

KEY = ''

CHAN_ID = ''

# Connect to client
client = discord.Client()


def apiGet(url):
    response = requests.get(url)
    return response.json()


def randomWord():
    url = "http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=0&\
	maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&api_key=" + KEY
    data = apiGet(url)
    return data["word"]


def defLook(word):
    url = "http://api.wordnik.com:80/v4/word.json/" + word +\
    "/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=" + KEY
    data = apiGet(url)
    if len(data) == 0:
        return ""
    else:
        return data[0]["text"]


def post(word, definition):
    return  "**WORD OF THE DAY: " + word + "**\n" +\
            "*Def - " + definition + "*"


def toWait(time):
    base = 86400
    h = time.hour - POST_TIME_H
    m = time.minute - POST_TIME_M
    s = time.second - POST_TIME_S
    dif = (h * 60 * 60) + (m * 60) + s
    if dif < 0:
        return abs(dif)
    else:
        return base - dif

# -- START --
@asyncio.coroutine
def my_background_task():
    lastPin = None
    yield from client.wait_until_ready()
    print("-- Task Started --")
    chan = discord.Object(id=CHAN_ID)
    while not client.is_closed:
        print("-- Selecting Word --")
        # Pull word from toread
        word = randomWord()
        # Pull def
        definition = defLook(word)
        print(word)
        print(definition)
        # Input word and def into proper format
        toPost = post(word, definition)
        # Calculate time til post time
        now = datetime.datetime.now()
        timeToWait = toWait(now)
        print("-- READY AT: {0} --".format(now))
        print("-- WAITING FOR: {0}s --".format(timeToWait))
        # Wait
        yield from asyncio.sleep(timeToWait)
        # Unpin last message
        if lastPin is not None:
            client.unpin_message(lastPin)
        # Post to client
        lastPin = yield from client.send_message(chan, toPost)
        # Pin new message
        client.pin_message(lastPin)
# -- END --

@asyncio.coroutine
def test_post():
    print("-- TEST --")
    yield from client.wait_until_ready()
    yield from client.send_message(CHAN_ID, "test")

# -- RUN --
# client.loop.create_task(my_background_task())
client.async_event(test_post)
client.run(BOT_EMAIL, BOT_PASS)
