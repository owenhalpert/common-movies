# -*- coding: utf-8 -*-
"""
original code by @senabayram
forked / updated by @owenhalpert
"""
import urllib.request
import random

username1, username2 = input("Your username: "), input("Your friend's username: ")

def watchlist_to_lst(username):
    try:
        userpage = urllib.request.urlopen("https://letterboxd.com/" + username + "/watchlist/page/1/")
    except:
        print("One or more invalid username inputs. Please try again.")
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

lst1, lst2 = watchlist_to_lst(username1), watchlist_to_lst(username2)

common_set = list(set(lst1) & set(lst2))
length = len(common_set)
if length > 1:
    print(f"\nGood news! {username1} and {username2} have {length} films in common!")
    print('\nHere they are:')
    for item in common_set:
        if '\\' in item:
            item = item.replace("\\", "'")
        print(item)
    print('\nFeeling lucky? Here is a random one to watch now: ' + random.choice(common_set).replace('"', ''))
elif length == 1:
    print(f"\nGood news! {username1} and {username2} have {length} film in common!")
    print('\nHere it is: ' + common_set[0].replace('\\', ''))
else:
    print(f"Sorry! {username1} and {username2} have no films in common!")


    
    
    
