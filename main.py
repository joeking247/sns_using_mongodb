import userpage


def mainpage(db):
    '''
    call signup() or signin()
    '''
    while True:
        switch = {1:userpage.signup, 2:userpage.signin}
        switchnum = None
        while switchnum not in {'1', '2', '0'}:
            print("=============================================")
            print("1. 가입하기")
            print("2. 로그인하기")
            print("0. 종료하기")
            switchnum =input("뭐할래? 번호를 입력해라: ")

            if switchnum.isdigit() and int(switchnum) in {1, 2}:
                switch[int(switchnum)](db)
            elif switchnum.isdigit() and int(switchnum)==0:
                return
            else:
                print("제대로 선택해")

if __name__ == "__main__":
    '''
    call mainpage()
    '''
    mainpage(userpage.db)