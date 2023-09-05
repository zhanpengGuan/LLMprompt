import pandas as pd
PATH_list = ["syno_judge_test_2type_tag2tag_open_sample_m_gpt35.json","syno_judge_test_2type_tag2tag_sample_m_gpt35.json",\
             "syno_judge_test_sample_m_gpt35-20230810.json","syno_judge_test_tag2tag_2type_reduct_sample_m_gpt35.json",\
                "syno_judge_test_tag2tag_k1_sample_m_gpt35.json",\
             "syno_judge_test_tag2tag_rand_sample_m_gpt35.json","syno_judge_test_tag2tag_sample_m_gpt35.json"]

for num_P in range(len(PATH_list)): 
    PATH = PATH_list[num_P]
    # 读取csv文件并合并
    result_path = PATH.split('.')[0]
    df = pd.DataFrame()
    for k in range(6):
        df1 = pd.read_csv('data/new_data2/sub-data/output'+str(k)+'.csv')
        df = pd.concat([df,df1])

    # 将合并后的数据写入新的csv文件
    df.to_csv('data/new_data2/output-'+str(num_P+1)+'.csv', index=False)
