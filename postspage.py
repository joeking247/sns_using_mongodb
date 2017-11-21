import time
import re
import pymongo

"""
from pymongo import MongoClient
client = MongoClient()
db = client.project
user = db.users.find_one()
"""

def postInterface(db, uid):
    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    switch = {1: insertPost, 2: deletePost, 3: showPost}
    switchnum = None
    while True:
        print()
        print("=============================================")
        print("글 관련 페이지. \n내 아이디: %s" % uid)
        print("1. 글 쓰기")
        print("2. 글 삭제하기")
        print("3. 내 글 보기")
        print("0. 뒤로가기")
        switchnum = input("뭐할래? 번호를 입력해라: ")

        if switchnum.isdigit() and int(switchnum) in {0, 1, 2, 3}:
            if int(switchnum) == 0:
                return
            else:
                switch[int(switchnum)](db, uid)
        else:
            print("제대로 선택해")



def insertPost(db, uid):
    """
    Insert user's text. You should create the post schema including,
    for example, posting date, posting id or name, and comments.

    You should consider how to delete the text.
    """
    posting = input("할 말 있으면 해봐(없으면 엔터): ")
    if not posting:
        return
    else:
        uid = uid
        name = db.users.find_one({"uid":uid})['name']
        t = time.ctime()

        # hash tag 기능 구현
        # '#'기준으로 parse
        p = re.compile(r"#\w+")
        res = p.findall(posting)
        tags = list(map(lambda x:x[1:], res))
        db.post.insert_one({'uid':uid, 'name':name, 'time':t, 'content':posting, '촌스러워':0, 'tags':tags})
        db.post.create_index([('tags', pymongo.TEXT)])




def deletePost(db, uid):
    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    """
    all = list(db.post.find({'uid': uid}))[::-1]
    showPost(db, uid)

    while True:
        num = input("게시물 번호 몇 번을 지울 건지 말해봐(없으면 엔터): ")
        if not num:
            return
        else:
            conf0 = input(str(num)+"번 지우는 거 확실해? 다시 안 물어볼거야\n확실하면 y를 입력해라: ").lower()
            if conf0 == 'y':
                go = all[int(num)-1]
                db.post.delete_one({"_id":go["_id"]})


def showPost(db, uid):
    all = list(db.post.find({'uid':uid}))[::-1]
    for idx in range(len(all)):
        one = all[idx]
        print()
        print("["+str(idx+1)+"]",one['time'],"\t",one['uid'])
        print("\n", one['content'], "\n")
        print("좋아요: ", str(one['촌스러워']))
        print("-----------------------------")


def showHash(db, uid):
    tag = input("검색할 단어를 하나 입력해라. 모든 띄어쓰기는 무시되니까 참고해(뒤로 가려면 엔터): ")
    if not tag:
        return
    else:
        word = tag.replace(" ","")
        res = list(db.post.find({'$text':{'$search':word}}))
        if not res:
            print("-----------------------------")
            print("\n\n그런 이상한 태그로는 아무도 글을 안썼어.\n\n")
            print("-----------------------------")
            time.sleep(2)
        else:
            for idx in range(len(res)):
                one = res[idx]
                print()
                print("[" + str(idx + 1) + "]", one['time'], "\tuser id: ", one['uid'])
                print("\n", one['content'], "\n")
                print("좋아요: ", str(one['촌스러워']))
                print("-----------------------------")

