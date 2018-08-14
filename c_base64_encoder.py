# coding: utf-8
import sys
from c_base64_module import binary, check_length, change_bit, table_64_e

#.bin파일을 바이너리모드로 읽음
input_file = sys.argv[1]
input_dec = open(input_file,'rb').read()

#아스키코드를 8비트 바이너리로 변환
bin_8bit = []
for i in input_dec :
    bin_8bit += binary(i,8)

#길이 계산 후 패딩과 LSB 값 계산 (least significant bit)
padding, LSB = check_length(len(bin_8bit))

#8비트 바이너리를 6비트 바이너리로 변환 후 LSB 추가
bin_6bit =  change_bit(bin_8bit,6,LSB)

#6비트씩 끊은 바이너리를 베이스64코드(0~63 숫자)로 변환하여 리스트
code_base64 = []
for i in range(len(bin_6bit)) :
    temp = 0
    for j in range(6) :
        if bin_6bit[i][j] :
            temp += 2**(5-j)
    code_base64.append(temp)

#베이스64코드를 아스키코드로 변환
encoded_string = ""
for i in code_base64 :
    encoded_string += chr(table_64_e(i))

#패딩 추가
for i in range(padding) :
    encoded_string += "="

#.bin파일 출력
output_file = open("c_base64_encoded.bin",'w')
output_file.write(encoded_string)
output_file.close()

print("인코딩 완료 !\nc_base64_encoded.bin 파일생성 완료!")