# user.py
from pymongo import MongoClient
from main import mainpage
import posts
import follow

client = MongoClient()
db = client.project

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
        #get id from user input
        uid = input("사용할 ID를 알려다오: ")
        s = db.users.find_one({"uid":uid})
        #if same id already exists
        if s:
            print("이거 누가 쓰고 있음 딴걸로 골라봐")

        #if id is valid
        else:
            conf1 = 'n'
            while conf1 == 'n':
                #get password from user input
                pswd = input("까먹지 않을 비밀번호를 알려다오: ")
                pswd2 = input("안까먹을 수 있으면 다시 쳐봐")
                if pswd==pswd2:
                    conf1='y'

                #if passwords don't match
                else:
                    print("어떻게 비밀번호를 벌써 까먹어?")
            conf0 = input("아이디랑 비밀번호 확실함? 나중에 안바꿔줘 (확실하면 y 아니면 n 눌러라): ").lower()

    conf2 ='n'
    while conf2 != 'y':
        name = input("이름을 알려다오: ")
        conf2 = input("이름 이거 확실함? (확실하면 y 아니면 n 눌러라): ").lower().strip()
        if conf2 == 'y':
            birth = input("생일을 알려다오(년/월/일) :")
            db.users.insert_one({"uid": uid, "password": pswd, "name":name, "birth":birth, "status":"여긴 내 페이지다 내 아이디는 %s, 내 이름은 비밀이지"%uid})

    return uid, pswd, name, mainpage(db)



def signin(db):
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''
    conf0 = 'n'
    while conf0 != 'y':
        uid = input("너의 ID를 알려다오: ")
        ans = db.users.find_one({"uid": uid})

        # wrong id
        if not ans:
            print("그런 ID 없다")

        # correct id
        else:
            conf1 = 'n'
            while conf1 != 'y':
                pswd = input("비밀번호를 알려다오: ")

                # wrong password
                if pswd != ans['password']:
                    print("비밀번호가 틀리잖아")
                    regrets = input("비밀번호 알려줘? (알고싶으면 다음을 정확히 입력해라:다음부터는 비밀번호를 까먹지 않겠습니다) ").strip()

                    # reset password
                    if regrets == '다음부터는 비밀번호를 까먹지 않겠습니다':

                        #get name to reset password
                        conf3 = 'n'
                        while conf3 != 'y':
                            name = input("너의 이름을 알려다오: ")
                            # correct name
                            if ans['name'] == name:
                                conf3 = 'y'

                                #if user data is correct -> get new password
                                newpw = input("까먹지 않을 비밀번호를 알려다오: ")
                                newpw2 = input("안까먹을 수 있으면 다시 쳐봐")

                                #passwords don't match
                                if newpw != newpw2:
                                    print("넌 벌써 비밀번호를 틀렸어")
                                    print("주어진 기회를 소중히하지 않았지")
                                #passwords match so update db
                                else:
                                    db.users.update({"uid":uid, "name":name},
                                                      {"$set":{'password':newpw}})
                                    conf1 = 'y'
                                    break
                            # wrong name : return to conf3
                            else:
                                print("그런 이름 없다")

                    else:
                        break
                else:
                    return userpage(db, ans)





def mystatus(db, user):
    '''
    print user profile, # followers, and # followings
    '''
    ans=user
    print(user['status'])
    print("꺄르륵!")
    return userpage(db, ans)



def cgstatus(db, user):
    ans = user
    newbase = input("상태창에 표시할 내용을 입력해라")
    db.users.update({"uid": ans['uid']},
                    {"$set": {'status': newbase}})


def userpage(db, user):
    '''
    user page
    '''
    switch = {1:mystatus, 2:cgstatus, 3:follow.followInterface, 4:posts.postInterface}
    switchnum = None
    while switchnum not in {'1', '2', '3', '4'}:
        print()
        print("=============================================")
        print("내 페이지. \n내 아이디: %s"%user['uid'])
        print("1. 내 상태를 확인")
        print("2. 내 상태를 변경")
        print("3. 팔로잉/팔로우 확인 및 설정")
        print("4. 내 글 관리")
        switchnum = input("뭐할래? 번호를 입력해라: ")

        if switchnum == 'q':
            break

        else:
            try:
                if eval(switchnum) in {1, 2, 3, 4}:
                    switch[eval(switchnum)](db, user)
                else:
                    print("있는 것 중에 똑바로 선택해라")
            except:
                print("있는 것 중에 똑바로 선택해라")

#signin(db)