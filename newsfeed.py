import time

def printer(apost, uid):
    print("=" * 30)
    print()
    print("time:", apost["time"], "\tuser id:", uid)
    print("\n" + apost["content"])
    print("\n좋아요:", apost["촌스러워"])
    print("=" * 30)

def getPosts(db,userid):
    """
It is similar to the function in wall.py
Get posts of your followings.
There can be a few options to sort the posts such as posting date or alphabetical order of following's name.
    """
    print("가장 최근에 올라온 글 순으로 네가 팔로우하는 사람들이 쓴 글을 보여주지")
    count = 0
    while True:
        uid = userid
        followings = list(db.follow.find({"follower": uid}))

        if not followings:
            print("\n\n누구를 팔로우 해야 뉴스피드를 보여주지!\n\n")
            time.sleep(1)
            return
        else:
            res = list(db.post.find({"uid": {"$in": followings}}).sort("time", -1).skip(count * 5).limit(5))
            if not res:
                print("\n\n아무도 글을 안 썼네\n\n")
                time.sleep(1)
                return
            else:
                for apost in res:
                    printer(apost, uid)

                more = input("더 보고 싶으면 1을 입력하고, 돌아가고 싶으면 엔터").strip()

                if not more:
                    return
                else:
                    if more == "1":
                        count += 1
                        res = list(db.post.find({"uid": {"$in": followings}}).sort("time", -1).skip(count * 5).limit(5))
                        if not res:
                            print("\n"*3)
                            print("이게 끝이야")
                            print("\n"*3)
                            time.sleep(1)
                            return
                        else:
                            for apost in res:
                                printer(apost, uid)


