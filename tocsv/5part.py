
import json
import csv
PATH_list = ["syno_judge_test_tag2tag_k1_sample_m_gpt35.json","syno_judge_test_sample_m_gpt35-20230810.json","syno_judge_test_2type_tag2tag_open_sample_m_gpt35.json",\
             "syno_judge_test_2type_tag2tag_sample_m_gpt35.json","syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json","syno_judge_test_tag2tag_rand_sample_m_gpt35.json",\
                "syno_judge_test_tag2tag_sample_m_gpt35.json"]
for num_P in range(len(PATH_list)): 
    PATH = PATH_list[num_P]
    with open(PATH, 'r') as f:
        json_data = f.read().splitlines()
        x1 = []
     
        for i in range(len(json_data)):
            data = json.loads(json_data[i])
            prompt = data['prompt']
            input = ""
            if "input" in data:
                input = data['input']['question'].split('。')
            else:
                input = prompt[55:].split('。')
            c_q = "已知条件："
            for x in input[:-1]:
                if "包括" in x:
                    c_q+=x.replace("包括",">")
                elif "是一种" in x:
                    c_q+=x.replace("是一种","<")
                else:   
                    c_q+=x[:-6].replace("和","=")
                c_q+="。"
            c_q+="请问"
            if "包括" in  input[-1]:
                c_q+=input[-1][:-1].replace("包括",">")
            elif "是一种" in input[-1]:
                c_q+=input[-1][:-1].replace("是一种","<")
            elif "为一种" in input[-1]:
                c_q+=input[-1][:-1].replace("为一种","<")
            else:
                c_q+=input[-1][:-9].replace("和","是否=")
            c_q+="?"

            prompt= "你现在是一名推理专家，擅长逻辑推理问题。结合你已经学习到的知识，现在再给你一些外部的知识信息如下：###有两种关系，“=”，“>”。这两种关系互斥，不能同时满足。input{"+c_q+\
"}### 请一步一步思考，输出结果，你要按照如下格式：###Output1:{这一段包括了最终的结果，给出是或者不是的答案。}Output2:{这一段要根据给定的外部信息展示推导过程，并推倒出最终的结果。"\
+"Output2必须按如下的过程推理：因为有（“entity name”,“relation name”,“entity name”），（“entity name”,“relation name”,“entity name”），因此（“entity name”,“relation name”,“entity name”）成立,其中relation name就是“>”或者“=”。}###下面是一个示例:input：{“ \“霉豆"\
+"腐”=“豆腐乳”。“豆腐乳”>“南乳”。“乳腐”=“豆腐乳”。“霉豆腐”=“腐乳”。“腐乳”=“乳腐”。“腐乳”=“豆腐乳”。请问“霉豆腐”是否>“南乳”？}Output1:{是}。（此处换行符）Output2:{因为(霉豆腐,=,豆腐乳)，(豆腐乳,>,南乳),因此(霉豆腐,>，南乳)成立。}"
            x1.append(prompt)

    # 打开CSV文件并写入数据
    result_path = PATH.split('.')[0]

    with open('result/'+result_path+'/'+'5_part_wo<>2_'+result_path+".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        j = 0
        for row in x1:
                writer.writerow([row])
                j+=1
                


    print('数据已写入CSV文件')
         