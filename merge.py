import json


# 使用前清除result和result_k1的数据，然后更换PATH，更换save_path即可
def ifin(s_list,s):
        
    return any(i in s for i in s_list)
def yes(t_list,s):
    if ifin(t_list,s) :
        return True
    else:
        return False
# 读取json文件
PATH = "syno_judge_test_tag2tag_k1_sample_m_gpt35.json"
PATH = "syno_judge_test_tag2tag_sample_m_gpt35.json"
with open(PATH, 'r') as f:
    json_data = f.read().splitlines()
    x = []
    right_str1 = ['是的','是同一种东西','是相同的','是']
    wrong_str1 = ['不是','不成立',]
    right_str2 = ['是的','是一种']
    wrong_str2 = ['不是','不成立','不是一种']
    right_str3 = ['是的','包括']
    wrong_str3 = ['不是','不包括','不成立']
    unclear = ['无法确定','不能确定','不确定','不知道']
    right_str= [right_str1,right_str2,right_str3]
    wrong_str= [wrong_str1,wrong_str2,wrong_str3]
        # 定义真实标签和预测标签
    true_labels = []
    pred_labels = []


    for i in range(len(json_data)):
        x.append(json.loads(json_data[i]))
    print(x[0])
    # test_label 三种关系 1 相同 2 A被B包括 3 A包括B
    for i in x:
 
        true_labels = []
        pred_labels = []
        for c in range(1,4):
            if i['test_label']==c:
                
                if i['target'][0]=='是':
                    i['true_label'] = 1
                else:
                    i['true_label'] = 0
                if yes(unclear,i['predict'][0]):
                    i['pred_label'] = 2
                elif yes(wrong_str[c-1],i['predict'][0]):
                    i['pred_label'] = 0
                elif yes(right_str[c-1],i['predict'][0]):
                    i['pred_label'] = 1
                else:
                    i['pred_label'] = 2
    with open('syno.txt', 'a') as f2:
        for i in x:
            f2.write('{}\n'.format(i))
        
