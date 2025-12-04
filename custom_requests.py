import time
import requests
import os

DEBUG = True
url = "https://example.invalid:443/"
path1 = "path1"
path2 = "path2"

FAIL = "\033[91m"
GOOD = "\033[92m"
END = "\033[0m"

def error(text):
    print(FAIL + text + END)

def good(text):
    print(GOOD + text + END)


def store_response(name, user, resp):
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    user = user.replace(" ", "")

    if not os.path.exists("./responses"):
        os.makedirs("./responses")

    with open("responses/" + ts + "_" + name + "_" + user + ".html", "w") as f:
        f.write(resp.text)

def check_sess(resp):
    if resp.text.find("SESSIONERROR") != -1:
        error("FAIL")
        error("ErrorText: " + resp.json()["ErrorText"])
        print("[!] Exiting")
        exit(1)

def read_stuff(session, results):
    name = "read_stuff"
    user = session["user"]
    userid = session["userid"]
    sessid = session["sessid"]
    burp0_cookies = {"SID_" + userid: sessid}

    res = False
    resp = None
    print("[*] " + name + " as " + user + " (uid " + userid + ")")

    burp0_url = url + path1 + "?APPNAME=asdf&SID=" + sessid
    resp = requests.get(burp0_url, cookies=burp0_cookies, verify=False, allow_redirects=False)

    print("HTTP " + str(resp.status_code) + ", size: " + str(len(resp.text)) + ", ", end="")
    
    check_sess(resp)
    if resp.text.find("error_msg_text") != -1:
        error("FAIL")
        if DEBUG:
            error("[!] request failed with error_msg_text")
    if resp.text.find("goodstring") != -1:
        good("OK")
        res = True
        if DEBUG:
            print("[+] Stuff read")

    store_response(name, user, resp)
    results.append({ name: res })

def read_more_stuff(session, results):
    name = "read_more_stuff"
    user = session["user"]
    userid = session["userid"]
    sessid = session["sessid"]
    burp0_cookies = {"SID_" + userid: sessid}

    res = False
    resp = None
    print("[*] " + name + " as " + user + " (uid " + userid + ")")

    burp0_url = url + path1 + "?APPNAME=asdf&SID=" + sessid
    resp = requests.get(burp0_url, cookies=burp0_cookies, verify=False, allow_redirects=False)

    print("HTTP " + str(resp.status_code) + ", size: " + str(len(resp.text)) + ", ", end="")
    
    check_sess(resp)
    if resp.text.find("error_msg_text") != -1:
        error("FAIL")
        if DEBUG:
            error("[!] request failed with error_msg_text")
    if resp.text.find("goodstring") != -1:
        good("OK")
        res = True
        if DEBUG:
            print("[+] More stuff read")

    store_response(name, user, resp)
    results.append({ name: res })

def create_stuff(session, results):
    name = "create_stuff"
    user = session["user"]
    userid = session["userid"]
    sessid = session["sessid"]
    burp0_cookies = {"SID_" + userid: sessid}

    res = False
    resp = None
    print("[*] " + name + " as " + user + " (uid " + userid + ")")

    burp0_url = url + path1 + "?TS=1"
    burp0_data = {"APPNAME": "asdf", "SID": sessid, "text": "Test12345"}
    resp = requests.post(burp0_url, cookies=burp0_cookies, data=burp0_data, verify=False, allow_redirects=False)

    print("HTTP " + str(resp.status_code) + ", size: " + str(len(resp.text)) + ", ", end="")

    check_sess(resp)
    if resp.text.find("Test12345") != -1:
        good("OK")
        res = True
    else:
        error("FAIL")

    store_response(name, user, resp)
    results.append({ name: res })


def delete_user(session, results):
    name = "delete_user"
    user = session["user"]
    userid = session["userid"]
    sessid = session["sessid"]
    burp0_cookies = {"SID_" + userid: sessid}

    res = False
    resp = None
    print("[*] " + name + " as " + user + " (uid " + userid + ")")

    burp0_url = url + path1 + "?TS=1"
    burp0_data = {"APPNAME": "asdf", "action": "delete", "SID": sessid, "targetUser": session["user"]}
    resp = requests.post(burp0_url, cookies=burp0_cookies, data=burp0_data, verify=False, allow_redirects=False)

    print("HTTP " + str(resp.status_code) + ", size: " + str(len(resp.text)) + ", ", end="")

    check_sess(resp)
    if resp.text.find("deleted") != -1:
        good("OK")
        res = True
    else:
        error("FAIL")

    store_response(name, user, resp)
    results.append({ name: res })


# def ...
