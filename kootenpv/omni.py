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
