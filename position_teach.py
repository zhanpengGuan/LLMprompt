
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
            data = json.loads(json_data[i])
            prompt = data['prompt']
            index = prompt.rfind("。")+1
            st = 54 
            if prompt[st]=="。":
                 st+=1
            prompt= "关系有以下三种类型，它们不能同时存在: “A”和“B”是相同的东西；“A”是一种“B”；“A”包括“B”。已知条件为："+prompt[st:index]+\
            "请根据已知条件，推断"+prompt[index:]+"请列出所有已知条件并作答。在末尾请另起一行，给出是或不是的答案。"

            x.append(prompt)

    # 打开CSV文件并写入数据
    result_path = PATH.split('.')[0]
    with open('result/'+result_path+'/'+'position_teach_'+result_path+".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        j = 1
        for row in x:
                writer.writerow([row])

    print('数据已写入CSV文件')