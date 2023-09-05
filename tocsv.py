
import json
import csv
PATH_list = ["syno_judge_test_tag2tag_k1_sample_m_gpt35.json","syno_judge_test_sample_m_gpt35-20230810.json","syno_judge_test_2type_tag2tag_open_sample_m_gpt35.json",\
             "syno_judge_test_2type_tag2tag_sample_m_gpt35.json","syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json","syno_judge_test_tag2tag_rand_sample_m_gpt35.json",\
                "syno_judge_test_tag2tag_sample_m_gpt35.json"]
for num_P in range(len(PATH_list)): 
    PATH = PATH_list[num_P]
    with open(PATH, 'r') as f:
        json_data = f.read().splitlines()
        x = []
     
        for i in range(len(json_data)):
            x.append(json.loads(json_data[i])['predict'][0])

    # 打开CSV文件并写入数据
    result_path = PATH.split('.')[0]
    with open('result/'+result_path+'/'+'predict.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        j = 1
        for row in x:
            if j%3==1:
                writer.writerow(['请判断这句话是否判定{}和{}是相同的东西？你只能使用“0”或者“1”回答，0代表不是，1代表是。“{}”'.format(row['predict'][0])])
            elif j%3==2:
                writer.writerow(['请判断这句话是否判定{}包括{}？{}'.format(row['predict'][0])])

    print('数据已写入CSV文件')