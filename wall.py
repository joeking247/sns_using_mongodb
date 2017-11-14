import time

def printer(apost, uid):
    print("=" * 30)
    print()
    print("time:", apost["time"], "\tuser id:", uid)
    print("\n" + apost["content"])
    print("\n좋아요:", apost["촌스러워"])
    print("=" * 30)


def getPosts(db, userid):
    """
Display your posts. Of course, get all posts would be fine.
However, the function that supports displaying a few posts, e.g., five posts, looks much better than displaying all posts.
Remind the lab4 that dealt with cursor.
    """
    count = 0
    while True:
        uid = userid

        res = list(db.post.find({"uid": uid}).sort("time", -1).skip(count * 5).limit(5))
        #first = db.post.find({"uid":uid}).sort("time",-1).limit(5)
        for apost in res:
            printer(apost, uid)

        more = input("더 보고 싶으면 1을 입력하고, 돌아가고 싶으면 엔터").strip()

        if not more:
            return
        else:
            if more == "1":
                count += 1
                res = list(db.post.find({"uid":uid}).sort("time",-1).skip(count*5).limit(5))
                if not res:
                    print("\n"*3)
                    print("이게 끝이야")
                    print("\n"*3)
                    time.sleep(1)
                    return
                else:
                    for apost in res:
                        printer(apost, uid)



