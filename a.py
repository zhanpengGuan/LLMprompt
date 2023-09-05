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
    for c in range(1,4):
        true_labels = []
        pred_labels = []
        for i in x:
            if i['test_label']==c:
                
                if i['target'][0]=='是':
                    true_labels.append(1)
                else:
                    true_labels.append(0)
                if yes(unclear,i['predict'][0]):
                    if c==1:
                        
                        print(i['predict'][0])
                    pred_labels.append(2)
                    
                    
                elif yes(wrong_str[c-1],i['predict'][0]):
                    pred_labels.append(0)
                elif yes(right_str[c-1],i['predict'][0]):
                    pred_labels.append(1)
                else:
                    pred_labels.append(2)
                    print(i['predict'][0])
        

        # 计算真正例（True Positive，TP）、假正例（False Positive，FP）、真反例（True Negative，TN）、假反例（False Negative，FN）的数量
        TP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 1 and pred_labels[i] == 1])
        FP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] == 1])
        TN = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] != 1])
        FN = sum([1 for i in range(len(true_labels)) if true_labels[i] == 1 and pred_labels[i] != 1])

        # 计算精确率（Precision）和召回率（Recall）
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)

        # 打印结果
        print('TP:', TP)
        print('FP:', FP)
        print('TN:', TN)
        print('FN:', FN)
        print('Precision:', precision)
        print('Recall:', recall)
        print(len(true_labels))
        # 将结果保存到文件中
        num = 0
        for j in pred_labels:
            if j==2:
                num+=1
        retsult_path = PATH.split('.')[0]
        with open('result.txt', 'a') as f:
            f.write('relation:{}\n'.format(c))
            f.write("true_labels:{}\n".format(true_labels))
            f.write("pred_labels:{}\n".format(pred_labels))
            f.write("unclear_labels:{}\n".format(num))
            f.write('Total:{}\n'.format(len(true_labels)))
            f.write('TP: {}\n'.format(TP))
            f.write('FP: {}\n'.format(FP))
            f.write('TN: {}\n'.format(TN))
            f.write('FN: {}\n'.format(FN))
            f.write('Precision: {}\n'.format(precision))
            f.write('Recall: {}\n'.format(recall))
