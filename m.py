
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
for num_P in range(len(PATH_list)): 
    PATH = PATH_list[num_P]
    with open(PATH, 'r') as f:
        json_data = f.read().splitlines()
        x = []
        right_str1 = ['是的','是同一种东西','是相同的','是']
        wrong_str1 = ['不是','不成立',]
        right_str2 = ['是的','是一种']
        wrong_str2 = ['不是','不成立','不是一种']
        right_str3 = ['是的','包括']
        wrong_str3 = ['不是','不包括','不成立']
        unclear = ['无法确定','不能确定','不确定','不知道','答案取决于具体的上下文','取决于具体情况']
        no_l = ['不','无法','没有']
        right_str= [right_str1,right_str2,right_str3]
        wrong_str= [wrong_str1,wrong_str2,wrong_str3]
        exact_wrong_str= [['属于不同','不是相同'],['不是一种'],['不包括']]
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
                        true_labels.append(1)
                    else:
                        true_labels.append(0)
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
                                if i['query']=='龙井酥':
                                    er = 1
                                if yes(exact_wrong_str[c-1],j):
                                    ap = 0       
                                    break
                                else:
                                    
                                    ap = 1
                    if ap == 2:
                        print(i['prompt'],pred_list,i['predict'][0])
                                    

                    pred_labels.append(ap)

            # 计算真正例（True Positive，TP）、假正例（False Positive，FP）、真反例（True Negative，TN）、假反例（False Negative，FN）的数量
            TP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 1 and pred_labels[i] == 1])
            FP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] != 0])
            TN = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] == 0])
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
            result_path = PATH.split('.')[0]
            # 检查文件夹是否存在，如果不存在就创建它
            if not os.path.exists('result/' + result_path):
                os.makedirs('result/' + result_path)
            if c==1:
                    way='w'
            else:
                    way='a'
            try:
      
                with open('result/'+result_path+'/'+'reslut.txt', way) as f:
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
            except FileNotFoundError:

                with open('result/'+result_path+'/'+'reslut.txt', 'w') as f:
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