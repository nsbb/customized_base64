#10진수를 n비트 바이너리로 변환
def binary(x, n) :
    bin_nbit = []
    for i in reversed(range(n)) :   #n-1부터 0까지 1씩 감소
        if x >= (2**i) :
            bin_nbit.append(1)
            x -= 2**i
        else :
            bin_nbit.append(0)

    return bin_nbit


#바이너리 데이터 x를 n비트 바이너리로 변환 및 LSB 추가(encoder만! decoder는 0입력)
def change_bit(x, n, LSB) :
    bin_nbit = []
    temp = []
    count = 0

    for i in x :
        temp.append(i)
        count += 1
        if count % n == 0 :
            bin_nbit.append(temp)
            temp = []

    if LSB :    #LSB값이 0이 아니면
        for i in range(LSB) :
            temp.append(0)
        bin_nbit.append(temp)

    return bin_nbit


#패딩과 LSB값 계산
def check_length(x) :
    if x % 24 == 0 :
        padding = 0
        LSB = 0
        return padding, LSB
    elif x % 24 == 8 :
        padding = 2
        LSB = 4
        return padding, LSB
    elif x % 24 == 16 :
        padding = 1
        LSB = 2
        return padding, LSB


#베이스64코드를 아스키코드로 변환
def table_64_e(x) :
    if x in range(26) :        # 0 <= x <= 25
        return x+97
    elif x in range(26,52) :   # 26 <= x <= 51
        return x+39
    elif x in range(52,62) :   # 52 <= x <= 61
        return x-4
    elif x == 62 :
        return 43
    elif x == 63 :
        return 47


#아스키코드를 베이스64코드로 변환
def table_64_d(x) : 
    if x in range(48,58) :     #'0~9'
        return x+4
    elif x in range(65,91) :   #'A~Z'
        return x-39
    elif x in range(97,123) :  #'a~z'
        return x-97
    elif x == 43 :             #'+'
        return 62
    elif x == 47 :             #'/'
        return 63
