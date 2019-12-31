[TOC]

## Hadoop 简介

数据本地化（data locality）特性是 Hadoop 数据处理的核心




## HDFS 分布式文件系统

### HDFS 基本概念和特性

1. 管理网络中跨多台计算机存储的文件系统称为分布式文件系统（distributed filesystem），HDFS 以流式数据访问模式（一次写入、多次读取）来存储超大文件，运行于硬件集群上。

2. HDFS 为各类分布式运算框架（如：MapReduce，Spark，Tez，……）提供数据存储服务，HDFS 中的文件在物理上是分块存储（block），块的大小可以通过配置参数（dfs.blocksize）来规定，默认大小在 hadoop2.x 版本中是 128M，老版本中是 64M。

3. 由于 namenode 将文件系统中的元数据存储在内存中，因此该文件系统所能存储的文件总数受限于 namenode 的内存容量。根据经验，每个文件、目录和数据块的存储信息大约占 150 字节，

4. HDFS 文件系统会给客户端提供**一个统一的抽象目录树**，客户端通过路径来访问文件，形如：hdfs://namenode:port/dir-a/dir-b/dir-c/file.data，**目录结构及文件分块信息(元数据)的管理由 namenode 节点承担**，namenode 是 HDFS 集群主节点，**负责维护整个 HDFS 文件系统的目录树，以及每一个路径（文件）所对应的 block 块信息（block的id，及所在的datanode服务器）**。

5. 文件的各个 block 的存储管理由 datanode 节点承担，datanode 是 HDFS 集群从节点，每一个 block 都可以在多个 datanode 上存储多个副本（副本数量也可以通过参数设置 dfs.replication）

> HDFS 是架在本地文件系统上面的分布式文件系统，它就是个软件，也就是用一套代码把底下所有机器的硬盘变成一个软件下的目录，和 ysql 没有什么区别，思想一样。


HDFS 优点：
- 支持超大文件存储
“超大文件”在这里指的是几百 MB，几百 GB，甚至几百 TB 大小的文件。目前已经有存储 PB 级数据的 Hadoop 集群了。

- 流式数据访问
一次性写入，多次读取是最高效的访问模式。数据集通常由数据源生成或从数据源复制而来，接着长时间在此数据集上进行各种分析。每次分析都将设计该数据集的大部分数据甚至全部数据，因此读取整个数据集的时间延迟比读取第一条记录的时间延迟更重要。（来一条处理一条）

- 容错能力和高可用性
通过多复本进而提供数据的容错能力和提高可用性。

HDFS 缺点：
- 不支持低时间延迟的数据访问
hadoop是为高数据吞吐量应用优化的，以提高时间延迟为代价。

- 不支持大量的小文件
由于 namenode 将文件系统的元数据存储在内存中，因此该文件系统所能存储的文件总数受限于 namenode 的内存容量。

- 不支持多用户写入文件、修改文件
hdfs 中的文件只支持单个写入者，而且写操作总是以“只添加”的方式在文件末尾写数据。不支持多个写入者的操作，也不支持在文件的任意位置进行修改。

- 不支持超强的事务
没有像关系型数据库那样，对事务有强有力的支持。

---

### 数据块 Block

HDFS 的数据块（block）的默认大小为 128 MB，HDFS 上的文件也被划分为块大小的多个分块（chunk），需要与磁盘的数据块（磁盘进行数据读写的最小单位）做区分。

HDFS 的块比磁盘的块大，其目的是为了最小化寻址开销（寻址时间与传输时间的占比）。如果块足够大，从磁盘传输数据的时间会明显大于定位这个块开始位置所需的时间。所以传输一个由多个块组成的大文件的时间取决于磁盘传输速率

数据块非常适合用于数据备份进而提供数据容错能力和提高可用性。将每个块复制到少数几个物理机上相互独立的机器上（默认为 3 个），可以确保在块、磁盘或机器发生故障后数据不会丢失

---

### HDFS 文件系统的基本操作

调用 HDFS 文件系统 Shell 命令应使用`bin/hadoop fs <args>`的形式。 
- 所有的的 FS shell 命令使用 URI 路径作为参数。URI 格式是 scheme://authority/path。对 HDFS 文件系统，scheme 是 hdfs，对本地文件系统，scheme 是 file。其中 scheme 和 authority 参数都是可选的，如果未加指定，就会使用配置中指定的默认 scheme。
- 一个 HDFS 文件或目录比如 /parent/child 可以表示成 hdfs://namenode:namenodeport/parent/child，或者更简单的 /parent/child（假设你配置文件中的默认值是 namenode:namenodeport）。大多数 FS Shell 命令的行为和对应的 Unix Shell 命令类似，不同之处会在下面介绍各命令使用详情时指出。出错信息会输出到 stderr，其他信息输出到 stdout。


常用命令
```shell
hadoop fs -help                             #获取每个命令的详细帮助文件
hadoop fs -ls [绝对/相对地址]                #显示当前目录结构，-R 递归显示目录结构
hadoop fs -mkdir                            #创建 hdfs 目录
hadoop fs -rm                               #删除文件，-R 递归删除目录和文件
hadoop fs -put [localsrc] [dst]             #从本地加载文件到 HDFS
hadoop fs -get [dst] [localsrc]             #从 hdfs 导出文件到本地
hadoop fs -copyFromLocal [localsrc] [dst]   #从本地加载文件到 HDFS，与 put 一致
hadoop fs -copyToLocal [dst] [localsrc]     #从 hdfs 导出文件到本地，与 get 一致
hadoop fs -getmerge [localsrc] [dst]        #合并下载多个文件
hadoop fs -test -e                          #检测目录和文件是否存在，存在返回值$?为0，不存在返回1
hadoop fs -cat [文件地址]                    #显示文件内容
hadoop fs -text [文件地址]                   #以字符形式打印一个文件的内容
hadoop fs -du [目录地址]                     #统计目录下各文件大小，单位字节。-du -s 汇总目录下文件大小，-du -h 显示单位
hadoop fs -tail [文件地址]                   #显示文件末尾
hadoop fs -cp [src] [dst]                   #从 hdfs 的一个路径拷贝 hdfs 的另一个路径
hadoop fs -mv [src] [dst]                   #在 hdfs 目录中移动文件
hadoop fs -chgrp [文件目录]                  #修改文件目录用户组
hadoop fs -chmod [文件目录]                  #修改文件目录权限
hadoop fs -chown [文件目录]                  #修改文件目录用户
hadoop fs -df -h /                          #统计 hdfs 文件系统的可用空间信息
hadoop fs -du -h [文件目录]                  #统计文件夹的大小信息
hadoop fs -setrep [num] [文件地址]           #设置 hdfs 中文件的副本数量
```

---

### HDFS 数据流

HDFS 集群分为两大角色：NameNode、DataNode (Secondary Namenode)
- NameNode 负责管理整个文件系统的元数据
- DataNode 负责管理用户的文件数据块
- 文件会按照固定的大小（blocksize）切成若干块后分布式存储在若干台 DataNode 上
- 每一个文件块可以有多个副本，并存放在不同的 DataNode 上
- DataNode 会定期向 NameNode 汇报自身所保存的文件 block 信息，而 NameNode 则会负责保持文件的副本数量
- HDFS 的内部工作机制对客户端保持透明，客户端请求访问 HDFS 都是通过向 NameNode 申请来进行

#### HDFS 文件写入

HDFS 文件写入基本流程：
- 客户端要向 HDFS 写入数据，首先要跟 NameNode 通信以确认可以写文件并获得接收文件 block 的 DataNode
- 然后客户端按顺序将文件逐个 block 传递给相应的 DataNode，并由接收到 block 的 DataNode 负责向其他 DataNode 复制 block 的副本

HDFS 文件写入详细流程示意图如下所示：
![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_2.png)

1. client 与 NameNode 通信请求上传文件 A，NameNode 检查目标文件是否已存在，父目录是否存在
2. NameNode 返回是否可以上传
3. client 请求第一个 block 该传输到哪些 DataNode 服务器上
4. NameNode 返回 3 个 DataNode
5. client 请求 3 台 DataNode 中的一台 DN_1 上传数据（本质上是一个 RPC 调用，建立 pipeline），DN_1 收到请求会继续调用 DN_1，然后 DN_2 调用 DN_3，将整个 pipeline 建立完成，逐级返回客户端
6. client 开始往 DN_1 上传第一个 block（先从磁盘读取数据放到一个本地内存缓存），以 packet 为单位，DN_1 收到一个 packet 就会传给 DN_2，DN_2 传给 DN_3。（DN_1 每传一个 packet 会放入一个应答队列等待应答）
7. 当一个 block 传输完成之后，client 再次请求 NameNode 上传第二个 block 的 DataNode 服务器... 重复上述步骤
8. 数据 block 全部写入完毕后，告知 NameNode，NameNode 会确认并记录元数据


#### HDFS 文件读取

HDFS 文件读取基本流程：
- 客户端将要读取的文件路径发送给NameNode，NameNode获取文件的元信息（主要是block的存放位置信息）返回给客户端，
- 客户端根据返回的信息找到相应 DataNode 逐个获取文件的 block 并在客户端本地进行数据追加合并从而获得整个文件

HDFS 文件写入详细流程：
- client 与 NameNode 通信查询元数据，NameNode 返回元数据信息，主要返回 block 存放的 DataNode 服务器
- 挑选一台 DataNode 服务器（就近原则，然后随机），请求建立 socket 流，请求读取 block 数据
- DataNode 开始发送数据（从磁盘里面读取数据后放入数据流中，以 packet 为单位来做校验）
- client 以 packet 为单位接收，先放入本地缓存，然后写入目标文件

---

### NameNode 与 DataNode 工作机制

#### NameNode 工作机制

NameNode 负责客户端请求的响应和元数据的管理维护（查询、修改）

NameNode 对数据的管理采用了三种存储形式：
- 内存元数据（NameSystem）
- 磁盘元数据镜像文件（fsimage）
- 数据操作日志文件（edits 可通过日志运算出元数据）

NameNode 元数据存储机制：
- 内存中有一份完整的元数据(内存 metadata)，同时磁盘有一个“准完整”的元数据镜像（fsimage）文件，保存在 NameNode 的工作目录中
- 数据操作日志（edits 文件）用于衔接内存 metadata 和持久化元数据镜像 fsimage，当客户端对 hdfs 中的文件进行新增或者修改操作，操作记录首先被记入 edits 日志文件中，当客户端操作成功后，相应的元数据会更新到内存 metadata 中
- fsimage 文件保存着文件的名字、id、分块信息、大小等信息

元数据的 checkpoint:
- 每隔一定的时间，Secondary NameNode 会将 NameNode 上最新的 edits 操作日志文件（下载过的 NameNode 会删除）和 fsimage（第一次会下载，以后不再下载）下载到本地节点，并加载到内存中进行合并
- NameNode 和 Secondary NameNode 的工作目录存储结构完全相同，所以，当 NameNode 故障退出需要重新恢复时，可以从 Secondary NameNode 的工作目录中将 fsimage 拷贝到 NameNode 的工作目录，以恢复 NameNode 的元数据。


##### 元数据目录结构

在 NameNode 的工作目录中主要保存着 fsimage 文件和 edits 文件，CDH 部署 HDFS 时默认路径为`/data/dfs/nn/current`，工作目录的文件结构如下：

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_3.png)

其中`dfs.namenode.name.dir`的默认路径是在`hdfs-site.xml`文件中配置的

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_4.png)

备注：`dfs.namenode.name.dir`属性可以配置多个目录，如`/data1/dfs/name`，`/data2/dfs/name`，`/data3/dfs/name`…，各个目录存储的文件结构和内容都完全一样，相当于备份，这样做的好处是当其中一个目录损坏了，也不会影响到HDFS 的元数据，特别是当其中一个目录是 NFS（网络文件系统 Network File System，NFS）之上，即使你这台机器损坏了，元数据也得到保存。


##### 元数据目录文件

###### VERSION

VERSION 文件是 Java 属性文件

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_5.png)

- namespaceID 是文件系统的唯一标识符，在文件系统首次格式化之后生成的
- storageType 说明这个文件存储的是什么进程的数据结构信息（如果是 DataNode，`storageType=DATA_NODE`）
- cTime 表示 NameNode 存储时间的创建时间，由于我的 NameNode 没有更新过，所以这里的记录值为0，以后对 NameNode 升级之后，cTime 将会记录更新时间戳；
- layoutVersion 表示 HDFS 永久性数据结构的版本信息，只要数据结构变更，版本号也要递减，此时的 HDFS 也需要升级，否则磁盘仍旧是使用旧版本的数据结构，这会导致新版本的 NameNode 无法使用
- clusterID 是系统生成或手动指定的集群 ID
- blockpoolID 是针对每一个 Namespace 所对应的 blockpool 的 ID，上面的这个`BP-1755288495-192.168.130.124-1577070274931`就是在我的 Namespace 下的存储块池的 ID，这个 ID 同时包含了其对应的 NameNode 节点的 ip 地址`192.168.130.124`。


###### seen_txid 

- seen_txid 文件非常重要，是存放 transactionId 的文件，format 之后是 0，它代表的是 NameNode 里面的`edits_*`文件的尾数，
- NameNode 重启的时候，会按照 seen_txid 的数字，循序从头跑 edits_0000001~ 到 seen_txid 的数字。所以当你的 hdfs 发生异常重启的时候，一定要比对 seen_txid 内的数字是不是你 edits 最后的尾数，不然会发生重置 NameNode 时metaData 的资料有缺少，导致误删 Datanode 上多余 block 的资讯

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_6.png)

###### fsimage 和 edits

元数据目录主要存储着 fsimage 和 edits 文件，及其对应的 md5 校验文件

---

#### DataNode 工作机制

DataNode 存储管理用户的文件块数据，并定期向 NameNode 汇报自身所持有的 block 信息（通过心跳信息上报）

CDH 部署的 HDFS 分布式文件系统的每个 DataNode 节点的`/data/dfs/dn/current/BP-1755288495-192.168.130.124-1577070274931/current/finalized/`目录下都可以找到文件的 block 切块

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HDFS_7.png)

---

### 利用 Python 上传下载文件

使用 python hdfs 模块，安装`hdfs`模块

```shell
pip install hdfs
```

基本操作
备注：本地机器需要在`C://Windows/System32/drivers/etc/hosts`文件中建立 ip 地址与 HDFS 主机名的映射

```python
from hdfs import *

# 建立客户端与 HDFS 的 http 连接，登录用户为 hdfs
client = InsecureClient("http://192.168.130.124:50070", user="hdfs")

# 查看 HDFS 的文件目录，返回列表格式
client.list('HDFS目录')
# 新建文件夹，需要用户有相应权限
client.makedirs('HDFS目录名')
# 重命名文件，需要用户有相应权限
client.rename('HDFS原目录名','HDFS新目录名')
# 删除文件，需要用户有相应权限，参数 recursive 为是否递归删除
client.delete('HDFS目录', recursive=True) 

# 读文件
with client.read('HDFS目录') as file:
    data=file.read()
print(data.decode())

# 追加写入数据， data 为追加写入的数据
client.write('HDFS目录', data, overwrite=False, append=True, encoding='utf-8') 
# 覆盖写入数据， data 为覆盖写入的数据
client.write('HDFS目录', data, overwrite=True, append=False, encoding='utf-8')

# 上传文件
client.upload('HDFS目录','本地目录',overwrite=True)
# 下载文件
client.download('HDFS目录','本地目录')
```


批量上传文件、批量下载文件、读取文件
```python
import os
from hdfs import *

client = InsecureClient("http://cdh-port001:50070", user="hdfs")

def upload_file(remote_dir, local_dir):
    """上传本地文件到 hdfs 目录"""
    client.delete(remote_dir, recursive=True)    # 视具体情况而定
    client.makedirs(remote_dir)
    
    for file in os.listdir(local_dir):
        client.upload(remote_dir, local_dir + file)


def download_file(remote_dir, local_dir):
    """从 hdfs 目录下载文件到本地目录"""
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)

    for file in client.list(remote_dir):
        client.download(remote_dir + file, local_dir)


def read_file(remote_dir, filename):
    """读取 hdfs 目录下文件内容，将每行存入数组返回"""
    lines = []
    with client.read(remote_dir + filename, encoding='utf-8', delimiter='\n') as file:
        for line in file:
            lines.append(line.strip())

```

---

### Java API










---

## MapReduce

MapReduce 是一种可用于数据处理的编程模型，Hadoop 可以运行各种语言版本（Java、Python、Ruby）的 MapReduce 程序

MapReduce 程序本质上是并行运行的

### MapReduce 处理分析数据流程 

MapReduce 处理数据的任务过程分为两个处理阶段：map 阶段和 reduce 阶段

每一个阶段都以键-值对作为输入和输出，map 阶段对应 map 函数，reduce 阶段对应 reduce 函数

具体流程（举例）

map 阶段的输入是原始数据（文本格式），提取需要的字段数据，键（key）一般是文件中的行或列偏移量 ——> MapReduce 框架处理，基于键-值对进行排序和分组 ——> reduce 阶段接受键-值对输入对数据进行进一步的查询等处理

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/MapReduce_1.png)


### 实例：Python MapReduce 计算最高气温

#### 1. 下载数据

数据下载地址：ftp://ftp.ncdc.noaa.gov/pub/data/gsod/

可以直接使用 wget 命令下载
```shell
wget -c -r -np -nc -L -p ftp://ftp.ncdc.noaa.gov/pub/data/gsod/文件名
```


常用参数
```shell
**注意：大小写敏感！大写和小写命令代表不同操作**
-P  表示下载到哪个目录
-r  表示递归下载，下载指定网页某一目录下（包括子目录）的所有文件 
-np 不要追溯到父目录
-k  表示将下载的网页里的链接修改为本地链接（下载整个站点后脱机浏览网页，最好加上这个参数）
-p  获得所有显示网页所需的元素，如图片等
-c  断点续传
-nd 递归下载时不创建一层一层的目录，把所有的文件下载到当前目录
-o  将log日志指定保存到文件（新建一个文件）
-a  –append-output=FILE 把记录追加到FILE文件中
-A  指定要下载的文件样式列表，多个样式用逗号分隔 
-N  不要重新下载文件除非比本地文件新
-O  表示下载并以不同的文件名保存
-nc 不要覆盖存在的文件或使用，即不要重复下载已存在的文件
-m  –mirror 等价于 -r -N -l inf -nr
-L  递归时不进入其它主机，如 wget -c -r www.xxx.org/，如果网站内有一个这样的链接：www.yyy.org，不加参数-L，会递归下载 www.yyy.org 网站 
-i  后面跟一个文件，文件内指明要下载的URL（常用于多个url下载）
-nc 不要重复下载已存在的文件 --no-clobber
```

也可使用 python 脚本下载数据
```python

import os
from urllib import request
import tarfile
import gzip

def get_data(remote="ftp://ftp.ncdc.noaa.gov/pub/data/gsod/", local="d:/data/"):
    """下载数据"""
    if not os.path.exists(local):
        os.makedirs(local)

    start, end = 1929, 1950
    for year in range(start, end + 1):
        file = "gsod_{}.tar".format(year)
        path = "{0}/{1}".format(year, file)
        resp = request.urlretrieve("{0}{1}".format(remote, path), local + file)

    print(resp)

# 可手动解压 tar 文件
# 使用
```

数据内容格式如下所示：
```
b'STN--- WBAN   YEARMODA    TEMP       DEWP      SLP        STP       VISIB      WDSP     MXSPD   GUST    MAX     MIN   PRCP   SNDP   FRSHTT\n'       
b'030050 99999  19291001    45.3  4    40.0  4  1001.6  4  9999.9  0   17.1  4    4.5  4    8.9  999.9    51.1    44.1*  0.00I 999.9  000000\n'
b'030050 99999  19291002    49.5  4    45.2  4   977.6  4  9999.9  0    9.3  4   17.5  4   29.9  999.9    53.1*   44.1  99.99  999.9  010000\n'       
b'030050 99999  19291003    49.0  4    41.7  4   975.7  4  9999.9  0   10.9  4   10.0  4   23.9  999.9    53.1    46.0  99.99  999.9  010000\n'       
b'030050 99999  19291004    45.7  4    38.5  4   992.0  4  9999.9  0    6.2  4   15.2  4   36.9  999.9    53.1    44.1  99.99  999.9  010000\n'       
b'030050 99999  19291005    46.5  4    41.5  4   997.8  4  9999.9  0    7.8  4    7.2  4   13.0  999.9    48.0*   43.0  99.99  999.9  010000\n'       
b'030050 99999  19291006    49.5  4    46.5  4   990.1  4  9999.9  0    7.8  4   15.5  4   23.9  999.9    53.1*   46.0  99.99  999.9  010000\n'       
b'030050 99999  19291007    48.2  4    44.8  4   979.1  4  9999.9  0    9.3  4    9.5  4   18.1  999.9    53.1    46.0  99.99  999.9  010000\n'       
b'030050 99999  19291008    46.5  4    39.2  4   994.3  4  9999.9  0   12.4  4    6.2  4    8.9  999.9    48.9    39.9   0.00I 999.9  000000\n'       
b'030050 99999  19291009    44.7  4    40.0  4  1005.4  4  9999.9  0   10.9  4   11.0  4   13.0  999.9    48.9    43.0   0.00I 999.9  000000\n'       
b'030050 99999  19291010    48.7  4    47.0  4  1000.6  4  9999.9  0    8.4  4    8.2  4   23.9  999.9    52.0*   39.0  99.99  999.9  010000\n'       
b'030050 99999  19291011    48.7  4    39.2  4   995.5  4  9999.9  0   12.4  4   36.9  4   36.9  999.9    53.1    46.0   0.00I 999.9  000000\n'       
b'030050 99999  19291012    48.5  4    44.2  4  1009.9  4  9999.9  0    6.8  4   17.0  4   36.9  999.9    52.0*   44.1  99.99  999.9  010000\n'       
b'030050 99999  19291014    49.0  4    44.5  4  1008.5  4  9999.9  0    7.8  4   15.7  4   29.9  999.9    53.1*   46.9  99.99  999.9  010000\n'       
b'030050 99999  19291015    43.7  4    35.5  4  1024.9  4  9999.9  0   21.7  4    3.5  4    8.9  999.9    50.0    39.0   0.00I 999.9  000000\n'
b'030050 99999  19291016    48.5  4    47.3  4  1007.8  4  9999.9  0    3.1  4   18.7  4   29.9  999.9    51.1*   44.1  99.99  999.9  010000\n'
b'030050 99999  19291017    49.7  4    48.7  4   996.0  4  9999.9  0    6.3  4    1.0  4    1.9  999.9    51.1    48.9  99.99  999.9  110000\n'
b'030050 99999  19291018    48.0  4    46.2  4   997.3  4  9999.9  0    6.2  4    6.0  4    8.9  999.9    51.1    46.9  99.99  999.9  010000\n'
```



#### 2. 合并数据

```python
# 合并数据（每年）
def merge_data(year, dir, savedir):
    """把包含的gz文件的内容合并为一个 txt 文本文件"""
    files = os.listdir(dir)

    with open('{0}{1}.txt'.format(savedir, year), 'w') as newfile:
        for i, file in enumerate(files):
            with gzip.open(dir + "/" + file, 'r') as f:
                for line in f:
                    line = str(line)  

                    # 去除名称字段
                    if i and ("YEARMODA" in line):
                        continue
                    
                    # 去除 b' 和 \n'
                    line = line[2:-3] 
                    newfile.write(line + "\n")


def merges(dir="D:/data/"):
    """获取目录并调用合并数据函数"""
    files = os.listdir(dir)
    for file in files:
        merge_data(file[-4:], dir + file, savedir) 


savedir="D:/test/"  # 自由指定，非源数据目录即可

```

合并后的数据文件（txt 文件）如下图所示：
![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/MapReduce_2.png)

#### 3. 使用 python 上传数据到 HDFS

```python
import os
from hdfs import *

client = InsecureClient("http://cdh-port001:50070", user="hdfs")

def upload_file(remote_dir, local_dir):
    """上传本地文件到 hdfs 目录"""
    client.delete(remote_dir, recursive=True)    # 视具体情况而定
    client.makedirs(remote_dir)
    
    for file in os.listdir(local_dir):
        client.upload(remote_dir, local_dir + file)

remote_dir = "/test/temper"
local_dir = "D:/test/"

```


#### 4. MapReduce

原理：使用 hadoop streaming 是利用 hadoop 流的 API，stdin(标准输入)、stdout(标准输出)在 map 函数和 reduce 函数之间传递数据

实现：利用 Python 的 sys.stdin 读取输入数据，并把我们的输出传送给 sys.stdout。


##### 4.1 Mapper

原始数据，根据空格切分字符串(`line = re.split(r" *", line)`)。
根据数据集字段可知取下标为 2 和 17 的元素为**年份**和**一州每日最高温度**(年份取前 4 位，华氏温度转换成摄氏温度)。

编写`mapper.py`脚本程序

```python
# mapper
import sys
import re

def toC(fahrenheit):
    """华氏温度转换成摄氏温度（摄氏＝(°F－32)/1.8）"""
    # 四舍五入并保留两位小数
    return round((fahrenheit-32)/1.8, 2)   


def max_temperature_mapper():
    """提取年份一州每日的最高温度"""
    for line in sys.stdin:
        line = re.split(r" *", line)

        if len(line) > 17:
            fahrenheit = line[17]
            if fahrenheit != '9999.9':
                fahrenheit = fahrenheit[:-1] if fahrenheit.endswith("*") else fahrenheit
                print("{0}\t{1}".format(line[2][:4], toC(float(fahrenheit))))

max_temperature_mapper()

```

在 linux 上可以使用`cat [文件名] | python3 mapper.py`



##### 4.2 Reduce

reducer接收的数据，已经按年份排序(没有像 java mapreduce 程序按 key 合并)

编写`reducer.py`脚本程序

```python
# reducer
import sys
from itertools import groupby
from operator import itemgetter

def read():
    """hadoop数据源"""
    for line in sys.stdin:
        yield line.split("\t", 1)


def max_temperature_reducer():
    """计算每个年份的最高温度"""
    # groupby()函数进行数据的分组以及分组后的组内运算
    # groupby()函数同时返回分组关键字和一个与关键字相对应的可迭代对象
    # 分组关键词设为 year
    for year, temperature_list in groupby(read(), key=itemgetter(0)):
        # 假设初始最大温度为 0
        max_temperature = 0
        for t in temperature_list:
            if len(t) > 1:
                temp = float(t[1])
                max_temperature = temp if temp > max_temperature else max_temperature
        print("{0}\t{1}".format(year, max_temperature))
    
max_temperature_reducer()
```

备注：`itertools.groupby()`函数用法

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/MapReduce_4.png)







#### 5. 使用 hadoop command 执行程序

编写 run.sh 

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/MapReduce_3.png)

```shell
# hadoop 的 bin 的路径
HADOOP_CMD="/etc/alternatives/hadoop" 
# HADOOP_CMD="/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/bin/hadoop"  

# streaming jar包的路径
STREAM_JAR_PATH="/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/jars/hadoop-streaming-2.6.0-cdh5.16.2.jar"  

INPUT_FILE_PATH="/test/temper/" #hadoop集群上的资源输入路径
#需要注意的是 intput 文件必须是在 hadooop 集群上的 hdfs 文件中
OUTPUT_PATH="/test/temper/output"
#需要注意的是这 output 文件必须是不存在的目录

$HADOOP_CMD fs -rmr  $OUTPUT_PATH


# -mapper：用户自己写的mapper程序，可以是可执行文件或者脚本
# -reducer：用户自己写的reducer程序，可以是可执行文件或者脚本
# -file：打包文件到提交的作业中，可以是 mapper 或者 reducer 要用的输入文件，如配置文件，字典等。

$HADOOP_CMD jar $STREAM_JAR_PATH \
    -input $INPUT_FILE_PATH \
    -output $OUTPUT_PATH \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file ./mapper.py \
    -file ./reducer.py

```



















