# user.py

import time
from pymongo import MongoClient
# from main import mainpage
import postspage
import followpage

userconnection = []
client = MongoClient()
db = client.project
"""
def closeconn(db):
    print("잘가요 %s"%userpage.userconnection.pop() if userpage.userconnection else "잘가 낯선 사람")
"""
def signup(db):
    '''
    1. Get his/her information.
    2. Check if his/her password equals confirm password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''

    conf0 = 'n'
    while conf0 != 'y':
        # get id from user input
        uid = input("사용할 ID를 알려줘(뒤로 가고 싶으면 엔터): ")
        # going back
        if not uid:
            return
        else:
            s = db.users.find_one({"uid":uid})

            # if same id already exists
            if s:
                print("이거 누가 벌써 쓰고 있다. 다른 걸로 골라봐!")
            # if id is valid
            else:
                conf0 = 'n'
                while conf0 == 'n':

                    # get password from user input
                    pswd = input("까먹지 않을 비밀번호로 알려줘(뒤로 가고 싶으면 엔터): ")
                    if not pswd:
                        break
                    else:
                        pswd2 = input("안 까먹을 수 있으면 다시 쳐봐")

                        # correct password -> may proceed
                        if pswd == pswd2:
                            conf1 = input("아이디랑 비밀번호 확실해? (다시 정하고 싶으면 !를 입력해. 확실하면 아무거나): ").strip()
                            if conf1 != '!':
                                conf0 = 'y'
                            else:
                                break
                        # if passwords don't match
                        else:
                            print("어떻게 비밀번호를 벌써 까먹어?")

    # id/password is set, gather other info
    conf2 = '!'
    while conf2 == '!':
        name = input("이름 알려줘: ")
        conf2 = input("이름 이거 확실해? (실수했으면 !입력해. 확실하면 아무거나): ").strip()
        if conf2 != '!':
            birth = input("생일을 알려줘(년/월/일) :")
            db.users.insert_one({"uid": uid, "password": pswd, "name": name, "birth": birth,
                                 "status": "여긴 내 페이지다 내 아이디는 %s, 내 이름은 비밀이지" % uid})
            print()
            print("축하해! 가입 완료!\n")
            time.sleep(1)
            print("이제 게임을 시작하지\n\n")
            time.sleep(1)
    return uid, pswd, name


def signin(db):
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''
    conf0 = 'n'
    while conf0 != 'y':
        uid = input("ID가 뭐야? (뒤로가려면 엔터): ")
        if not uid:
            return
        # id check
        else:
            user = db.users.find_one({"uid": uid})

            # wrong id
            if not user:
                print("그런 ID 없다")
            # correct id
            else:
                # password check
                conf1 = 'n'
                while conf1 != 'y':
                    pswd = input("비밀번호 알려줘 (뒤로가려면 엔터): ")
                    if not pswd:
                        break
                    else:
                        # wrong password
                        if pswd != user['password']:
                            time.sleep(0.8)
                            print("비밀번호가 틀리잖아")
                            time.sleep(0.89)
                            regrets = input("비밀번호 알려줘? 다시 시도해보려면 아무 키나.\n"
                                            "까먹은 거면 다음을 정확히 입력해라: 다음부터는 비밀번호를 까먹지 않겠습니다 ").strip()

                            # reset password
                            if regrets == '다음부터는 비밀번호를 까먹지 않겠습니다':
                                time.sleep(0.8)

                                # get name to reset password
                                conf3 = 'n'
                                while conf3 != 'y':
                                    name = input("본인 확인하게 이름을 알려줘: ")
                                    # correct name
                                    if user['name'] == name:
                                        conf3 = 'y'

                                        # if user data is correct -> get new password
                                        newpw = input("까먹지 않을 비밀번호를 알려다오: ")
                                        newpw2 = input("안까먹을 수 있으면 다시 쳐봐")

                                        # passwords don't match
                                        if newpw != newpw2:
                                            print()
                                            time.sleep(0.8)
                                            print("넌 벌써 비밀번호를 틀렸어\n\n")
                                            time.sleep(1)
                                            print("주어진 기회를 소중히 하지 않았지\n\n")
                                            time.sleep(0.8)
                                            return
                                        # passwords match so update db
                                        else:
                                            db.users.update({"uid": uid, "name": name},
                                                            {"$set": {'password': newpw}})
                                            conf1 = 'y'
                                            time.sleep(0.8)
                                            print("\n\n비밀번호 변경 완료! 잘 기억하도록 해\n")
                                            print("*"*30)
                                            break
                                    # wrong name : return to conf3
                                    else:
                                        print("그런 이름 없다\n")
                                        break
                        #correct
                        else:
                            conf1='y'
                            conf0='y'
                            userpage(db, uid)


def mystatus(db, uid):
    '''
    print user profile, # followers, and # followings
    '''
    user = db.users.find_one({"uid": uid})
    print("\n\n")
    print(user['status'])
    print("꺄르륵!")
    print("\n\n")
    time.sleep(2)
    return userpage(db, uid)


def cgstatus(db, uid):
    newbase = input("상태창에 표시할 내용을 입력해라")
    db.users.update({"uid":uid},
                    {"$set": {'status': newbase}})
    return userpage(db, uid)


def userpage(db, uid):
    '''
    user page
    '''
    switch = {1: mystatus, 2: cgstatus, 3: followpage.followInterface, 4: postspage.postInterface}
    switchnum = None
    while True:
        print()
        print("=============================================")
        print("\n        ++++++++++내 페이지++++++++++\n\n\t내 아이디:%s\n" % uid)
        print("\t1. 내 상태를 확인")
        print("\t2. 내 상태를 변경")
        print("\t3. 팔로잉/팔로우 확인 및 설정")
        print("\t4. 내 글 관리")
        print("\t0. 뒤로 가기\n")
        switchnum = input("뭐할래? 번호를 입력해라: ")

        if switchnum.isdigit() and int(switchnum) in {0, 1, 2, 3, 4}:
            if int(switchnum) == 0:
                return
            else:
                switch[int(switchnum)](db, uid)
        else:
            print("제대로 선택해")
