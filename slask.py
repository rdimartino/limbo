from flask import Flask, request
from pprint import pformat
import json
app = Flask(__name__)

import urllib2
from urllib import quote
import re
from random import shuffle

def gif(searchterm, unsafe=False):
    searchterm = quote(searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]
    result = opener.open(searchurl).read()

    gifs = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(gifs)

    return gifs[0] if gifs else ""

@app.route("/", methods=['POST'])
def hello():
    text = request.form.get("text", "")
    if text.startswith("!gif"):
        match = re.findall(r"!gif (.*)", text)
        term = match[0] if match else "dumb running sonic"
        return json.dumps({"text": gif(term), "parse": "full"})
    return ""

if __name__ == "__main__":
    app.run()
