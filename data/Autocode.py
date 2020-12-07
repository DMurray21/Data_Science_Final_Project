import pandas as pd
import os.path as osp
import json
import warnings
import argparse
import numpy
codes=["Future administration","Lame Duck","Overturning 2020 Election Results","Trump legacy","Election Fraud","Transition","Election insights","Other Political Happenings"]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input',help="Path to the input data file.")
    parser.add_argument('-c',help="Number of posts counted.")
    args = parser.parse_args()
    target = args.input.split(".json")[0] + "_CODED.json"
    c = 0
    posts = []

    if type(intify(args.c)) == type(c):
        c=intify(args.c)
    d = c
    with open(args.input, "r") as fp:
        for line in fp:
            post=json.loads(line)
            posts += [post]
    print(f"Loading {args.input} starting from post {c}, total number of posts = {len(posts)}\n")
    with open(target, "a+") as fp:
        for post in posts:
            if c > 0:
                c -= 1
                continue
            cmd = "" 
            title = post["title"]
            print(f"Post title: {title} \n")
            while not valid(cmd):
                print("Which code should it have?\n")
                cmd = input()
                cmd = intify(cmd)
                if cmd == "help":
                    helpmsg()
                if cmd == "progress":
                    print(f"Coded {d} posts out of {len(posts)}")

            
            if cmd == "quit":
                break
            print(codes[cmd],"\n")
            post["code"] = codes[cmd]
            line=json.dumps(post)
            fp.write(line)
            fp.write("\n")
            d += 1
    with open("log.txt", "w") as f:
        f.write(str(d))

def valid(word):
    return (word in range(8))  or (word == "quit")
def intify(word):
    try:    
        word = int(word)
    except:
        pass
    return word
def helpmsg():
    print("Accepted commands:") 
    print ("help\nquit")
    for i in range(len(codes)):
        print(f"{i}:  {codes[i]}")
    print("\n")
if __name__ == "__main__":
    main()
    