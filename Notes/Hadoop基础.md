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

> HDFS 是架在本地文件系统上面的分布式文件系统，它就是个软件，也就是用一套代码把底下所有机器的硬盘变成一个软件下的目录，和 mysql 没有什么区别，思想一样。


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
    # 分组关键词设为 year，可迭代对象为 temperature_list
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

在 linux 上可以使用`cat [文件名] | python3 mapper.py | python3 reducer.py`

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

INPUT_FILE_PATH="/test/temper/*" #hadoop集群上的资源输入路径
#需要注意的是 intput 文件必须是在 hadooop 集群上的 hdfs 文件中
OUTPUT_PATH="/test/temper/output"
#需要注意的是这 output 文件必须是不存在的目录
$HADOOP_CMD fs -rm -r  $OUTPUT_PATH


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

添加可执行权限并运行，需要同时将`run.sh`脚本文件放入`INPUT_FILE_PATH`目录下
```shell
# 修改权限
chmod 777 run.sh
# 运行
source run.sh
```

---

## HBase

Hadoop database 的简称，也就是基于 Hadoop HDFS 的数据库，是一种 NoSQL 数据库，主要适用于海量明细数据（十亿、百亿）的随机实时查询，如日志明细、交易清单、轨迹行为等。

HBase 主要解决实时数据查询问题


### HBase 表

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HBase_1.png)

HBase中一张表为例
- RowKey为行的唯一标识，所有行按照RowKey的字典序进行排序；
- 该表具有两个列族，分别是personal和office;
- 其中列族personal拥有name、city、phone三个列，列族office拥有tel、addres两个列

数据是按照列存储，每一列都单独存放，数据即索引，在查询时可以只访问指定列的数据，有效地降低了系统的I/O负担，空(null)列并不占用存储空间，表可以设计的非常稀疏，在插入数据的过程中可以动态的创建列，在HBase的表中添加数据的时候，只能一列一列的添加，不能同时添加多列


命名空间namespace
namespace命名空间指对一组表的逻辑分组，类似RDBMS中的database，方便对表在业务上划分。
HBase系统默认定义了两个缺省的namespace：

hbase：系统内建表，包含namespace和meta表
default：用户建表时未指定namespace的表都创建在此




create '表名称', '列族名称1','列族名称2','列族名称N'
put '表名称', 'RowKey名','列族名称:列名','列值'



### HBase Shell

使用`hbase shell`命令进入命令行

|命令名|描述|语法|
|----|----|----|
|`help` | 查看命令的使用描述 | `help '命令名'` |
|`whoami` | 查看当前用户信息 | `whoami` |
|`version` | 返回 HBase 版本信息 | `version` |
|`status` |	返回 HBase 集群的状态信息 |	`status` |
|`table_help` |	查看如何操作表 | `table_help` |
|`list` | 列出 HBase 中存在的所有表 | `list` |
|`list_namespace` | 列出命名空间 | `list_namespace` |
|`list_namespace_tables` | 查看命名空间下的所有表 | `list_namespace_tables '命名空间名'` |
|`describe`	| 显示表相关的详细信息 | `describe '表名'` |
|`describe_namespace` | 显示命名空间的详细信息 | `describe_namespace '命名空间名'` |
|`create` |	创建表 | `create '表名', '列族名1', '列族名2', '列族名N'` |
|`create_namespace` | 创建命名空间 | `create_namespace '命名空间名'` |
|`alter` | 修改列族	| 添加一个列族：`alter '表名', '列族名'` <br> 删除列族：`alter '表名', {NAME=> '列族名', METHOD=> 'delete'}` |
|`exists` |	测试表是否存在 | `exists '表名'` |
|`put` | 添加或修改的表的值 | `put '表名', '行键', '列族名', '列值'` <br> `put '表名', '行键', '列族名:列名', '列值'` |
|`scan` | 通过对表的扫描来获取表中的值 | 扫描整个表：`scan '表名'` <br> 扫描某个列族：`scan '表名', {COLUMN=> '列族名'}` <br> 扫描某个列族的某个列：`scan '表名', {COLUMN=> '列族名:列名'}` <br> 查询同一个列族的多个列：`scan '表名', {COLUMNS => ['列族名1:列名1', '列族名1:列名2', …]}` <br> 查询表中指定范围行的值：`scan '表名', {STARTROW => '行键名', STOPROW => '行键名'}` <br> LIMIT 返回的行数：`scan '表名', {LIMIT=> 行数}` <br> 过滤等于某个值：`scan '表名', FILTER=>"ValueFilter(=,'binary:列值')"` <br> 过滤包含某个值：`scan '表名', FILTER=>"ValueFilter(=,'substring:列值')"`|
|`get` | 获取行或单元（cell）的值 |	`get '表名', '行键'` <br> `get '表名', '行键', '列族名'` |
|`count` | 统计表中行的数量 | `count '表名'` |
|`get_counter` | 获取计数器 | `get_counter '表名', '行键', '列族:列名'` |
|`delete` |	删除指定对象的值（可以为表，行，列对应的值，另外也可以指定时间戳的值）| 删除列族的某个列：`delete '表名', '行键', '列族名:列名'` |
|`deleteall` | 删除指定行的所有元素值 | `deleteall '表名', '行键'` |
|`truncate` | 重新创建指定表（先 disable 表-> 然后 drop 表-> 最后重新 creat 表） | `truncate '表名'` |
|`enable` |	使表有效 | `enable '表名'` |
|`is_enabled` | 是否启用 | `is_enabled '表名'` |
|`disable` | 使表无效 | `disable '表名'` |
|`is_disabled` | 是否无效 | `is_disabled '表名'` |
|`drop` | 删除表（drop 的表必须是 disable 的） | `disable '表名'` <br> `drop '表名'`|
|`drop_namespace` | 删除命名空间 | `drop_namespace '命名空间名'` |
|`tools`| 列出 HBase 所支持的工具 | `tools` |	
|`exit` | 退出 HBase shell | `exit` |	
|`shutdown` | 关闭 HBase 集群（与 exit 不同） |	`shutdown` |





### Java HBase

1.首先使用 Maven 自动引入依赖的 jar 包

在`pox.xml`文件添加 HBase 的<dependency>，版本需要对应，IDEA import Changes

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/HBase_10.png)

2.Java 连接 HBase 

```


```
















### Python HBase
目前有两个库可以操作 HBase：happybase（推荐，较为简单方便）和 hbase-thrift

#### happybase

首先添加库及其依赖库
```shell
pip install happybase
pip install thrift
```

连接 HBase 及相关操作
```python
import happybase
from conf import setting

# 创建连接
connection = happybase.Connection(host="192.168.130.126", port=9090, timeout=None, autoconnect=True, table_prefix=None, table_prefix_separator=b'_', compat='0.98',  transport='buffered', protocol='binary')

参数
host：主机名 
port：端口 
timeout：超时时间 
autoconnect：连接是否直接打开 
table_prefix：用于构造表名的前缀，因为一个Hbase会被多个项目共同使用，所以就会导致 table 的命名冲突，为了解决这个问题，可以在创建 table 的时候，手动加上项目的名字作为 table 名字的前缀
table_prefix_separator：用于 table_prefix 的分隔符 
compat：兼容模式 
transport：运输模式 
protocol：协议


# 打开传输，无返回值
connection.open()
# 关闭传输，无返回值
connection.close()


--------------------------------------------------------------------------


# 显示所有表
print(connection.tables())

# 创建表，无返回值
connection.create_table(
    'mytable',
    {'cf1': dict(max_versions=10),
     'cf2': dict(max_versions=1, block_cache_enabled=False),
     'cf3': dict(),  # use defaults
    }
)

# 获取一个表对象，返回一个 happybase.table.Table 对象(返回二进制表名)
table = connection.table('mytable') 
# <happybase.table.Table name=b'mytable'>


--------------------------------------------------------------------------


# 定位 row
# 获取表中某个 cell 的值（定位于 row-key、列族：列）
row = table.row(b'row-key')
print(row[b'cf1:col1'])   # prints the value of cf1:col1

# 获取表中多个 row 的值，返回列表[(,{}),(,{})]
rows = table.rows([b'row-key-1', b'row-key-2'])
for key, data in rows:
    print(key, data)
# 也可转化为字典形式
rows_as_dict = dict(table.rows([b'row-key-1', b'row-key-2']))

# 以字典形式返回某 row 某列族某些列及其对应值
row = table.row(b'row-key', columns=[b'cf1:col1', b'cf1:col2'])
print(row[b'cf1:col1'])
print(row[b'cf1:col2'])

# 返回时间戳，例如 {b'baseInfo:age': (b'29', 1578623474628), b'baseInfo:name': (b'tom', 1578623474560)}
row = table.row(b'row-key', columns=[b'cf1:col1'], include_timestamp=True)
value, timestamp = row[b'cf1:col1']

# 检索给定行的列的所有时间戳版本（也可指定最大版本数），返回一个包含所有版本的 list
cells = table.cells(b'row-key', b'cf1:col1', versions=3, include_timestamp=True)
for value, timestamp in cells:
    print("Cell data at {}: {}".format(timestamp, value))


--------------------------------------------------------------------------


# 获取一个扫描器，返回一个 generator，输出所有行值
for key, data in table.scan():
    print(key, data)

# 设置扫描表的行范围，起始行位置，结束行位置
for key, data in table.scan(row_start=b'aaa', row_stop=b'xyz'):
    print(key, data)

# row_prefix 行号前缀，默认为 None，即不指定前缀扫描，可传入前缀来扫描符合此前缀的行 
for key, data in table.scan(row_prefix=b'abc'):
    print(key, data)


--------------------------------------------------------------------------


# 存储数据，键值对字典形式
table.put(b'row-key', {b'cf:col1': b'value1', b'cf:col2': b'value2'})
# 提供时间戳
table.put(b'row-key', {b'cf:col1': b'value1'}, timestamp=123456789)


# 删除数据，删除一行数据
table.delete(b'row-key')
# 删除数据，删除一行中某列数据
table.delete(b'row-key', columns=[b'cf1:col1', b'cf1:col2'])


# 批量存储、删除（推荐方法、效率高）
b = table.batch(timestamp=123456789)    # 根据情况选择是否指定时间戳
b.put(b'row-key-1', {b'cf:col1': b'value1', b'cf:col2': b'value2'})
b.put(b'row-key-2', {b'cf:col2': b'value2', b'cf:col3': b'value3'})
b.put(b'row-key-3', {b'cf:col3': b'value3', b'cf:col4': b'value4'})
b.delete(b'row-key-4')
b.send()

# with 语句（不需要 send 语句）
try:
    with table.batch(transaction=True) as b:
        b.put(b'row-key-1', {b'cf:col1': b'value1', b'cf:col2': b'value2'})
        b.put(b'row-key-2', {b'cf:col2': b'value2', b'cf:col3': b'value3'})
        b.put(b'row-key-3', {b'cf:col3': b'value3', b'cf:col4': b'value4'})
        b.delete(b'row-key-4')

except ValueError:
    # error handling goes here;
    raise ValueError("Something went wrong!")

# 设置 batch 大小
with table.batch(batch_size=1000) as b:
    for i in range(1200):
        # this put() will result in two mutations (two cells)
        b.put(b'row-{}'.format(i), {b'cf1:col1': b'v1', b'cf1:col2': b'v2'})


--------------------------------------------------------------------------


# 使用连接池
# 创建连接，通过参数 size 来设置连接池中连接的个数
pool = happybase.ConnectionPool(size=3, host='192.168.130.126', table_prefix='myproject')

pool = happybase.ConnectionPool(size=3, host='192.168.130.126')
with pool.connection() as connection:
    print(connection.tables())

with pool.connection() as connection:
    table = connection.table('table-name')
    row = table.row(b'row-key')


---------------------------------------------------------------------------

```













---

## Hive

Hive 是构建在 Hadoop 上的数据仓库框架，Hive 并不是数据库，只是一个 SQL 解析引擎，由 Facebook 开发且主要是让开发人员能够通过 SQL 来计算和处理 HDFS 上的结构化数据，适用于离线的批量数据计算。

Hive 中的表是纯逻辑表，就只是表的定义等，即表的元数据。Hive 本身不存储数据，它完全依赖 HDFS 和 MapReduce。这样就可以将结构化的数据文件映射为一张张数据库表，并提供完整的 SQL 查询功能，并将 SQL 语句最终转换为 MapReduce 任务进行运行。

- Hive 作为 Hadoop 的数据仓库处理工具，它所有的数据都存储在 Hadoop 兼容的文件系统（HDFS、Hbase等）中。
- **Hive 在加载数据过程中不会对数据进行任何的修改，只是将数据移动到 HDFS 中 Hive 设定的目录下，因此，Hive 不支持对数据的改写和添加，所有的数据都是在加载的时候确定的**


### Hive CLI

Hive Shell 环境是我们和 Hive 交互、发出 HiveQL 命令的主要方式，HQL 命令与 SQL 命令相似

CDH 的 hive 命令的绝对路径为`/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/bin/hive`



### Hive 基本数据类型

| 分类 | 类型 | 描述 | 字面量示例 |
|----|----|----|----|
| 数值类型-整型 | TINYINT | 1字节的带符号整数 | 100 |
|              | SMALLINT | 2字节的带符号整数 | 100，1000 |
|              | INT | 4字节的带符号整数 | 100，1000，50000 |
|              | BIGINT | 8字节带符号整数 | 100，1000*10^10 |
| 数值类型-浮点型 | FLOAT | 4字节单精度浮点数 | 1500.00 |
|                | DOUBLE | 8字节双精度浮点数 | 750000.00 |
|                | DEICIMAL | 任意精度的带符号小数 | 1.0 |
| 字符串类型 | STRING | 不设定长度，最大2GB | |
|           | VARCHAR | 字符串1-65355长度 | |
|           | CHAR | 字符串，固定长度255| |
| 布尔及二进制型 | BOOLEAN | 布尔类型，true/false | |
|               | BINARY | 二进制型 | |   
| 时间类型 | TIMESTAMP | 时间戳，纳秒级精度 | 122327493795 |
|         | DATE | 日期，只包含年月日 | '2016-03-29' |
| 复杂类型 | ARRAY | 有序的同类型字段的集合，可以使用`名称[index]`访问对应的值 | ARRAY<data_type>：array("a","b","c")|
|         | MAP | Key-Value键值对，键的类型必须是原始类型，值可以是任意类型，可以使用`名称[key]`的方式访问对应的值| MAP<primitive_type, data_type>：map("a",1,"b",2) |
|         | STRUCT | 包含不同数据类型的元素，通过`名称.字段名`的方式来得到所需要的元素 | STRUCT<col_name:data_type,...>：STRUCT('xiaoming', 12, '2018-12-12')|
|         | UNION | | UNIONTYPE<data_type,data_type,...>| 


示例：

```sql
CREATE TABLE students(
  name      STRING,   -- 姓名
  age       INT,      -- 年龄
  subject   ARRAY<STRING>,   --学科
  score     MAP<STRING,FLOAT>,  --各个学科考试成绩
  address   STRUCT<houseNumber:int, street:STRING, city:STRING, province：STRING>  --家庭居住地址
) ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```


### Hive 存储格式

Hive 会在 HDFS 为每个数据库上创建一个目录，数据库中的表是该目录的子目录，表中的数据会以文件的形式存储在对应的表目录下。Hive 支持以下几种文件存储格式：

|格式  | 说明 | 
|----|----|
|TextFile | 存储为纯文本文件。 这是 Hive 默认的文件存储格式。这种存储方式数据不做压缩，磁盘开销大，数据解析开销大。|
|SequenceFile |	SequenceFile 是 Hadoop API 提供的一种二进制文件，它将数据以<key,value>的形式序列化到文件中。这种二进制文件内部使用 Hadoop 的标准的 Writable 接口实现序列化和反序列化。它与 Hadoop API 中的 MapFile 是互相兼容的。Hive 中的 SequenceFile 继承自 Hadoop API 的 SequenceFile，不过它的 key 为空，使用 value 存放实际的值，这样是为了避免 MR 在运行 map 阶段进行额外的排序操作。|
|RCFile	RCFile | 文件格式是 FaceBook 开源的一种 Hive 的文件存储格式，首先将表分为几个行组，对每个行组内的数据按列存储，每一列的数据都是分开存储。|
|ORC Files | ORC 是在一定程度上扩展了 RCFile，是对 RCFile 的优化。|
|Avro Files	Avro | 是一个数据序列化系统，设计用于支持大批量数据交换的应用。它的主要特点有：支持二进制序列化方式，可以便捷，快速地处理大量数据；动态语言友好，Avro 提供的机制使动态语言可以方便地处理 Avro 数据。|
|Parquet | Parquet 是基于 Dremel 的数据模型和算法实现的，面向分析型业务的列式存储格式。它通过按列进行高效压缩和特殊的编码技术，从而在降低存储空间的同时提高了 IO 效率。|

> 以上压缩格式中 ORC 和 Parquet 的综合性能突出，使用较为广泛，推荐使用这两种格式。

各个存储文件类型指定方式如下：
```sql
STORED AS TEXTFILE
STORED AS SEQUENCEFILE
STORED AS ORC
STORED AS PARQUET
STORED AS AVRO
STORED AS RCFILE
```



### Hive 体系结构

Hive 的体系结构如下图所示

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/Hive_1.png)

- CLI（command-line shell）：通过 hive 命令行的的方式来操作数据；
- thrift／jdbc：通过 thrift 协议按照标准的 JDBC 的方式操作数据。



### Hive 的数据导入方式

使用筛选过字段后的气象数据举例

首先使用 CREAT TABLE 语句为气象数据（举例）新建立一个内部表

```sql
CREATE TABLE records (  
    year STRING,  
    temp INT,         
    max_temp INT,     
    min_temp INT) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

# ROW FORMAT 子句是 HQL 特有的，这个子句声明的是数据文件的每一行是由制表符分隔的文本
# STORED AS 子句指定存储格式（文件类型）
```


1. 从本地文件系统中导入数据到 Hive 内部表：

```shell
LOAD DATA LOCAL INPATH '本地文件路径' [OVERWRITE] INTO TABLE [hive数据库表名];
```

- 这一命令告诉 Hive 把指定的本地文件放入仓库目录中，Hive 的默认仓库目录为`usr/hive/warehouse/表名`，CDH 部署的默认仓库目录为`/user/hive/warehouse`（注意为 HDFS 目录）

- OVERWRITE 关键字告诉 Hive 删除表对应目录中已有的所有文件。如果省去这一关键字，Hive 就简单地把新文件加入目录中（除非重名会替换）

- Hive 仓库的表目录下可以有多个文件，使用 Hive 查询表的时候会读入所有这些文件，所以可以直接导入多个文件'文件目录/*'


2. 从 HDFS 上导入数据到 Hive 表：

```shell
# 注意，没有 LOCAL 
LOAD DATA INPATH 'HDFS文件路径' [OVERWRITE] INTO TABLE [hive数据库表名];
```


3. 从别的表中查询出相应的数据并导入到Hive表中；




4. 在创建表的时候通过从别的表中查询出相应的记录并插入到所创建的表中。





### Hive Java








### Hive Python

安装 PyHive 库及其依赖库
```
conda install pyhive
conda install sasl
```

```python
from pyhive import hive   
conn = hive.Connection(host='192.168.130.124', port=10000, username='hdfs', database='default')
cursor = conn.cursor()
cursor.execute('SELECT * FROM records LIMIT 10')

```















---


## Echarts 可视化

### 安装 Echarts

Echarts 可以看作 JS 库，构建项目之前需要下载 Echarts 库并引入到项目中

下载地址：https://echarts.apache.org/zh/download.html

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/Echarts_1.png)

可以看到下载方法有三种

一般选择从 GitHub 下载编译产物

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/Echarts_2.png)

将下载后的`echarts.js`文件放入`工程目录/js`目录下

ECharts 的引入方式就可以像 JavaScript 库一样用 script 标签引入即可

创建一个 html 文件，创建一个简单的图表
- 引入资源文件js
- 定义图表显示区域
- 初始化echarts对象
- 指定相关配置项（数据、样式）
- 渲染图表

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="js/echarts.js"></script>
</head>
<body>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main" style="width: 1200px;height:800px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'ECharts 柱状图'
            },
            tooltip: {},
            legend: {
                data:['销量','成本']
            }, 
            xAxis: {
                data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            },
            {
                name: '成本',
                type: 'bar',
                data: [0.5, 2, 3.6, 1, 1, 2]
            }
        ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>
</html>
```



### Echarts 异步加载数据

jquery








































































