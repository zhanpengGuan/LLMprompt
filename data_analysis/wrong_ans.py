import json
import os
import csv
import ast
import chardet
# 使用前清除result和result_k1的数据，然后更换PATH，更换save_path即可
def ifin(s_list,s):
        
    return any(i in s for i in s_list)
def yes(t_list,s):
    if ifin(t_list,s) :
        return True
    else:
        return False

# 读取json文件
PATH_list = ["syno_judge_test_2type_tag2tag_open_sample_m_gpt35.json","syno_judge_test_2type_tag2tag_sample_m_gpt35.json",\
             "syno_judge_test_sample_m_gpt35-20230810.json","syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json",\
                "syno_judge_test_tag2tag_k1_sample_m_gpt35.json",\
             "syno_judge_test_tag2tag_rand_sample_m_gpt35.json","syno_judge_test_tag2tag_sample_m_gpt35.json"]



for num_P in range(len(PATH_list)): 
    x = []
    PATH = PATH_list[num_P]
    result_path = PATH.split('.')[0]
    with open('result/'+result_path+'/'+result_path+'.json', 'r') as f:
        json_data = f.read().splitlines()
        for i in range(len(json_data)):
            x.append(json.loads(json_data[i]))
        print(x[0])
    y = []
    with open('result/'+result_path+'/teach_position_'+result_path+'.json', 'r') as f:
        json_data = f.read().splitlines()
        for i in range(len(json_data)):
            y.append(json.loads(json_data[i]))
        print(x[0])
    true_labels = []
    pred_labels1 = []
    pred_labels2 = []
    with open('result/'+result_path+'/'+'reslut.txt', 'r') as f:
        data = f.read().splitlines()
        true_labels.append(ast.literal_eval(data[1][12:]))
        pred_labels1.append(ast.literal_eval(data[3][12:]))
        true_labels.append(ast.literal_eval(data[14][12:]))
        pred_labels1.append(ast.literal_eval(data[16][12:]))
        true_labels.append(ast.literal_eval(data[27][12:]))
        pred_labels1.append(ast.literal_eval(data[29][12:]))
    with open('result/'+result_path+'/teach_position_'+'reslut.txt', 'r') as f:
        data = f.read().splitlines()
        pred_labels2.append(ast.literal_eval(data[3][12:]))
        pred_labels2.append(ast.literal_eval(data[16][12:]))
        pred_labels2.append(ast.literal_eval(data[29][12:]))
    with open('result/'+result_path+'/compare.txt','w') as f2:
        for c in range(3):
            for i in range(len(true_labels[c])):
                if true_labels[c][i]==1 and pred_labels1[c][i]!=pred_labels2[c][i]:
                    index = i*3+c
                    jsonstr =   json.dumps(x[index],ensure_ascii=False)
                    f2.write('\n'+'*'*20+'\n')
                    f2.write(x[index]['prompt']+'\n')
                    f2.write('true_label:'+str(true_labels[c][i])+'\n')
                    f2.write('-'*20+'\n')
                    f2.write('pred_label1:'+str(pred_labels1[c][i])+'\n'+x[index]['predict'][0]+'\n')
                    f2.write('-'*20+'\n')
                    f2.write('pred_label2:'+str(pred_labels2[c][i])+'\n'+y[index]['predict'][0]+'\n')
                    
            
            