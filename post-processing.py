# coding=utf-8

import re
import numpy
# en2zh

def RemoveSpaceToSmaoll(str):
    str = str.replace(" ","")
    str = str.lower()
    return str
    
def find_lcseque(s1, s2):   
     # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果  
    m = [ [ 0 for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   
    # d用来记录转移方向  
    d = [ [ None for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   
  
    for p1 in range(len(s1)):   
        for p2 in range(len(s2)):   
            if s1[p1] == s2[p2]:            #字符匹配成功，则该位置的值为左上方的值加1  
                m[p1+1][p2+1] = m[p1][p2]+1  
                d[p1+1][p2+1] = 'ok'            
            elif m[p1+1][p2] > m[p1][p2+1]:  #左值大于上值，则该位置的值为左值，并标记回溯时的方向  
                m[p1+1][p2+1] = m[p1+1][p2]   
                d[p1+1][p2+1] = 'left'            
            else:                           #上值大于左值，则该位置的值为上值，并标记方向up  
                m[p1+1][p2+1] = m[p1][p2+1]     
                d[p1+1][p2+1] = 'up'           
    (p1, p2) = (len(s1), len(s2))   
    # print numpy.array(d)  
    s = []   
    while m[p1][p2]:    #不为None时  
        c = d[p1][p2]  
        if c == 'ok':   #匹配成功，插入该字符，并向左上角找下一个  
            s.append(s1[p1-1])  
            p1-=1  
            p2-=1   
        if c =='left':  #根据标记，向左找下一个  
            p2 -= 1  
        if c == 'up':   #根据标记，向上找下一个  
            p1 -= 1  
    s.reverse()   
    return ''.join(s)   
  
def find_n_sub_str(src, sub, pos, start):
    index = src.find(sub, start)
    if index != -1 and pos > 0:
        return find_n_sub_str(src, sub, pos - 1, index + 1)
    return index

if __name__ == '__main__':
    file1 = open("outen.txt","r",encoding='UTF-8')
    file2 = open("ggzh.txt","r",encoding='UTF-8')
    file3 = open("ggout1.txt","w",encoding='UTF-8')
    file_log = open("log.txt","a",encoding='UTF-8')
    file_log.write("\n*****************************************************\n\n")

    pattern = re.compile(r'[ 0-9A-Za-z]+')
    while True:
        line_en = file1.readline()
        line_zh = file2.readline()     
        if line_en == None or line_zh == None :
            break

        # 测试
        line_en = "i have an iPhone 7"
        line_zh = "我有一个iphone7"
        
        re_ans = pattern.findall(line_zh)   #中文中的所有英文成分
        for item in re_ans:
            # item 去掉首尾空格
            item = item.strip()
            # 完全去空格处理
            en_processed = RemoveSpaceToSmaoll(line_en)
            zh_processed = RemoveSpaceToSmaoll(item)
            if zh_processed in en_processed:   # 完全相同 大小写和空格问题 解决方法 定位，完全替换
                pos = 0
                start = 0
                subpos = find_n_sub_str(en_processed, zh_processed, pos, start)
                while subpos != -1:
                    temp_en = ""
                    start = subpos
                    tempsubpos = subpos
                    for i in line_en:
                        if tempsubpos == 0:
                            temp_en += i
                            print("temp_en :" + temp_en)
                            if RemoveSpaceToSmaoll(temp_en) == zh_processed:
                                print("done!")
                                print(temp_en)
                                print(zh_processed)
                            continue
                        if i != ' ':
                            tempsubpos = tempsubpos - 1
                        else:
                            pass
                    pos = pos + 1
                    subpos = find_n_sub_str(en_processed, zh_processed, pos, start)
                    print(subpos)
            if len(find_lcseque(en_processed,zh_processed))/len(zh_processed) > 0.7 :      #这个数值待调整
                pass
            else:
                file_log.write("\nradio <= 0.7: \n")                
                file_log.write(line_en)
                file_log.write(item)
        break
        # word_bags
        

