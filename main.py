# -*- coding: utf-8 -*-
"""
02-mar-2020

@author: senabayram
"""
import urllib.request
import random

username1 = input("Your username: ")
try:
    userpage = urllib.request.urlopen("https://letterboxd.com/" + username1 + "/watchlist/page/1/")
except:
    print("Invalid username")

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
    
person1_lst = []
              
for page in range(1, page_num + 1):
    watchlist = urllib.request.urlopen("https://letterboxd.com/" + username1 + "/watchlist/page/" + str(page) + "/")
    watchlisthtml = watchlist.read().decode("utf-8")
    while "\n" in watchlisthtml:
        watchlisthtml = watchlisthtml.split("\n")
    for line in watchlisthtml:
        if "film-poster" in line:
            film_strt = line.find("alt=") + len("alt=")
            film_end = line.find("/>", film_strt)
            try:
                person1_lst.append(line[film_strt:film_end]) 
            except:
                break   

username2 = input("Their username: ")
try:
    userpage = urllib.request.urlopen("https://letterboxd.com/" + username2 + "/watchlist/page/1/")
except:
    print("Invalid username!")
    quit()
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
              
person2_lst = []

for page in range(1, page_num + 1):
    watchlist = urllib.request.urlopen("https://letterboxd.com/" + username2 + "/watchlist/page/" + str(page) + "/")
    watchlisthtml = watchlist.read().decode("utf-8")
    while "\n" in watchlisthtml:
        watchlisthtml = watchlisthtml.split("\n")
    for line in watchlisthtml:
        if "film-poster" in line:
            film_strt = line.find("alt=") + len("alt=")
            film_end = line.find("/>", film_strt)
            try:
                person2_lst.append(line[film_strt:film_end]) 
            except:
                break

common_set = list(set(person1_lst) & set(person2_lst))
length = len(common_set)
if length > 0:
    print(f"\nGood news! {username1} and {username2} have {length} films in common!")
    print('\nHere they are:')
    for item in common_set:
        if '\\' in item:
            item = item.replace("\\", "'")
        print(item)
    print('\nFeeling lucky? Here is a random one to watch now: ' + random.choice(common_set).replace('"', ''))
else:
    print(f"Sorry! {username1} and {username2} have no films in common!")


    
    
    