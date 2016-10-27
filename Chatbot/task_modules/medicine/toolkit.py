
def calculate_sympthom_weight(dic):
    """依照症狀對應的疾病數調整症狀的權重，症狀對應的疾病越多，得分越低
    """
    with open('result/symptom_score.txt','w',encoding='utf-8') as output:
        max = -1
        min = 99
        for v in dic.values():
            if max < len(v.diseases):
                max = len(v.diseases)
            elif min > len(v.diseases):
                min = len(v.diseases)

        for k,v in dic.items():
            output.write('%s:%.4f\n' % (k,1- (len(v.diseases) - min) / (max - min) ))

def cleanline(line):
    """去除讀入資料中的換行符與 ',' 結尾
    """
    line = line.strip('\n')
    line = line.strip(',')
    return line
