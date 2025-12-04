#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import requests
from custom_requests import *

DEBUG = True
renewSessions = False   # or load old sessions from file
runTests = False
url = "https://example.invalid:443/"
path1 = "path1"
path2 = "path2"

accounts = {
    "Company Admin": "password",
    "Configuration Admin": "password",
    "System Admin": "password",
    "Manager": "password",
    "Standard": "password",
    "System Operator": "password",
    "User Editor": "password"
}
sessions = []
results = []
FAIL = "\033[91m"
GOOD = "\033[92m"
END = "\033[0m"

def error(text):
    print(FAIL + text + END)

def good(text):
    print(GOOD + text + END)

def pretty(d):
    return json.dumps(d.json(), indent=4)

# 1. get sessions
def get_sessions():
    print("[*] Getting Sessions")
    global sessions

    for user, password in accounts.items():
        session = {}

        burp0_data = {"HEADER": "content", "username": user, "password_input": password}
        resp = requests.post(url + path1, data=burp0_data, verify=False, allow_redirects=False)
        dat = resp.json()
        userid = dat.get('userId')
        sessid = dat.get('sessionId')

        session['user'] = user
        session['password'] = password
        session['userid'] = userid
        session['sessid'] = sessid
        if int(userid) > 0:
            sessions.append(session)
        else:
            error("[!] Could not get session for user " + user)
            continue

        if DEBUG:
            out = "User: " + user + " Password: " + password + " UserID: " + userid + " SessionID: " + sessid
            print(out)
            print(resp.headers.get('Set-cookie'))
    
    with open('sessions.json', 'w') as f:
        json.dump(sessions, f)

# 2. run test requests
def run_tests():
    global sessions
    err = False

    if not renewSessions:
        sessions = []
        # load old sessions from file
        with open("sessions.json", "r") as f:
            sessions = json.load(f)
    
    for session in sessions:
        user = session["user"]
        userid = session["userid"]
        sessid = session["sessid"]
        if DEBUG:
            print("[*] Running test request as user " + user + " (uid " + userid + ")")

        # test request if session is valid
        para = "?APPNAME=asdf&UID=" + userid + "&SID=" + sessid
        burp0_cookies = {"SID_" + userid: sessid}
        resp = requests.get(url + path1 + para, cookies=burp0_cookies, verify=False, allow_redirects=False)

        #print(pretty(resp))

        if resp.status_code != 200 or resp.text.find("SESSIONERROR") != -1:
            err = True
            dat = resp.json()
            error("[!] Test request unsuccessful (HTTP " + str(resp.status_code) + ", " + dat["ErrorText"] + ")")

    if err:
        error("[!] At least one session is invalid, exiting")
        exit(1)

# 3. run requests
def run_requests():
    global sessions, results
    i = 0

    if not renewSessions:
        sessions = []
        # load sessions from file
        with open("sessions.json", "r") as f:
            sessions = json.load(f)
    
    for session in sessions:
        i += 1
        ###################################################################

        # 1 custom request a
        read_stuff(session, results)

        # 2 custom request b
        read_more_stuff(session, results)

        # 3 custom request c
        create_stuff(session, results)

        # 4 delete user Manager
        if session["user"].find("Manager") == -1:
            delete_user(session, results)

        # 5 ...

        ###################################################################
    

# 4. collect results
def write_results():
    if not bool(results):
        with open('results.json', 'w') as f:
            json.dump(results, f)
    else:
        error("[!] No results to write")
        

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # renew sessions
    if len(sys.argv) > 1 and sys.argv[1] == "renew":
        get_sessions()
        exit(0)

    # keep sessions by doing test requests
    if len(sys.argv) > 1 and sys.argv[1] == "keep":
        while True:
            run_tests()
            print("[*] sleeping for 20 mins...")
            time.sleep(20 * 60)

    if renewSessions:
        get_sessions()
    
    if runTests:
        run_tests()
    
    run_requests()

    write_results()
