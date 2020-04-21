#importing pandas
import pandas as pd

def filterRanked(data,skill_input,exp_input):
    #user required skills
    keylist = skill_input
    list_with_index= []
    len_key = len(keylist)

    #user required experience
    req_experience = int(exp_input)

    list_with_rating=[]


    for dict in data:
        
        experience_have = dict.get('Experience')

        if req_experience <= experience_have:
            exp_rate = 10
            # index_of_dict_in_list.append(data.index(dict))
            skill_list = dict.get('Skills')
            total_rating,count=0,0

            for item in keylist:
                if item in skill_list:
                    count+=1

            if count !=0:
                diff = len_key - count
                skill_rate = 10 - ((len_key/10) * diff)

                if count == len_key:
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
    # sorted_list_with_rating = sorted(list_with_rating, key = lambda i:i['Experience'])
    # sorted_list_with_rating = sorted(list_with_rating, key = lambda i:i['Skill_Count'], reverse = True)
    df = pd.DataFrame(sorted_list_with_rating)
    df.to_csv('data1.csv')
    print('done')
    # print(sorted_list_with_rating)
    return sorted_list_with_rating
