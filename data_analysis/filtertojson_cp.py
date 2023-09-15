import codecs
import json
import os
import csv
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
PATH_list = ["syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json"]


for num_P in range(len(PATH_list)): 
    # 读取文件
    PATH = PATH_list[num_P]
    result_path = PATH.split('.')[0]
    row_tp = []
    with open('result/'+result_path+'/'+'cp_ltm'+result_path+".csv", 'r') as f:
        json_data = f.read().splitlines()
        order = []
        for i in range(len(json_data)):
            s = json_data[i][7:-270]
            order.append(s)

        def my_sort(value):
        
            for i, s in enumerate(order):
                if s in value[0]:
                    
                    return i
      
            return len(order)
        
        
        with open("data/test/output-11.csv", 'rb') as f:
            result = chardet.detect(f.read())
            print(result['encoding'])
        with codecs.open("data/test/output-11.csv", 'r',encoding = 'gb18030' ) as f:
            # 创建CSV读取器
            reader = csv.reader(f)
    
            for row in reader:
                # 处理每行数据
                data = row
                # 输出处理结果
              
                if not row[0].startswith("origin"):
                    row_tp.append(row)
        row_tp.sort(key=my_sort)
        for ix in row_tp:
            if "枣" in ix[0]:

                if order[1] in ix[0]:
                    print("yes")

    PATH = PATH_list[num_P]
    with open(PATH, 'r') as f:
        json_data = f.read().splitlines()
        x = []
        right_str1 = ['是的','是同一种东西','是相同的','是']
        wrong_str1 = ['不是','不成立',"否"]
        right_str2 = ['是的','是一种','是']
        wrong_str2 = ['不是','不成立','不是一种',"否"]
        right_str3 = ['是的','包括','是']
        wrong_str3 = ['不是','不包括','不成立',"否"]
        unclear = ['无法确定','不能确定','不确定','不知道','答案取决于具体的上下文','取决于具体情况','根据具体情况','无法推断','无法']
        no_l = ['不','无法','没有']
        right_str= [right_str1,right_str2,right_str3]
        wrong_str= [wrong_str1,wrong_str2,wrong_str3]
        exact_wrong_str= [['属于不同','不是相同','不是同一种','并非同一种'],['不是一种'],['不包括']]
        exact_right_str= [['是相同','同一种'],['是一种'],['包括']]
            # 定义真实标签和预测标签
        true_labels = []
        pred_labels = []
        #记录下来所有没有证据的条件
        filter = []
        


        for i in range(len(json_data)):
            x.append(json.loads(json_data[i]))

        new_x = []
        for c in range(1,4):
            true_labels = []
            pred_labels = []
            #记录下来所有没有证据的条件
            filter = []
            
            for i_num,i in enumerate(x):
                if i['test_label']==c:
                    ap = -1
                    if i['context']['tag2tag']=="":
                        continue
                    if i['target'][0]=='是':
                        true_labels.append(1)
                        ap = 1
                    elif i['target'][0]=='否':
                        true_labels.append(0)
                        ap = 0
                    else:
                        true_labels.append(2)
                        ap = 2
                    
                    
                    i['true_label'] = ap
                    i['prompt'] = row_tp[i_num][0]
                    i['predict'][0] = row_tp[i_num][1]
                    #predict
                    predict = i['predict'][0]
                    index1 = predict.find("output1:") if predict.find("output1:")!=-1 else predict.find("Output1:")
                    index2 = predict.find("output2:") if predict.find("output2:")!=-1 else predict.find("Output2:")
                    if yes( wrong_str1,predict[-20:]):        
                        ap = 0
                    elif yes(right_str1,predict[-20:]):        
                        ap = 1
                    else:
                        ap = 2                 
                                    
                    i['pred_label'] = ap
                    pred_labels.append(ap)
                    new_x.append(i)
                    
            
            # 计算真正例（True Positive，TP）、假正例（False Positive，FP）、真反例（True Negative，TN）、假反例（False Negative，FN）的数量
            TP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 1 and pred_labels[i] == 1])
            FP = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] == 1])
            TN = sum([1 for i in range(len(true_labels)) if true_labels[i] == 0 and pred_labels[i] != 1])
            FN = sum([1 for i in range(len(true_labels)) if true_labels[i] == 1 and pred_labels[i] != 1])

            # 计算精确率（Precision）和召回率（Recall）
            precision = TP / (TP + FP) if (TP+FP) != 0 else 0
            recall = TP / (TP + FN)
            Accuracy = (TP + TN) / (TP + TN + FP + FN)
            f1 = 2*precision*recall/(precision+recall)

            # 打印结果
            print('TP:', TP)
            print('FP:', FP)
            print('TN:', TN)
            print('FN:', FN)
            print('Precision:', precision)
            print('Recall:', recall)
            print('f1:', f1)
            print(len(true_labels))
            # 将结果保存到文件中
            num = 0
            for j in pred_labels:
                if j==2:
                    num+=1
            result_path = PATH.split('.')[0]
            p_n = len(pred_labels)
            # 检查文件夹是否存在，如果不存在就创建它
            if not os.path.exists('result/' + result_path):
                os.makedirs('result/' + result_path)



            with open('result/'+result_path+'/5_part_ltm2_'+result_path+'.json','w') as f2:
                for data in new_x:
                    jsonstr =   json.dumps(data,ensure_ascii=False)
                    f2.write(jsonstr+'\n')
          
            if c==1:
                    way='w'
            else:
                    way='a'
            try:
      
                with open('result/'+result_path+'/'+'5_part_ltm2_reslut.txt', way) as f:
                    f.write('relation:{}\n'.format(c))
                    f.write("true_labels:{}\n,true:false={}:{}\n".format(true_labels,true_labels.count(1),true_labels.count(0)))
                    f.write("pred_labels:{}\n,true:false:unclear={}:{}:{}\n".format(pred_labels,pred_labels.count(1),pred_labels.count(0),pred_labels.count(2)))
                    f.write("unclear_labels:{}\n".format(num))
                    f.write('Total:{}\n'.format(len(true_labels)))
                    f.write('TP: {}\n'.format(TP))
                    f.write('FP: {}\n'.format(FP))
                    f.write('TN: {}\n'.format(TN))
                    f.write('FN: {}\n'.format(FN))
                    f.write('Precision: {}\n'.format(precision))
                    f.write('Recall: {}\n'.format(recall))
                    f.write('f1: {}\n'.format(f1))
           
            except FileNotFoundError:

                with open('result/'+result_path+'/'+'5_part_ltm2_reslut.txt', 'w') as f:
                    f.write('relation:{}\n'.format(c))
                    f.write("true_labels:{}\n,true:false={}:{}\n".format(true_labels,true_labels.count(1),true_labels.count(0)))
                    f.write("pred_labels:{}\n,true:false:unclear={}:{}:{}\n".format(pred_labels,pred_labels.count(1),pred_labels.count(0),pred_labels.count(2)))
                    f.write("unclear_labels:{}\n".format(num))
                    f.write('Total:{}\n'.format(len(true_labels)))
                    f.write('TP: {}\n'.format(TP))
                    f.write('FP: {}\n'.format(FP))
                    f.write('TN: {}\n'.format(TN))
                    f.write('FN: {}\n'.format(FN))
                    f.write('Precision: {}\n'.format(precision))
                    f.write('Recall: {}\n'.format(recall))
                    f.write('f1: {}\n'.format(f1))