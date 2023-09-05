import json
import os


# 使用前清除result和result_k1的数据，然后更换PATH，更换save_path即可
def ifin(s_list,s):
        
    return any(i in s for i in s_list)
def yes(t_list,s):
    if ifin(t_list,s) :
        return True
    else:
        return False
# 读取json文件
PATH_list = ["syno_judge_test_tag2tag_k1_sample_m_gpt35.json","syno_judge_test_sample_m_gpt35-20230810.json","syno_judge_test_2type_tag2tag_open_sample_m_gpt35.json",\
             "syno_judge_test_2type_tag2tag_sample_m_gpt35.json","syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json","syno_judge_test_tag2tag_rand_sample_m_gpt35.json",\
                "syno_judge_test_tag2tag_sample_m_gpt35.json"]
for num_p in range(len(PATH_list)): 
    PATH = PATH_list[num_p]
    with open(PATH, 'r') as f:
        json_data = f.read().splitlines()
        x = []
        right_str1 = ['是的','是同一种东西','是相同的','是']
        wrong_str1 = ['不是','不成立',]
        right_str2 = ['是的','是一种']
        wrong_str2 = ['不是','不成立','不是一种']
        right_str3 = ['是的','包括']
        wrong_str3 = ['不是','不包括','不成立']
        unclear = ['无法确定','不能确定','不确定','不知道','答案取决于具体的上下文','取决于具体情况','根据具体情况']
        no_l = ['不','无法','没有']
        right_str= [right_str1,right_str2,right_str3]
        wrong_str= [wrong_str1,wrong_str2,wrong_str3]
        exact_wrong_str= [['属于不同','不是相同'],['不是一种'],['不包括']]
        exact_right_str= [['是相同','同一种'],['是一种'],['包括']]
            # 定义真实标签和预测标签
        true_labels = []
        pred_labels = []


        for i in range(len(json_data)):
            x.append(json.loads(json_data[i]))
        print(x[0])
        # test_label 三种关系 1 相同 2 A被B包括 3 A包括B
        for c in range(1,4):
            true_labels = []
            pred_labels = []
            for i in x:
                if i['test_label']==c:
                    ap = -1
                    if i['target'][0]=='是':
                        ap = 1
                    elif i['target'][0]=='否':
                        ap = 0
                    else:
                        ap = 2
                    i['target_label'] = ap
                    ap = -1
                    #predict
                    if yes(unclear,i['predict'][0]):
                        ap = 2         
                    elif yes(wrong_str[c-1],i['predict'][0]) :
                        ap = 0
                    elif yes(right_str[c-1],i['predict'][0]) :
                        ap = 1
                    else:
                        ap = 2
                        # print(i['predict'][0])
                    pred_list = i['predict'][0].split('，')
                    if ap!=2:
                        for j in pred_list:
                            if i['query'] in j and i['rewrite'] in  j:
                                if yes(exact_wrong_str[c-1],j):
                                    ap = 0       
                                    break
                                elif yes(exact_right_str[c-1],j):
                                    ap = 1
                                    break
                    if ap == 2:
                        print(i['prompt'],pred_list,i['predict'][0])
                                   

                    i['pred_label'] = ap
        result_path = PATH.split('.')[0]
            # 检查文件夹是否存在，如果不存在就创建它
        if not os.path.exists('result/' + result_path):
            os.makedirs('result/' + result_path)

        with open('result/'+result_path+'/'+result_path+'.json','w') as f2:
            for data in x:
                jsonstr =   json.dumps(data,ensure_ascii=False)
                f2.write(jsonstr+'\n')
      
