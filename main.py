# -*- coding: utf-8 -*-
"""
original code by @senabayram
forked / updated by @owenhalpert
"""
import urllib.request
import random

print("""
Welcome to the Letterboxd Common Movies Tool.
This tool will generate a list of common movies between two or more Letterboxd users. 
Please enter the usernames of the two or more users you wish to compare, and type 'done' when you have entered them all.

""")

usernames, done = [], False

#Get usernames
while not done: 
    username = input("Enter a Letterboxd username, or write 'done': ")
    if username == "":
        print("Error: You must enter a valid username.")
        username = None
    if username == "done":
        done = True
    else:
        usernames.append(username)

if len(usernames) == 1:
    print("Error: You must enter at least two usernames.")
    exit()

def watchlist_to_lst(username):
    try:
        userpage = urllib.request.urlopen("https://letterboxd.com/" + username + "/watchlist/page/1/")
    except:
        print("Error: One or more invalid username inputs. Please try again.")
        exit()
    userpagehtml = userpage.read().decode("utf-8")
    page_num = 1
    while "\n" in userpagehtml:
            userpagehtml = userpagehtml.split("\n")      
    for line in userpagehtml:
        if "paginate-current" in line:
            pos = line.find("paginate-current") + len("paginate-current")
            if line.find("page/3", pos) == -1:
                page_num = 2
            else:
                page_pos = line.find("page/3", pos) + len("page/3")
                if line.find("page/", page_pos) != -1:
                    reduced = line[line.find("page/", page_pos) + len("page/"):]
                    page_num = int(reduced.split("/")[0])
                else:
                    page_num = 3 
    lst = []          
    for page in range(1, page_num + 1):
        watchlist = urllib.request.urlopen("https://letterboxd.com/" + username + "/watchlist/page/" + str(page) + "/")
        watchlisthtml = watchlist.read().decode("utf-8")
        while "\n" in watchlisthtml:
            watchlisthtml = watchlisthtml.split("\n")
        for line in watchlisthtml:
            if "film-poster" in line:
                film_strt = line.find("alt=") + len("alt=")
                film_end = line.find("/>", film_strt)
                try:
                    lst.append(line[film_strt:film_end]) 
                except:
                    break
    return lst

#Get watchlists for each user
p = [] 
for user in usernames: 
    p.append(watchlist_to_lst(user))

#Get common movies
result = set(p[0]) 
for s in p[1:]:
    result.intersection_update(s)

#Print results
length = len(result) 
if length > 1:
    print(f"\nGood news! These users have {length} films in common!")
    print('\nHere they are:')
    for item in result:
        if '\\' in item:
            item = item.replace("\\", "'")
        print(item)
    print('\nFeeling lucky? Here is a random one to watch now: ' + random.choice(list(result)).replace('"', ''))
elif length == 1:
    print(f"\nGood news! These inputted users have 1 film in common!")
    print('\nHere it is: ' + list(result)[0].replace('\\', ''))
else:
    print(f"Sorry! These users have no films in common!")


    
    
    
