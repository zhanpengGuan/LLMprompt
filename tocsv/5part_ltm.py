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

            prompt= "你现在是一名推理专家，擅长逻辑推理问题。结合你已经学习到的知识，现在再给你一些外部的知识信息如下：###有两种关系，“=”，“>”。这两种关系互斥，不能同时满足。"+c_q+"### 你需要输出两个Output，其中Output1是一步一步推理的过程，Output2是最终结果，这个结果是根据Output1的推理过程决定的。你需要你要按照如下格式：###Output1:{step1:首先按照提问中的顺序找到其中的两个元素entity a和entity b，以及提问的关系relation x。step2:再找到已知条件中所有含有这两个元素中任何一个的条件，列出来。step3:根据列出来的条件判断两者之间是否存在有向路径。判断方法如下，首先必须选择a为首部的元素，你需要写一条从首部元素开始到尾部元素结束的一条路径，并且路径中的关系只能是=或>。 形式类似下面的格式“a,relation,entity,relation，entity,...,relation,b”。其中relation只能是>或=。如果无法得到这条路径，即step2列出来的条件无法写一个从a到b的路径。则output2的结果就为否。如果存在，进入step4。step4:如果存在一条路径从a到b,并且这条路径只包括>或=,列出提问的关系relation x,如果根据传递性判断这条路径的首尾元素是否满足（首部entity，relation x,尾部entity），如果满足，Output2为是，如果不满足，则Output2为否。Output2:{根据Output1中step3的结果，输出是或否}。下面是几个示例：###示例1:input:{已知条件：“文具”>“书钉”。“文具用品”>“订书针”。“订书针”=“书钉”。“文具用品”>“订书钉”。“订书钉”=“书钉”。“文具”>“订书针”。“文具”>“订书钉”。请问“书钉”是否>“文具用品”?}output1:{step1：首先，先找出两个元素，分别是“书钉”，“文具用品”，关系是>。step2:有以下条件：“文具”>“书钉”，“订书钉”=“书钉”,“文具用品”>“订书钉”，“文具用品”>“订书针”。step3:根据step2的条件，无法写出一条路径其首部是书钉，尾部是文具用品且整个路径只包括=或>。因此不存在元素从书钉到文具用品之间的路径。}。output2:{否}。###示例2：input{已知条件：“五花”=“猪五花肉”。“猪五花肉”=“三层肉”。“猪肉”>“猪五花肉”。“五花”=“肋条肉”。“肋条肉”=“五花肉”。“五花肉”=“三层肉”。请问“三层肉”是否>“五花”?}Output1:{step1:首先，先找出两个元素，分别是“三层肉”，“五花”，关系是>。step2:有以下条件：“三层肉”=“猪五花肉”，“三层肉”=“五花肉”,“五花肉”=“肋条肉”，“肋条肉”=“五花”。step3:存在路径：三层肉=五花肉=肋条肉=五花。step4:realtion x是>,根据传递性，不满足(三层肉>五花)}Output2:{否}你必须严格按照题目所给的条件和示例所给的格式输出结果。"
            x1.append(prompt)
    # 打开CSV文件并写入数据
    result_path = PATH.split('.')[0]

    with open('result/'+result_path+'/'+'5_part_ltm2_'+result_path+".csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        j = 0
        for row in x1:
                writer.writerow([row])
                j+=1
                


    print('数据已写入CSV文件')
         