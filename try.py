


for year in range(1929,1951):
    with open("d:/test/" + str(year) + ".txt") as f:
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line.strip()[14:18] + '\t' + line.strip()[25:30].strip() +  '\t' +  line.strip()[101:108].strip() + '\t' +  line.strip()[111:116].strip() + '\n')


    with open("d:/test/file/" + str(year) + ".txt", 'w') as f:
        for i in range(1, len(data)):
            f.writelines(data[i])

