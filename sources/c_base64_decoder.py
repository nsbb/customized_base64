# coding: utf-8
import sys
from c_base64_module import binary, change_bit, table_64_d

#.bin파일을 바이너리모드로 읽음
input_file = sys.argv[1]
input_dec = open(input_file,'rb').read()

#아스키코드를 베이스64코드(0~63 숫자)로 변환
code_base64 = []
for i in input_dec :
    if i != 61 :               # '='(패딩)이 아닌 경우만
        code_base64.append(table_64_d(i))

#베이스64코드를 6비트 바이너리로 변환
bin_6bit = []
for i in code_base64 :
    bin_6bit += binary(i,6)

#6비트 바이너리를 8비트 바이너리로 변환
bin_8bit = change_bit(bin_6bit,8,0)

#8비트 바이너리를 아스키코드로 변환 후 문자열로 변환
decoded_string = ""
for i in range(len(bin_8bit)) :
    ascii_code = 0
    for j in range(8) :
        if bin_8bit[i][j] :
            ascii_code += 2**(7-j)
    decoded_string += chr(ascii_code)

#.bin파일 출력
output_file = open("c_base64_decoded.bin",'w')
output_file.write(decoded_string)
output_file.close()

print("디코딩 완료!\nc_base64_decoded.bin 파일생성 완료!")
