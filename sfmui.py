#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb; cgitb.enable()

import os
import pickle
import shutil

from sfmuisettings import *

def get_next():
    record = None
    inp_dict = {}
    if os.path.isfile(INPROGRESS_FILE):
        inp_dict = pickle.load(open(INPROGRESS_FILE, "rb"))
    # check for orphaned record
    if len(inp_dict.keys()) > 0:
        record = inp_dict[list(inp_dict.keys())[0]]        
    # otherwise pop the next pending record
    else:
        if not os.path.isfile(PENDING_FILE):
            print("sfmui is not set up")
        pendingstack = pickle.load(open(PENDING_FILE, "rb"))
        if len(pendingstack) > 0:
            record = pendingstack.pop()
            pickle.dump(pendingstack, open(PENDING_FILE, "wb"))    
            # put the active record in the in-progress structure
            inp_dict[record["id"]] = record
            pickle.dump(inp_dict, open(INPROGRESS_FILE, "wb"))
    if record:
        # print the page that requests a response from a user
        # FIXME: add option to respond to multiple images on one page maybe by looping multiple table cells or using iframes
        idNum = record["id"]
        url = record["url"]
        metadata = ""
        for k in sorted(list(record["metadata"].keys())):
            metadata += k + ": " + record["metadata"][k] + "<br>"
        metadata = metadata[:-3]
        alttext = metadata.replace("<br>", ", ")
        print(ASK_PAGE_STRING.replace("!QUESTION!", QUESTION).replace("!URL!", url).replace("!ALTEXT!", alttext).replace("!ID!", idNum).replace("!INPUTS!", INPUTS).replace("!METADATA!", metadata).replace("!FOOTER!", FOOTER))
    else:
        if not os.path.isfile(FINALRESULTS_FILE):
            if os.path.isfile(COMPLETED_FILE):
                completed = pickle.load(open(COMPLETED_FILE, "rb"))
                with open(FINALRESULTS_FILE, "w") as f:
                    f.write('id,score\n')
                    for r in completed:
                        f.write(str(r) + "," + str(completed[r]) + "\n")
        backup()
        cleanup()
        print("All done!")         

def handle_response(idNum, score):
    # record the score
    completed = {}
    if os.path.isfile(COMPLETED_FILE):
        completed = pickle.load(open(COMPLETED_FILE, "rb"))
    completed[idNum] = score
    pickle.dump(completed, open(COMPLETED_FILE, "wb"))
    # remove the record from the in-progress structure
    inp_dict = pickle.load(open(INPROGRESS_FILE, "rb"))
    inp_dict.pop(idNum)
    pickle.dump(inp_dict, open(INPROGRESS_FILE, "wb"))
    # find out whether the user wants to keep going
    #FIXME: add ability to redo a response if user changes their mind
    print(RESPONSE_RECORDED_PAGE_STRING.replace("!ID!", idNum).replace("!SCORE!", score).replace("!FOOTER!", FOOTER))

def setup():
    backup()
    cleanup()
    pending = []
    with open(DATA_FILE, "r") as f:
        header = f.readline().strip().split(",") if HAS_HEADER else None
        for line in f:
            record = {}
            line = line.strip().split(",")
            record["id"] = line[ID_INDEX]
            record["url"] = line[URL_INDEX]
            metadata = {}
            for i in range(len(line)):
                if i != ID_INDEX and i != URL_INDEX and i not in IGNORE_INDICES:
                    k = header[i] if header else str(i)
                    metadata[k] = line[i]
            record["metadata"] = metadata
            pending.append(record)
    pickle.dump(pending, open(PENDING_FILE, "wb"))
    print("Good to go. <a href=\"" + SFMUI_URL + "sfmui.py?action=get" + "\">Rate stuff</a>")

def backup():
    if not os.path.exists("backup"):
        os.makedirs("backup")
    srcs = [FINALRESULTS_FILE, PENDING_FILE, INPROGRESS_FILE, COMPLETED_FILE]
    [ shutil.copyfile(s, os.path.join("backup",s)) for s in srcs if os.path.exists(s) ]

def cleanup():
    srcs = [PENDING_FILE, INPROGRESS_FILE, COMPLETED_FILE]
    [ os.remove(s) for s in srcs if os.path.exists(s) ]
        
    
if __name__=="__main__":
    print("Content-Type: text/html\n\n")
    args = cgi.FieldStorage()
    if "action" not in args.keys():
        print("No action specified!")
    else:
        action = args["action"].value
        if action == "get":
            get_next()
        elif action == "submit":
            if "score" not in args.keys():
                print("Didn't get a score!")
            elif "id" not in args.keys():
                print("Didn't get an id!")
            else:
                idNum = args["id"].value
                score = args["score"].value  
                handle_response(idNum, score)
        elif action == "quit":
            print("Thanks for responding!")
        elif action == "setup":
            setup()
        else:
            print("Unknown action: " + str(action))
