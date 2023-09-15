#coding:utf-8
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

            prompt= "你现在是一名推理专家，擅长逻辑推理问题。结合你已经学习到的知识，现在再给你一些外部的知识信息如下：###有两种关系，“=”，“>”。这两种关系互斥，不能同时满足。 ### 你需要输出两个Output，其中Output1根据已有条件生成新的条件，Output2判断是否停止。你需要你要按照如下格式：\n###Output1:{根据CP规则推理，得到新的条件，如果新条件中有一个条件的首尾实体与问题的首尾实体相同，则开始判断问题的结果为是或否。否则，输出未知}\n Output2:{根据Output1的结果，输出是或否}。\n CP（condotional proof）规则推理如下，需要根据已知的条件两两合并，推出新的条件。合并规则如下。\n 规则示例1:“已知条件中有A=B，B=C。则可以推出新条件A=C。”\n规则示例2:“已知条件中有A=B，B>C。则可以推出新条件A>C”。\n 规则示例3:“已知条件中有A>B，B=C。则可以推出新条件A>C。”\n规则示例4:“已知条件中有A>B，B>C。则可以推出新条件A>C。”\n 规则示例5:“已知条件中有A>B，C>B。则无法推导出新的结论”。\n规则示例6:“已知条件中有A>B,B>A。则产生矛盾。”，\n 示例规则7:“已知条件中有A=B,A>B,则产生矛盾。”。\n 根据以上的示例规则，现在请你给出以下问题的结果。"+c_q+"下面是几个回答的示例：\n ###回答示例1：\ninput{已知条件：“五花”=“五花肉”。“猪肉”>“猪五花肉”。请问“三层肉”是否>“五花”?}\nOutput1:{\n1，根据“五花”=“五花肉”。“猪肉”>“猪五花肉”。无法推导出任何新条件。\n没有推出的新条件，因此问题的结论未知}\n Output2:{未知}\n###回答示例2：\ninput{已知条件：“五花”=“猪五花肉”。“猪五花肉”=“三层肉”。“猪肉”>“猪五花肉”。请问“三层肉”是否>“五花”?}\nOutput1:{\n1，根据“五花”=“猪五花肉”。“猪五花肉”=“三层肉”。可以推导得出新条件五花=三层肉。\n2，根据五花=猪五花肉，“猪肉”>“猪五花肉”。可以推导出新条件猪肉>五花。\n3，根据猪五花肉=三层肉，“猪肉”>“猪五花肉”。可以推导出新条件猪肉>三层肉。\n推出的3个条件中，第一个条件五花=三层肉的首尾实体与问题相同，判断问题的结果为否}\n Output2:{否}\n ###回答示例3:\ninput:{已知条件：“文具”>“书钉”。“文具用品”>“订书针”。“订书针”=“书钉”。“订书钉”=“书钉”。请问“书钉”是否>“文具用品”?}\nOutput1:{\n 1，根据“文具”>“书钉”。“订书针”=“书钉”。可以推导出新条件文具>订书针。\n 2，根据“文具”>“书钉”。“订书钉”=“书钉”。可以推导出新条件文具>订书钉。\n3，根据“文具”>“书钉”。“文具用品”=“订书针”。无法推导出新条件。\n 4，根据“文具用品”>“订书针”。“订书针”=“书钉”。可以推导出新条件文具用品>书钉。\n 5，根据“文具用品”>“订书针”。“订书钉”=“书钉”。无法推导出新条件。\n 4，根据“订书针”=“书钉”。“订书钉”=“书钉”。可以推导出新条件订书针=订书钉。\n共推导出了4个新条件，在推出的4个新条件中没有出现与问题首位实体相同的条件。因此问题的结果未知。}。\n Output2:{未知}。\n 请注意，你需要think step by step,你必须严格按照题目所给的条件和回答示例所给的格式输出结果。"
            # prompt = prompt.replace('\n','   ')
            x1.append(prompt)
    # 打开CSV文件并写入数据
    result_path = PATH.split('.')[0]

    with open('result/'+result_path+'/'+'cp_ltm_'+result_path+".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        j = 0
        for row in x1:
                writer.writerow([row])
                j+=1
                


    print('数据已写入CSV文件')
         