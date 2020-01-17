

"""
# 数据筛选、前处理

for year in range(1929,1951):
    with open("d:/test/" + str(year) + ".txt") as f:
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line.strip()[14:18] + '\t' + line.strip()[25:30].strip() +  '\t' +  line.strip()[101:108].strip() + '\t' +  line.strip()[111:116].strip() + '\n')


    with open("d:/test/file/" + str(year) + ".txt", 'w') as f:
        for i in range(1, len(data)):
            f.writelines(data[i])
"""


"""
# HBase

import happybase

connection = happybase.Connection(host="192.168.130.126", port=9090, timeout=None, autoconnect=True, table_prefix=None, table_prefix_separator=b'_', compat='0.98',  transport='buffered', protocol='binary')

connection.open()

table = connection.table('Student') 

for key, data in table.scan():
    print(key, data)

connection.close()
"""


"""
from pyhive import hive   
conn = hive.Connection(host='192.168.130.124', port=10000, username='hdfs', database='default')
cursor = conn.cursor()
cursor.execute('SELECT * FROM records LIMIT 10')
"""



