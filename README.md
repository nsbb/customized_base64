# customized_base64
2018.08.15  
김희수  

# Introduction
**c_base64_encoder** : .bin 파일명을 매개변수로 받아 파일 안에 있는 평문을 Customized-base64 테이블에 따라 암호화 한 후 다른 .bin 파일에 문자열로 저장하는 프로그램. Python3.6 으로 코딩함.  
**c_base64_decoder** : .bin 파일명을 매개변수로 받아 파일 안에 있는 암호문을 Customized-base64 테이블에 따라 복호화 한 후 다른 .bin 파일에 문자열로 저장하는 프로그램. Python3.6 으로 코딩함.

# Goal
‘utf-8’로 인코딩된 평문을 바이너리값으로 변환하면 맨 앞자리는 0이고 나머지 7비트의 값이 0또는 1인 8자리 바이너리 값을 얻게 된다. 이 8비트 바이너리 값을 6비트로 변형한 후, 변환된 6비트 바이너리 값(2진수)를 10진수로 계산하여 Customized-base64의 테이블에 있는 값으로 변환하여 출력하는것이 문제.

# Customized-base64-table
|6-bits value|original-base64|customized-base64|
|:-:|:-:|:-:|
|0~25|A~Z|a~z|
|26~51|a~z|A~Z|
|52~61|0~9|0~9|
|62|+|+|
|63|/|/|

# Backgrounds
평문은 ‘utf-8’ 로 인코딩 되어 있으며, 영문과 숫자 및 문자 부호는 7비트만 사용하므로 ‘ASCII’ 로 인코딩 하는 것과 동일한 값을 가진다.
.bin파일 평문을 ‘utf-8’ 로 인코딩한 것과, github 문제페이지 처럼 ‘hexadecimal’ 로 인코딩한 것 두가지 경우로 테스트 하였다. (0xc4 라는 16진수값을 유저가 타이핑하지 못하므로)  ‘hexadecimal’ 로 인코딩하여 저장한 파일은 유니코드 ‘utf-8’ 로 인코딩하여 열면 값을 제대로 확인하기 힘드므로 16진수로 표현해주는 전용 에디터를 사용하여 확인해야 한다.

# Specifications
### Encoder
1. .bin 파일을 바이너리 모드로 읽는다. 데이터를 ASCII 코드값으로 읽는다.
2. 10진수인 코드값을 8비트 2진수로 변환한다.
3. 총 비트길이를 계산 하여 패딩과 LSB값을 구한다. 총 비트는 8의 배수이고 이를 24비트씩 나눴을 때의 나머지를 구한다. 패딩은 0, 1, 2중 하나, LSB는 0, 2, 4중 하나의 값을 가진다.
4. 8비트 바이너리 값을 6비트로 변환한다. 이때 3번에서 구한 LSB값 만큼 ‘0’ 을 마지막 바이트 값에 채워준다.
5. 6비트 바이너리 값을 10진수로 변환하여 Customized-base64 코드값을 얻는다.
6. Customized-base64 코드값을 ASCII 코드값으로 변환하여 문자열로 저장한다.
7. 3번에서 구한 패딩값 만큼 ‘=’ 을 문자열에 추가한다.
8.새로운 .bin 파일에 문자열을 쓴 후 종료한다.

### Decoder
1. .bin 파일을 바이너리 모드로 읽는다. 데이터를 ASCII 코드값으로 읽는다.
2. 10진수인 코드값 중 패딩 ‘=’ 이 아닌 값만 Customized-base64 코드값으로 변환한다.
3. Customized-base64 코드값들을 6비트 바이너리로 변환한다.
4. 6비트 바이너리 값을 8비트로 변환한다. 이 과정에서 마지막 바이트의 LSB 비트는 무시된다. (24의 배수로 되어있는 비트를 8로 나누는 과정에서 LSB는 자동으로 제외된다.)
5. 8비트 바이너리 값을 ASCII 코드값으로 변환 후 문자열로 저장한다.
6. 새로운 .bin 파일에 문자열을 쓴 후 종료한다.

### Module
1. 10진수값 x와 n을 받아 x를 n비트 바이너리로 변환하여 리턴하는 함수.
```python
def binary(x, n) :
    bin_nbit = []
    for i in reversed(range(n)) :   #n-1부터 0까지 1씩 감소
        if x >= (2**i) :
            bin_nbit.append(1)
            x -= 2**i
        else :
            bin_nbit.append(0)
        return bin_nbit
```
n-1부터 0까지 1씩 감소하며 반복문을 돈다.  
10진수 값이 2의 n-1승 이상이면 해당 비트 값을 ‘1’로 세팅하고 2의 n-1값을 빼준다.  
그 보다 작으면 ‘0’으로 세팅 한다.  

2. 2진수 리스트 x와 10진수 값 n, LSB를 받아 x를 n비트 바이너리값으로 길이 변환 및 LSB 비트를 추가하여 리턴하는 함수.
```python
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
 ````
카운트 변수를 이용하여 원하는 비트 수 n으로 길이를 변환 후 바이너리 리스트를 리턴한다.  
If문에서 변수의 값이 0일때만 ‘False’이므로 0이 아니면 항상 ‘True’ 이다.  
LSB는 인코더 프로그램에서만 입력해주고 디코더 프로그램은 항상 0만 보내준다.   

3. 인코더 프로그램에서 평문 데이터의 비트의 총 길이를 받아서 패딩값과 LSB값을 리턴하는 함수.
```python
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
```
평문 데이터를 8비트 바이너리 데이터로 변환하면 총 비트 수는 8의 배수가 된다.   
3바이트로 나눴을 때 나눠 떨어지면 패딩과 LSB가 발생하지 않으므로 둘 다 0을 리턴한다.  
1바이트가 마지막에 남으면 16비트를 0으로 채워줘야 한다. 6비트 2블록을 패딩값, 나머지 4비트를 LSB값으로 리턴한다.  
2바이트가 마지막에 남으면 8비트를 0으로 채워줘야 한다. 6비트 1블록을 패딩값, 나머지 2비트를 LSB값으로 리턴한다.  

4. Customized-base64 코드값 10진수 x를 받아 아스키 코드값으로 변환하여 리턴하는 함수.
```python
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
```
x가 0\~25 (‘a\~z’) 이면 x에 97을 더한 값  (ASCII : ‘97\~122’) 을 리턴.  
x가 26\~51 (‘A\~Z’) 이면 x에 39를 더한 값 (ASCII : ‘65\~90’) 을 리턴.  
x가 52\~61 (‘0\~9’) 이면 x에서 4를 뺀 값 (ASCII : ‘48\~57’) 을 리턴.  
x가 62 (‘+’) 이면 43을 리턴.  
x가 63 (‘/’) 이면 47을 리턴.  

5. ASCII 코드값 10진수 x를 받아 Customized-base64 코드값으로 변환하여 리턴하는 함수
```python
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
```
x가 48\~57 (‘0\~9’) 이면 x에 4를 더한 값 (c_base64 : ‘52\~61’) 을 리턴.  
x가 65\~90 (‘A\~Z’) 이면 x에서 39를 뺀 값 (c_base64 : ‘26\~51’) 을 리턴.  
x가 97\~122 (‘a\~z’) 이면 x에서 97를 뺀 값 (c_base64 : ‘0\~25’) 을 리턴.  
x가 43 (‘+’) 이면 62를 리턴.  
x가 47 (‘/’) 이면 63을 리턴.  

#### Mapping table
|Char|ASCII|Adding value|Customized-base64|
|:-:|:-:|:-:|:-:|
|0~9|48~57|±4|52~61|
|a~z|97~122|±97|0~25|
|A~Z|65~90|±39|26~51|
|+|43|±19|62|
|/|47|±16|63|  


# Results
### ‘utf-8’ 로 인코딩하여 저장한 .bin 파일
인코딩 디코딩 모두 제대로 동작한다.
> ./c_base64_encoder hi.bin  
> 인코딩 완료!  
> c_base64_encoded.bin 파일생성 완료!  
  
> ./c_base64_decoder c_base64_encoded.bin  
> 디코딩 완료!  
> c_base64_decoded.bin 파일생성 완료!  
  
> hi.bin  
> a813Valskd hello !@#$%1  
   
> c_base64_encoded.bin  
> ytGXm1zHBhnRzcb0zwXSBYaHqcmKjte=  
  
> c_base64_decoded.bin  
> a813Valskd hello !@#$%1  
  
### ‘hexadecimal’ 로 인코딩하여 저장한 .bin 파일
7비트가 넘어가는 값은 암호화는 잘 되지만, 복호화는 제대로 되지 않는다.  
파이썬에서 int값을 문자열로 변경 할 때 숫자 값과 인코더 종류를 인수로 넣어주면 테이블에 따라서 변경해주는데 ‘ASCII’ 는 1바이트에서 7비트만 사용하므로 8비트 이상의 값은 인코딩자체가 불가능하다. ‘utf-8’ 는 인코딩은 되지만 8비트 이상의 값은 특수한 규칙에 따르게 된다. (유니코드 코드명 U+0079 다음이 U+0080인데, 16진수 코드 값을 보면 0x79 다음이 0x80이 아니라 0xc2 0x80이 되어버려 1바이트가 아닌 2바이트가 된다. 10진수 코드 127 이후 부터는 2바이트로 표현. 아스키코드와의 호환성 때문.)  
그래서 7비트가 넘는 값을 문자열로 변경하면 무조건 ‘utf-8’ 로 인코딩이 되고, 결과값이 달라져서 원래의 평문과는 값이 달라진다.  
  
> ./c_base64_encoder 0420c4.bin  
> 인코딩 완료!  
> c_base64_encoded.bin 파일생성 완료!  
  
> ./c_base64_decoder c_base64_encoded.bin  
> 디코딩 완료!  
> c_base64_decoded.bin 파일생성 완료!  
  
> 0420c4.bin  
> 04 20 C4  
  
> c_base64_encoded.bin  
> 62 63 64 65 | bcde  
   
> c_base64_decoded.bin  
> 04 20 C3 84  
  
인코딩은 잘 되지만 디코딩을 하면 복호화된 값과 평문의 값이 다르다.  
  
> 4   |' '|   0x04  
> 32  |' '|   0x20  
> 196 |'Ä'| 0xc3 0x84  
   
복호화된 값을 int, str, hex형으로 비교해본 모습. 16진수값 ‘c4’ 가 10진수 값은 일치하나 ‘utf-8’로 인코딩하여 문자열로 저장하는 과정에서 16진수의 값이 변한다.  
  
> In  : bytes(chr(127), 'utf-8')  
> Out : 0x7f  
> In  : bytes(chr(127), 'utf-8')  
> Out : 0xc2 0x80  
> In  : bytes(chr(127), 'utf-8')  
> Out : 0xc3 0x84  
  
|Unicode code point|hex|
|---|---|
|U+007E|0x7e|
|U+007F|0x7f|
|U+0080|0xc2 0x80|
|U+0081|0xc2 0x81|
|U+00C4|0xc3 0x84|
  
127은 0x7f이지만 128은 0x80이 아닌 0xc2 0x80이 된다.  
  
# References
* [smartm2m/customized-base64](https://github.com/smartm2m/customized-base64)  
* [Base64 - Wikipedia](https://en.wikipedia.org/wiki/Base64)  
* [ASCII - Wikipedia](https://en.wikipedia.org/wiki/ASCII)  
* [Unicode/UTF-8 character table](https://www.utf8-chartable.de/unicode-utf8-table.pl)  
