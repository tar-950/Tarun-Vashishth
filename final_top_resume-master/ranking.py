#importing pandas
import pandas as pd

def filterRanked(data,key_list,experience_min,experience_max):
    #user required skills
    keylist = key_list
    list_with_index= []
    len_list = len(keylist)

    #user required experience
    req_experience_min = experience_min
    req_experience_max = experience_max

    list_with_rating=[]

    for dict in data:
        total_rating,count=0,0        
        experience_have = dict.get('Experience')

        if req_experience_min <= experience_have and req_experience_max>=experience_have:
            exp_rate = 10
            # index_of_dict_in_list.append(data.index(dict))
            skill_list = dict.get('Skills')

            for item in keylist:
                if item in skill_list:
                    count+=1

            if count!= 0:
                diff = len_list - count
                skill_rate = 10 - ((10/len_list) * diff)

                if count == len_list:
                    #fetching skills from our data and rate them
                    total_skill = dict.get('Skill_Count')
                    left_skill_rate = (total_skill-count)/5
                    total_rating+= left_skill_rate
                
                #adding all the skills and store them for the selected list dictionary item
                total_rating+= skill_rate + exp_rate

                index_dict_in_list = data.index(dict)
                data[index_dict_in_list].update({'Rating': total_rating})
                list_with_index.append(index_dict_in_list)

    # print(index_of_dict_in_list)

    for index in list_with_index:
        list_with_rating.append(data[index])

    sorted_list_with_rating = sorted(list_with_rating, key = lambda i: (i['Rating'],i['Experience'],i['Skill_Count']), reverse= True)

    df = pd.DataFrame(sorted_list_with_rating)
    df.to_csv('data1.csv')
    print('done')
    return sorted_list_with_rating
