# Omni Challenge: kootenpv

In this Omni Challenge, the omni.py script will share the users' localhost with a remote PC (loco).

On the remote PC it will be possible to access "localhost:4000/omni/do_all" as a result of (aserve).

That route will run the `do_all` function, which will conveniently scrape and convert from a html tree to only text (requests_viewer).

From this text, (natura) will extract Money objects that can be converted to dictionaries.

A list of dictionaries is conveniently written to file by (just).

(yagmail) will send an email attaching the json file, and as contents have some html.

Finally, (whereami) will return where the original PC is located at, as a web response.

## Setup:

    pip install natura just yagmail loco aserve requests_viewer whereami

Assumes:

- yagmail: that you have setup .yagmail file and password in keyring
- whereami: you have trained the machine learning model at least on 1 location
- aserve: only works on python 3 (the rest also on py2)
- loco: assumes `loco0` user exists by `loco create` on remote machine

## Script

```python
from natura import Finder                                 # https://github.com/kootenpv/natura
import just                                               # https://github.com/kootenpv/just
import yagmail                                            # https://github.com/kootenpv/yagmail
from loco import loco                                     # https://github.com/kootenpv/loco
import aserve                                             # https://github.com/kootenpv/aserve
import requests_viewer.web                                # https://github.com/kootenpv/requests_viewer
from whereami.predict import predict as predict_location  # https://github.com/kootenpv/whereami


def do_all():
    url = "http://www.infiniteunknown.net/2009/01/03/chancellor-alistair-darling-on-brink-of-second-bailout-for-banks/"
    # request url and extract text only from html tree
    html2 = requests_viewer.web.get_tree(url).text_content()
    # find all money and converted into base currency (EUR/USD), such as "$2 Trillion"
    money = Finder().findall(html2)
    # one-liner to conveniently write json file
    just.write([x.to_dict() for x in money], "money.json")
    # send email with html content and a json attachment. yagmail avoids need
    # of username/password in script
    yagmail.SMTP().send(subject=":)", contents="<h1>Hi there</h1> see attach",
                        attachments=["money.json"])
    # find the location of this machine (trained through machine learning)
    return predict_location()  # returns e.g. "couch" as web response

if __name__ == "__main__":
    try:
        # Start a tunnel in the background; sharing what is on my localhost:52222
        # with my other machine (ssh alias/config is "locolan")
        loco.cast(["locolan", "--background"])
    except SystemExit:
        print("actually, already listening")
    # Start a webserver which loads all the functions in a file (fun: this file in this case)
    # It will be automatically served like localhost:4000/omni/do_all
    aserve.main(["omni.py", "--port", "52222"])
```
