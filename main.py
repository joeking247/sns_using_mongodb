# main.py
import user

def mainpage(db):
    '''
    call signup() or signin()
    '''
    while True:
        switch = {1:user.signup, 2:user.signin}
        switchnum = None
        while switchnum not in {'1', '2', '0'}:
            print("=============================================")
            print("1. 가입하기")
            print("2. 로그인하기")
            print("0. 종료하기")
            switchnum =input("뭐할래? 번호를 입력해라: ")

            try:
                if int(switchnum) in {1, 2}:
                    return switch[int(switchnum)](db)
                if int(switchnum) == 0:
                    return
                else:
                    print("있는 것 중에 똑바로 선택해라")
            except:
                print("있는 것 중에 똑바로 선택해라")


if __name__ == "__main__":
    '''
    call mainpage()
    '''
    mainpage(user.db)