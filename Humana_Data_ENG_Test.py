
data_types = {0: 'int', 1: 'string', 2: 'string', 3: 'int', 4: 'string'}

def cal_length(tlist):
    length = 0
    for i in tlist:
        length = length + len(i)
    return length


with open("C:/Users/C083478/Downloads/data.tsv", "r", encoding='UTF-16LE') as r:
    # get header and its lenght
    data = r.readlines()
    i = 0
    while i < len(data):
        # print('new_data: {0}'.format(new_data[i].strip()))
        data_list = data[i].strip().split('\t')
        new_list = []
        new_list.append(data_list)
        length = cal_length(new_list)
        if length < 5:
            while length < 5:
                i = i + 1
                new_list.append(data[i].strip().split('\t'))
                length = cal_length(new_list)
                if length == 5:
                    if len(data[i+1].strip().split('\t')) == 1:
                        i = i + 1
                        new_list.append(data[i].strip().split('\t'))
                        length = cal_length(new_list)
            data_list = []
            if cal_length(new_list) == 5:
                for j in new_list:
                    data_list = data_list + j
            elif cal_length(new_list) == 6:
                # if has two last names that are not equal, then here we will concatenate them
                if len(new_list[0]) == 3:
                    new_list[0][2] = new_list[0][2]+' '+new_list[1][0]
                    new_list[1].pop(0)
                    for j in new_list:
                        data_list = data_list + j
                elif len(new_list[0]) == 2 and len(new_list[1]) == 4:
                    # if has two equal first names
                    if new_list[0][-1].strip() == new_list[1][0].strip():
                        new_list[1].pop(0)
                    # if has two equal last names
                    elif new_list[1][0].strip() == new_list[1][1].strip():
                        new_list[1].pop(0)
                        for j in new_list:
                            data_list = data_list + j
                    else:
                        print('*'*80)
                        print('exception: {0}'.format(new_list))
                else:
                    print('*'*80)
                    print('exception: {0}'.format(new_list))
            else:
                print('*'*80)
                print('exception: {0}'.format(new_list))

        with open('result2.tsv', 'a', encoding='UTF-8') as f:
            line = '\t'.join(data_list)
            line = line+'\n'
            f.write(line)
        i = i + 1
f.close()
r.close()
