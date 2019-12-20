[TOC]

# CDH 搭建大数据平台

## 大数据平台简介

### 大数据关键技术

1.数据采集技术

利用ETL工具将分布的、异构数据源中的数据如关系数据、平面数据文件等，抽取到临时中间层后进行清洗、转换、集成，最后加载到数据仓库或数据集市中，成为联机分析处理、数据挖掘的基础；或者也可以把实时采集的数据作为流计算系统的输入，进行实时处理分析

2.数据存储和管理

利用分布式文件系统、数据仓库、关系数据库、NoSQL数据库、云数据库等，实现对结构化、半结构化和非结构化海量数据的存储和管理

3.数据处理与分析

利用分布式并行编程模型和计算框架，结合机器学习和数据挖掘算法，实现对海量数据的处理和分析；对分析结果进行可视化呈现，帮助人们更好地理解数据、分析数据



### 大数据计算模式及其代表产品

| 大数据计算模式 | 解决问题                       | 代表产品                                                     |
| -------------- | ------------------------------ | ------------------------------------------------------------ |
| 批处理计算     | 针对大规模数据的批量处理       | MapReduce(磁盘)**、**Spark（内存）**等                       |
| 流计算         | 针对流数据的实时计算           | Storm、S4、**Flume、Streams**、Puma、DStream、银河流数据处理平台等 |
| 图计算         | 针对大规模图结构数据的处理     | Pregel、GraphX、Hama、GoldenOrb等                            |
| 查询分析计算   | 大规模数据的存储管理和查询分析 | Dremel、Hive、Cassandra、Impala等                            |

Hadoop生态系统

- Hadoop简介

  –Hadoop是Apache软件基金会旗下的一个**开源分布式计算平台**，为用户提供了系统底层细节透明的**分布式基础架构**

  –Hadoop是基于**Java语言**开发的，具有很好的跨平台特性，并且可以部署在廉价的计算机集群中

  –Hadoop的核心是分布式文件系统**HDFS（Hadoop Distributed File System）和MapReduce**

  –Hadoop被公认为行业大数据标准开源软件，在分布式环境下提供了海量数据的处理能力

  –几乎所有主流厂商都围绕Hadoop提供开发工具、开源软件、商业化工具和技术服务，如谷歌、雅虎、微软、思科、淘宝等，都支持Hadoop

  

- Hadoop版本演变

  <插入图片1>

- Hadoop项目结构

| **组件**  | **功能**                                                     |
| --------- | ------------------------------------------------------------ |
| HDFS      | 分布式文件系统                                               |
| MapReduce | 分布式并行编程模型                                           |
| YARN      | 资源管理和调度器                                             |
| Tez       | 运行在YARN之上的下一代Hadoop查询处理框架                     |
| Hive      | Hadoop上的数据仓库                                           |
| HBase     | Hadoop上的非关系型的分布式数据库                             |
| Pig       | 一个基于Hadoop的大规模数据分析平台，提供类似SQL的查询语言Pig Latin |
| Sqoop     | 用于在Hadoop与传统数据库之间进行数据传递                     |
| Oozie     | Hadoop上的工作流管理系统                                     |
| Zookeeper | 提供分布式协调一致性服务，存储配置信息                       |
| Storm     | 流计算框架                                                   |
| Flume     | 一个高可用的，高可靠的，分布式的海量日志采集、聚合和传输的系统 |
| Ambari    | Hadoop快速部署工具，支持Apache Hadoop集群的供应、管理和监控  |
| Kafka     | 一种高吞吐量的分布式发布订阅消息系统，可以处理消费者规模的网站中的所有动作流数据 |
| Spark     | 类似于Hadoop  MapReduce的通用并行框架                        |

<插入图片2>

<插入图片3>

### 分布式文件系统

- 简介

分布式文件系统在物理结构上是由计算机集群中的多个节点构成的，这些节点分为两类，一类叫“主节点”(Master Node)或者称为“名称结点”(NameNode)，另一类叫“从节点”（Slave Node）或者称为“数据节点”(DataNode)。HDFS默认一个块64MB（Hadoop V2块大小128M），一个文件被分成多个块，以块作为存储单位。

- 整体架构

  <插入图片4>

  <插入图片5>

- 名称节点

  1.功能

名称节点记录了每个文件中各个块所在的数据节点的位置信息和负责管理分布式文件系统的命名空间（Namespace）

​      2.数据结构

它保存了两个核心的数据结构，即FsImage（镜像文件）和EditLog（编辑日志）； FsImage用于维护文件系统树以及文件树中所有的文件和文件夹的元数据；操作日志文件EditLog中记录了所有针对文件的创建、删除、重命名等操作

​     <插入图片6>

- 数据节点

数据节点是分布式文件系统HDFS的工作节点，负责数据的存储和读取，会根据客户端或者是名称节点的调度来进行数据的存储和检索，并且向名称节点定期发送自己所存储的块的列表

- 第二名称节点

  1.功能

  它是HDFS架构中的一个组成部分，它是用来保存名称节点中对HDFS 元数据信息的备份，并减少名称节点重启的时间。SecondaryNameNode一般是单独运行在一台机器上

  2.工作机制

  ​     <插入图片7>

### 分布式数据库HBase

- 简介

HBase是一个高可靠、高性能、面向列、可伸缩的分布式数据库，是谷歌BigTable的开源实现，主要用来存储非结构化和半结构化的松散数据。HBase的目标是处理非常庞大的表，可以通过水平扩展的方式，利用廉价计算机集群处理由超过10亿行数据和数百万列元素组成的数据表 

- Hadoop生态系统中HBase与其他部分的关系  

  ​    <插入图片8>

  

- HBase与传统关系数据库的对比

  1.数据类型：关系数据库采用关系模型，具有丰富的数据类型和存储方式，HBase则采用了更加简单的数据模型，它把数据存储为未经解释的**字符串**

  2.数据操作：关系数据库中包含了丰富的操作，其中会涉及复杂的多表连接。HBase操作则**不存在复杂的表与表之间的关系**，只有简单的插入、查询、删除、清空等，因为HBase在设计上就避免了复杂的表和表之间的关系

  3.存储模式：关系数据库是基于行模式存储的。HBase是基于**列存储**的，每个列族都由几个文件保存，不同列族的文件是分离的

  4.数据索引：关系数据库通常可以针对不同列构建复杂的多个索引，以提高数据访问性能。HBase只有一个**索引——行键**，通过巧妙的设计，HBase中的所有访问方法，或者通过行键访问，或者通过行键扫描，从而使得整个系统不会慢下来

  5.数据维护：在关系数据库中，更新操作会用最新的当前值去替换记录中原来的旧值，旧值被覆盖后就不会存在。而在HBase中执行更新操作时，并不会删除数据旧的版本，而是**生成一个新的版本**，旧有的版本仍然保留

  6.可伸缩性：关系数据库很难实现横向扩展，纵向扩展的空间也比较有限。相反，HBase和BigTable这些分布式数据库就是为了实现灵活的水平扩展而开发的，能够轻易地通过在集群中增加或者减少硬件数量来实现性能的伸缩

- HBase表结构

  1.简介

  HBase是一个稀疏、多维度、排序的映射表，每个值是一个未经解释的字符串，没有数据类型；用户在表中存储数据，每一行都有一个可排序的行键和任意多的列；表在水平方向由一个或者多个列族组成，一个列族中可以包含任意多个列，同一个列族里面的数据存储在一起；列族支持动态扩展，可以很轻松地添加一个列族或列，无需预先定义列的数量以及类型，所有列均以字符串形式存储，用户需要自行进行数据类型转换

​     2.元素

​     <插入图片9>

​    3.范例

​     <插入图片10>

- HBase系统架构

    <插入图片11>

  1.客户端

  包含访问HBase的接口，同时在缓存中维护着已经访问过的Region位置信息，用来加快后续数据访问过程

  2.Zookeeper

  帮助选举出一个Master作为集群的总管，并保证在任何时刻总有唯一一个Master在运行，这就避免了Master的“单点失效”问题；也是一个集群管理工具，被大量用于分布式计算，提供配置维护、域名服务、分布式同步、组服务等

  3.主服务器Master（主要负责表和Region的管理工作）

  –管理用户对表的增加、删除、修改、查询等操作

  –实现不同Region服务器之间的负载均衡

  –在Region分裂或合并后，负责重新调整Region的分布

  –对发生故障失效的Region服务器上的Region进行迁移

  4.Region服务器

  是HBase中最核心的模块，负责维护分配给自己的Region，并响应用户的读写请求

  

  ### Hive分布式数据仓库

- 简介

  –Hive 作为Hadoop 的数据仓库处理工具，它所有的数据都存储在Hadoop 兼容的文件系统中

  –Hive是一个SQL解析引擎,它将SQL语句转译成MapReduce作业并在Hadoop上执行

  –Hive表是HDFS的一个文件目录，一个表名对应一个目录名，如果有分区表的话，则分区值对应子目录名

  –Hive 在加载数据过程中不会对数据进行任何的修改，只是将数据移动到HDFS 中Hive 设定的目录下，因此，Hive 不支持对数据的改写和添加，所有的数据都是在加载的时候确定的

- 设计特点

  –支持索引，加快数据查询

  –不同的存储类型，例如，纯文本文件、HBase 中的文件

  –将元数据保存在关系数据库中，减少了在查询中执行语义检查时间

  –可以直接使用存储在Hadoop 文件系统中的数据

  –内置大量用户函数UDF 来操作时间、字符串和其他的数据挖掘工具，支持用户扩展UDF 函数来完成内置函数无法实现的操作

  –类SQL 的查询方式，将SQL 查询转换为MapReduce 的job 在Hadoop集群上执行

  –编码跟Hadoop同样使用UTF-8字符集

- Hive体系结构  

   <插入图片12>

  –用户接口主要有三个：CLI，Client 和  WUI。其中最常用的是CLI，Cli启动的时候，会同时启动一个Hive副本。Client是Hive的客户端，用户连接至Hive  Server。在启动 Client模式的时候，需要指出Hive Server所在节点，并且在该节点启动Hive Server。  WUI是通过浏览器访问Hive
  –Hive将元数据存储在数据库中，如mysql、derby。Hive中的元数据包括表的名字，表的列和分区及其属性，表的属性（是否为外部表等），表的数据所在目录等
  –解释器、编译器、优化器完成HQL查询语句从词法分析、语法分析、编译、优化以及查询计划的生成。生成的查询计划存储在HDFS中，并在随后有MapReduce调用执行
  –Hive的数据文件存储在HDFS中，大部分的查询、计算由MapReduce完成（包含*的查询，比如select * from tbl不会生成MapRedcue任务）

  

- Hive数据模型

   Hive中包含以下数据模型：Table内部表，External Table外部表，Partition分区，Bucket桶。Hive默认可以直接加载文本文件，还支持sequence file 、RCFile

  <插入图片13>

  

  –Hive数据库

  类似传统数据库的DataBase，在第三方数据库里实际是一张表。简单示例命令行 hive > create database test_database;

  

  –内部表

  Hive的内部表与数据库中的Table在概念上是类似。每一个Table在Hive中都有一个相应的目录存储数据。例如一个表pvs，它在HDFS中的路径为/wh/pvs，其中wh是在hive-site.xml中由${hive.metastore.warehouse.dir} 指定的数据仓库的目录，所有的Table数据（不包括External Table）都保存在这个目录中。删除表时，元数据与数据都会被删除

    内部表简单示例：
    创建数据文件：test_inner_table.txt

    创建表：create table test_inner_table (key string)
    加载数据：LOAD DATA LOCAL INPATH ‘filepath’ INTO TABLE test_inner_table
    查看数据：select * from test_inner_table; select count(*) from test_inner_table
    删除表：drop table test_inner_table

   

  –外部表

  外部表指向已经在HDFS中存在的数据，可以创建Partition。它和内部表在元数据的组织上是相同的，而实际数据的存储则有较大的差异。内部表的创建过程和数据加载过程这两个过程可以分别独立完成，也可以在同一个语句中完成，在加载数据的过程中，实际数据会被移动到数据仓库目录中；之后对数据对访问将会直接在数据仓库目录中完成。删除表时，表中的数据和元数据将会被同时删除。而外部表只有一个过程，加载数据和创建表同时完成（CREATE EXTERNAL TABLE ……LOCATION），实际数据是存储在LOCATION后面指定的 HDFS  路径中，并不会移动到数据仓库目录中。当删除一个External Table时，仅删除该链接
    外部表简单示例：
    创建数据文件：test_external_table.txt
    创建表：create external table test_external_table (key string)
    加载数据：LOAD DATA INPATH ‘filepath’ INTO TABLE test_inner_table
    查看数据：select * from test_external_table; •select count(*) from test_external_table
    删除表：drop table test_external_table

   

  –分区

  Partition对应于数据库中的Partition列的密集索引，但是Hive中Partition的组织方式和数据库中的很不相同。在Hive中，表中的一个Partition对应于表下的一个目录，所有的Partition的数据都存储在对应的目录中。

  例如pvs表中包含ds和city两个Partition，则对应于ds = 20090801, ctry = US 的HDFS子目录为/wh/pvs/ds=20090801/ctry=US；对应于 ds =  20090801, ctry = CA 的HDFS子目录为/wh/pvs/ds=20090801/ctry=CA

    分区表简单示例：
    创建数据文件：test_partition_table.txt
    创建表：create table test_partition_table (key string) partitioned by (dt string)
    加载数据：LOAD DATA INPATH ‘filepath’ INTO TABLE test_partition_table partition (dt=‘2006’)
    查看数据：select * from test_partition_table; select count(*) from test_partition_table
    删除表：drop table test_partition_table

  

  –桶

     Buckets是将表的列通过Hash算法进一步分解成不同的文件存储。它对指定列计算hash，根据hash值切分数据，目的是为了并行，每一个Bucket对应一个文件。分区是粗粒度的划分，桶是细粒度的划分，这样做为了可以让查询发生在小范围的数据上以提高效率。适合进行表连接查询、适合用于采样分析。

  例如将user列分散至32个bucket，首先对user列的值计算hash，对应hash值为0的HDFS目录为/wh/pvs/ds=20090801/ctry=US/part-00000；hash值为20的HDFS目录为/wh/pvs/ds=20090801/ctry=US/part-00020。

    桶的简单示例：
    创建数据文件：test_bucket_table.txt
    创建表：create table test_bucket_table (key string) clustered by (key) into 20 buckets
    加载数据：LOAD DATA INPATH ‘filepath’ INTO TABLE test_bucket_table
    查看数据：select * from test_bucket_table; set hive.enforce.bucketing = true

  

  –Hive的视图

    视图与传统数据库的视图类似。视图是只读的，它基于的基本表，如果改变，数据增加不会影响视图的呈现；如果删除，会出现问题。•如果不指定视图的列，会根据select语句后的生成
    示例：create view test_view as select * from tes

  

- Hive应用的场景

  适用场景：海量数据的存储处理、数据挖掘、海量数据的离线分析

  不适用场景：复杂的机器学习算法、复杂的科学计算、联机交互式实时查询

  

  

  ### Spark生态系统

- 简介

  Spark的生态系统主要包含了Spark Core（内存计算）、Spark SQL（交互式查询）、Spark Streaming（流处理）、MLLib和GraphX （数据挖掘）等组件

  –Spark Core：包含Spark的基本功能；尤其是定义RDD的API、操作以及这两者上的动作。其他Spark的库都是构建在RDD和Spark Core之上的

  –Spark SQL：提供通过Apache Hive的SQL变体Hive查询语言（HiveQL）与Spark进行交互的API。每个数据库表被当做一个RDD，Spark SQL查询被转换为Spark操作

  –Spark Streaming：对实时数据流进行处理和控制。Spark Streaming允许程序能够像普通RDD一样处理实时数据

  –MLlib：一个常用机器学习算法库，算法被实现为对RDD的Spark操作。这个库包含可扩展的学习算法，比如分类、回归等需要对大量数据集进行迭代的操作。

  –GraphX：控制图、并行图操作和计算的一组算法和工具的集合。GraphX扩展了RDD API，包含控制图、创建子图、访问路径上所有顶点的操作

  | **应用场景**             | **时间跨度** | **其他框架**           | **Spark生态系统中的组件** |
  | ------------------------ | ------------ | --------------------- | ------------------------- |
  | 复杂的批量数据处理        | 小时级        | MapReduce、Hive        | Spark                     |
  | 基于历史数据的交互式查询  | 分钟级、秒级   | Impala、Dremel、Drill  | Spark SQL                 |
  | 基于实时数据流的数据处理  | 毫秒、秒级     | Storm、S4              | Spark Streaming           |
  | 基于历史数据的数据挖掘    | -             | Mahout                 | MLlib                     |
  | 图结构数据的处理         | -             | Pregel、Hama           | GraphX                    |

- Spark运行架构图

  Spark运行架构包括集群资源管理器（Cluster Manager）、运行作业任务的工作节点（Worker Node）、每个应用的任务控制节点（Driver）和每个工作节点上负责具体任务的执行进程（Executor），资源管理器可以自带或Mesos或YARN

  <插入图片14>

  –Cluster Manager：在standalone模式中即为Master主节点，控制整个集群，监控worker。在YARN模式中为资源管理器

  –Worker节点：从节点，负责控制计算节点，启动Executor或者Driver

  –Driver： 运行Application 的main()函数

  –Executor：执行器，是为某个Application运行在worker node上的一个进程

---

## CDH 简介

CDH 全称 Cloudera’s Distribution Including Apache Hadoop，是 Hadoop 众多发行版本（分支）中的一种，基于稳定版本的 Apache Hadoop 构建，由 Cloudera 维护（免费）。

CDH 是一个拥有**集群自动化安装、中心化管理、集群监控、报警功能**的一个工具（软件），使得集群的安装可以从几天的时间缩短为几个小时，运维人数也会从数十人降低到几个人，极大的提高了集群管理的效率

CHD 的优点：
- 基于 Apache 协议，100% 开源
- 版本管理清晰，相较于 Apache Hadoop 在兼容性、安全性、稳定性上有增强，并且版本更新快
- 提供了部署、安装、配置工具，大大提高了集群部署的效率
- 运维简单。提供了管理、监控、诊断、配置修改的工具，管理配置方便，定位问题快速、准确，使运维工作简单，有效。

CDH 的安装：
    CDH支持Yum包、tar包、RPM包，CM（Cloudera Manager）四种安装方式。

CM（Cloudera Manager）的功能：
- 管理：对集群进行管理，例如添加、删除节点等操作
- 监控：监控集群的健康情况，对设置的各种指标和系统的具体运行情况进行全面的监控
- 诊断：对集群出现的各种问题进行诊断，并且给出建议和解决方案
- 集成：多组件可以进行版本兼容间的整合


CDH 体系架构：

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/CDH_1.png)

---


## CDH 部署 Hadoop 平台

Hadoop 分布式文件系统在物理结构上是由计算机集群中的多个节点构成的，这些节点分为两类，一类叫主节点（Master Node)，另一类叫从节点（Slave Node），Master Node 存储元数据（保存在内存中），Slave Node 存储文件块。

这里以 4 个系统节点搭建 Hadoop 大数据分布式平台，一个 Master Node，三个 Slave Node。

CDH5.x 的部署和 CDH6.x 的部署不一样


离线安装需要准备的安装包如下图所示： 
![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/CDH_6.png)  

- jdk 安装包下载地址：https://www.oracle.com/technetwork/java/javase/downloads/index.html

- mysql 安装包下载地址：https://dev.mysql.com/downloads/mysql/#downloads

- mysql JDBC 安装包下载地址：https://dev.mysql.com/downloads/connector/j/5.1.html

- CM6.x（cloudera manager6.x）安装包下载地址：https://archive.cloudera.com/cm6/
截止到目前官方 cm6.x 只有 rpm 包，cm5.x 有 tar 包

- cdh6.x 安装包下载地址：https://archive.cloudera.com/cdh6/
  

- 官方部署文档地址：https://docs.cloudera.com/documentation/enterprise/6/6.2/topics/installation.html

---

### 基础环境配置

#### 1. 修改主机名并配置 hosts

```shell
# 输入 hostname 命令可以查看当前系统的主机名，CentOS 系统的默认主机名为 localhost.localdomain
hostname
或
hostnamectl  # 返回内容更为详细

# hostnamectl 命令修改主机名（推荐）
hostnamectl set-hostname [newHostname]
# 在所有节点上把 IP 和 主机名的对应关系追加写入 /etc/hosts
vi /etc/hosts
# 追加具体内容形式如下：
--------------------------------------------------------
x.x.x.x [主机名]
x.x.x.x [主机名]
x.x.x.x [主机名]
# 追加内容也可以为 IP、主机名（域名）和主机名简写（域名简写）
--------------------------------------------------------

# 验证设置，使用 uname -a 命令查看是否有输出匹配的主机名
uname -a
# ping [主机名] 看是否能够成功
ping [主机名]
```

---

#### 2. 关闭防火墙（基础阶段）

集群是内网搭建的，对外还有一个防火墙，由它来访问内网集群。如果内网内部节点开启防火墙后，就需要在内部节点把通讯需要的端口一个个打开，如果节点数量大的话，是个很繁杂的工程。

临时关闭防火墙是为了安装更方便，安装完毕后可以根据需要设置防火墙策略，保证集群安全。关闭防火墙需要在所有节点执行

```shell
# 关闭防火墙并关闭防火墙的自启动（永久关闭）
systemctl stop firewalld
systemctl disable firewalld
```

CentOS7 默认使用 firewalld，如果需要改用 iptables，需要自行安装`yum install iptables-services`并启动服务

下面是防火墙的一些基本操作命令：

```shell
# 查看防火墙状态
systemctl status firewalld
或
service firewalld status 

# 暂时关闭防火墙
systemctl stop firewalld
或
service firewalld stop

# 暂时打开防火墙
systemctl start firewalld
或
service firewalld start

# 永久关闭防火墙（防止自启动）
systemctl disable firewalld
或
chkconfig firewalld off

# 重启防火墙（重启系统后生效）
systemctl enable firewalld
或
service firewalld restart 
```

---

#### 3. 关闭 SELinux 模块

安全增强型 Linux（Security-Enhanced Linux）简称 SELinux，它是一个 Linux 内核模块，也是 Linux 的一个安全子系统。SELinux 主要作用就是最大限度地减小系统中服务进程可访问的资源（最小权限原则）。

第一步，所有节点先查看 SELinux 模块状态

```shell
# 检查 SELinux 状态
getenforce
# 如果返回的是 Permissive 或 Disabled，那么可以跳过此步骤
```

第二步，返回的 SELinux 模块状态是`enforcing`，需要修改`/etc/selinux/config`文件，`config`文件内容如下:

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/CDH_2.png)

将 `SELINUX=enforcing` 改为 `SELINUX=permissive`或`SELINUX=disabled`，修改后保存文件（重启后永久生效）。

```shell
vi /etc/selinux/config
```

第三步，重启系统或者临时关闭 SELinux 模块

```shell
# 临时关闭 SELinux
setenforce 0
```

---

#### 4. 启用 NTP 服务

NTP 全名 Network TimeProtocol，即网络时间协议，是由 RFC 1305 定义的时间同步协议，用来在分布式时间服务器和客户端之间进行时间同步。它是把计算机的时钟同步到世界协调时 UTC，其精度在局域网内可达 0.1ms。

CDH 要求集群中的每台计算机都配置 NTP 服务。**REHL7 兼容操作系统（包括 CentOS7）默认使用 chronyd 而不是 ntpd**。如果系统上有同时安装 ntpd 和 chronyd，Cloudera Manager 会依赖 chronyd 验证时间同步，即使它没有正确同步。

一般采用所有节点卸载 chrony，只使用 ntp。

- 配置 ntpd

master 节点作为 ntp 服务器与外界对时中心同步时间，随后对所有 slave 节点提供时间同步服务，所有 slave 节点以 master 节点为基础同步时间。

1. 首先同步时区（节点时区不一样情况下）
```shell
# 查看时区
timedatectl

# 修改时区
timedatectl list-timezones 
timedatectl set-timezones [ZONE]
```

2. 所有节点安装 ntp 

```shell
# 查看是否有 chronyd 服务及其状态
systemctl status chronyd
# 在有 chronyd 服务的情况下卸载 chrony
yum -y remove chrony
# 在所有节点安装 ntp
yum install -y ntp
```

3. 修改主节点配置文件，增加同步时间服务器
```shell
vi /etc/ntp.conf

# 添加以下内容，可更改具体服务器
-----------------------------------------------
server 0.asia.pool.ntp.org
server 1.asia.pool.ntp.org
server 2.asia.pool.ntp.org
server 3.asia.pool.ntp.org

# 当外部时间不可用时，可使用本地硬件时间
server 127.127.1.0 iburst local clock
# 设置允许连接网段
restrict 192.168.130.0 mask 255.255.255.0 nomodify
-----------------------------------------------
```

4. 启动主节点 ntpd 服务
```shell
# 开启 NTP 服务
systemctl start ntpd

# 查看 NTP 服务状态
systemctl status ntpd

# 配置 NTP 服务自启动
systemctl enable ntpd

# 验证
ntpq -p
```

5. 其他所有从节点停止禁用 ntpd 服务
```shell
# 各从节点停止 ntpd 服务
systemctl stop ntpd
# 各从节点禁用 ntpd 服务
systemctl disable ntpd
```


5. 所有 slave 节点同步 master 节点时间（每 10 分钟）
```shell
# 安装 ntpdate 服务
yum install ntpdate

# 在所有从节点输入命令同步主节点时间
/usr/sbin/ntpdate [主节点名]
或
ntpdate [主节点名]

# 设置每 10 分钟同步
# crontab 让使用者在固定时间或固定间隔执行程序之用
crontab -e
# 写入
------------------------------------------
*/10 * * * * /usr/sbin/ntpdate [主节点名]
------------------------------------------
```

---

#### 5. 设置 ssh 免密码访问

在所有节点上执行下面代码生成生成私钥和公钥
```shell
ssh-keygen -t rsa
# 参数 -t rsa 表示使用 ras 算法进行加密
```

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/CDH_3.png)

执行后可以在`/root/.ssh/`目录下找到私钥`id_rsa`和公钥`id_rsa.pub`

然后将所有节点的公钥内容都拷贝到到 master 节点（主机）上的认证文件`authorized_keys`中，授权后再分发到各节点。

```shell
# master 节点上采用 ssh-copy-id 命令，会自动生成 authorized_keys 文件并将公钥内容拷贝
ssh-copy-id localhost
# 或采用追加写入
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

# 登录其他主机，拷贝其他主机的公钥内容到 master 主机上的 authorized_keys 文件中
ssh-copy-id -i [master主机名]

# 授权 authorized_keys 文件
chmod 600 /root/.ssh/authorized_keys

# 最后将授权文件分配到其他主机上，scp 命令
scp /root/.ssh/authorized_keys root@[slave主机名]:/root/.ssh/
# 可以使用同步脚本对配置文件同步发放

# 验证
ssh root@[主机名]
# 第一次远程仍然需要输入密码

# （可做）
# ssh 远程登录一个节点后会自动生成 root/.ssh/known_hosts 文件，可以远程登录所有节点后将其分发到各节点
scp /root/.ssh/known_hosts root@[slave主机名]:/root/.ssh/
```

---

#### 6. 禁用 Transparent HugePages

在所有节点禁用透明大页面（Transparent HugePages）

> 透明大页面：内存是由块管理，即众所周知的页面。超大页面是 2MB 和 1GB 大小的内存块。2MB 使用的页表可管理多 GB 内存，而 1GB 页是 TB 内存的最佳选择。红帽企业版 Linux 6 开始就采用了超大页面管理。
>
> 超大页面必须在引导时分配。它们也很难手动管理，且经常需要更改代码以便可以有效使用。因此红帽企业版 Linux 也部署了透明超大页面 (THP)。THP 是一个提取层，可自动创建、管理和使用超大页面的大多数方面。THP可以改进系统的性能。

透明 HugePages 可能会在运行时导致内存分配延迟。它与Hadoop工作负载的交互很差，并且会严重降低性能。


```shell
# 检查是否已启用 Transparent HugePages 内存
cat /sys/kernel/mm/transparent_hugepage/enabled

# 判断透明大页是否被禁用；返回 0 则表示已禁用
grep -i HugePages_Total /proc/meminfo

# 
echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

---


### JDK 与 数据库的安装

#### 1. 安装 JDK

使用 Oracle 的 jdk，例如使用`jdk-8u181-linux-x64`版本。

- 首先查看各节点 linux 系统中是否已安装 jdk，如果安装了需要卸载。

```shell
# 查看系统已经装的jdk： 
rpm -qa|grep jdk
# 卸载jdk：
rpm -e --nodeps [openjdk文件名]
```

###### 1.1 yum 安装

直接使用 yum 命令安装即可（对网络有要求）
```shell
yum install -y oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm
```

###### 1.2 离线安装

离线安装：将已下载好的 jdk 软件包解压到`/usr/java`，CDH 默认加载此路径。

```shell
# 创建 java目录
mkdir -p /usr/java

# 解压 jdk 安装包到 /usr/java 目录下，注意不能更换路径
tar -xvzf jdk-8u181-linux-x64.tar.gz -C /usr/java/

# 查看文件所属的用户组，如果不是 root:root 则需要更改文件所属的用户、用户组
chown -R root:root /usr/java
```

- 设置软链接，方便升级替换（可不做，配置环境变量时写原先的）

```shell
ln -s /usr/java/jdk1.8.0_181/ /usr/java/default
```

- 配置环境变量

```shell
vi /etc/profile
```

```shell
# 追加写入环境变量
-------------------------------------------------
# env 已设置软链接
export JAVA_HOME=/usr/java/current
export JRE_HOME=$JAVA_HOME/jre
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib

-------------------------------------------------

或

-------------------------------------------------
# env 未设置软链接
export JAVA_HOME=/usr/java/jdk1.8.0_181
export JRE_HOME=$JAVA_HOME/jre
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
-------------------------------------------------
```

- 生效环境变量

```shell
source /etc/profile
```

- 验证是否安装成功

```shell
which java
# 查看版本
java
java -verion
```

- 其他节点可以将配置同步过去即可 

```shell
scp /etc/profile [主机名]:/etc/
```

---

#### 2. 安装 Mysql

Mysql 用于 master 节点元数据的存储

- 卸载系统自带的相关数据库
```shell
# 查看系统是否已经安装了 mysql、mariadb 等数据库，CentOS7系统默认自带 mariadb-lib
rpm -qa | grep mysql
rpm -qa | grep mariadb

# --nodeps：不检查依赖
rpm -e --nodeps [mysql-libs文件名]
rpm -e --nodeps [mariadb-libs文件名]
```

- 解压缩 Mysql 安装包
```shell
# 解压 tar 包到 /usr/local（软件目录），重命名为 mysql
# 在安装包位置处解压，也可使用绝对路径
tar -zxvf mysql-5.7.28-el7-x86_64.tar.gz -C /usr/local/
mv /usr/local/mysql-5.7.28-el7-x86_64/ /usr/local/mysql 
```

- 更改所属用户和用户组（需要先添加用户组和用户）
```shell
# 创建数据存放目录 /usr/local/mysql/data，Innodb 日志存放目录 arch，临时文件目录 temp
cd /usr/local/mysql
mkdir data arch tmp

# 添加用户组 mysql 和用户 mysql
groupadd mysql
useradd -r -g mysql -G root -d /usr/local/mysql mysql    

# 更改目录及目录下文件的用户和用户组、赋权
chown -R mysql:mysql /usr/local/mysql/
chmod -R 755 /usr/local/mysql
```

- 编辑配置文件 my.cnf，添加配置如下：
```shell
# 创建并编辑配置文件
vi /etc/my.cnf 

# 覆盖写入
------------------------------------------------------------
[client]
port            = 3306
socket          = /usr/local/mysql/data/mysql.sock
default-character-set=utf8mb4

[mysqld]
port            = 3306
socket          = /usr/local/mysql/data/mysql.sock

skip-slave-start
skip-external-locking
key_buffer_size = 256M
sort_buffer_size = 2M
read_buffer_size = 2M
read_rnd_buffer_size = 4M
query_cache_size= 32M
max_allowed_packet = 16M
myisam_sort_buffer_size=128M
tmp_table_size=32M

table_open_cache = 512
thread_cache_size = 8
wait_timeout = 86400
interactive_timeout = 86400
max_connections = 600

# Try number of CPU's*2 for thread_concurrency
#thread_concurrency = 32 

#isolation level and default engine 
default-storage-engine = INNODB
transaction-isolation = READ-COMMITTED

server-id = 1739
basedir = /usr/local/mysql
datadir = /usr/local/mysql/data
pid-file = /usr/local/mysql/data/hostname.pid

#open performance schema
log-warnings
sysdate-is-now

binlog_format = ROW
log_bin_trust_function_creators=1
log-error = /usr/local/mysql/data/hostname.err
log-bin = /usr/local/mysql/arch/mysql-bin
expire_logs_days = 7

innodb_write_io_threads=16

relay-log = /usr/local/mysql/relay_log/relay-log
relay-log-index = /usr/local/mysql/relay_log/relay-log.index
relay_log_info_file= /usr/local/mysql/relay_log/relay-log.info

log_slave_updates=1
gtid_mode=OFF
enforce_gtid_consistency=OFF

# slave
slave-parallel-type=LOGICAL_CLOCK
slave-parallel-workers=4
master_info_repository=TABLE
relay_log_info_repository=TABLE
relay_log_recovery=ON

#other logs
#general_log =1
#general_log_file  = /usr/local/mysql/data/general_log.err
#slow_query_log=1
#slow_query_log_file=/usr/local/mysql/data/slow_log.err

#for replication slave
sync_binlog = 500

#for innodb options 
innodb_data_home_dir = /usr/local/mysql/data/
innodb_data_file_path = ibdata1:1G;ibdata2:1G:autoextend

innodb_log_group_home_dir = /usr/local/mysql/arch
innodb_log_files_in_group = 4
innodb_log_file_size = 1G
innodb_log_buffer_size = 200M

#根据生产需要，调整pool size 
innodb_buffer_pool_size = 2G
#innodb_additional_mem_pool_size = 50M #deprecated in 5.6
tmpdir = /usr/local/mysql/tmp

innodb_lock_wait_timeout = 1000
#innodb_thread_concurrency = 0
innodb_flush_log_at_trx_commit = 2

innodb_locks_unsafe_for_binlog=1

#innodb io features: add for mysql5.5.8
performance_schema
innodb_read_io_threads=4
innodb-write-io-threads=4
innodb-io-capacity=200
#purge threads change default(0) to 1 for purge
innodb_purge_threads=1
innodb_use_native_aio=on

#case-sensitive file names and separate tablespace
innodb_file_per_table = 1
lower_case_table_names=1

[mysqldump]
quick
max_allowed_packet = 128M

[mysql]
no-auto-rehash
default-character-set=utf8mb4

[mysqlhotcopy]
interactive-timeout

[myisamchk]
key_buffer_size = 256M
sort_buffer_size = 256M
read_buffer = 2M
write_buffer = 2M
------------------------------------------------------------

# 更改用户和用户组、赋权
chown mysql:mysql /etc/my.cnf
chmod 640 /etc/my.cnf
```

- 初始化MySQL
```shell
# 进入 mysql 目录
cd /usr/local/mysql/
# 初始化 mysql，需要链接库文件 libaio（系统没安装时会报错并且需要安装）
bin/mysqld --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --initialize
                               ↓
# 注意会生成 root@localhost 登录 mysql 数据库的临时密码，密码是随机的（每个人生成的临时密码不一样）
[Note] A temporary password is generated for root@localhost: g7symwg+tJ<N

# 可在 mysql/data 目录下 hostname.err 文件中查看
cat /usr/local/mysql/data/hostname.err | grep password
```

- 设置环境变量
```shell
# 编辑 /etc/profile 文件
vi /etc/profile

# 在 /etc/profile 文件中追加写入：
# MySQL
export PATH=$PATH:/usr/local/mysql/bin

# 生效环境变量
source /etc/profile
```

- 设置开机启动
```shell
# 复制开机启动脚本到系统服务
cp /usr/local/mysql/support-files/mysql.server /etc/rc.d/init.d/mysqld
chown mysql:mysql /etc/rc.d/init.d/mysqld

# 赋予可执行权限
chmod +x /etc/rc.d/init.d/mysqld

#删除服务
chkconfig --del mysqld
# 添加服务
chkconfig --add mysqld
chkconfig --level 345 mysqld on
```

- 启动 MySQL 服务
```
# 启动服务
systemctl start mysqld
或
service mysqld start

# 验证
systemctl status mysqld
或
service mysqld status
```

- 设置MySQL账号密码与登陆权限
```shell
# 使用初始化密码登陆
mysql -uroot -p'初始密码'

# 修改密码，注意不能使用"$"等特殊符号
mysql> set password=password('cdh123');
mysql> flush privileges;

# 远程登陆权限
mysql> grant all privileges on *.*  to  'root'@'%'  identified by 'cdh123'  with grant option;
mysql> flush privileges;
mysql> exit

# 重启服务
systemctl restart mysqld
或
service mysqld restart
```

---

#### 3. 在 Mysql 创建 CDH 数据库

根据所需要安装的服务参照下表创建对应的数据库以及数据库用户，数据库必须使用utf8编码，创建数据库时要记录好用户名及对应密码：

|服务名|数据库名|用户名|
|----|----|----|
|Cloudera Manager Server           |  scm       |   scm    |
|Activity Monitor                  |  amon      |   amon   |
|Reports Manager                   |  rman      |   rman   |
|Hue                               |  hue       |   hue    |
|Hive Metastore Server             |  metastore |   hive   |
|Sentry Server                     |  sentry    |   sentry |
|Cloudera Navigator Audit Server   |  nav       |   nav    |
|Cloudera Navigator Metadata Server|  navms     |   navms  |



```shell
mysql -u root -p

# 先创建 2 个数据库及对应用户，操作步骤如下
mysql> CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 然后为数据库授权设置密码并 FLUSH
mysql> GRANT ALL PRIVILEGES ON scm.* TO 'scm'@'%' IDENTIFIED BY 'cdh123';
mysql> GRANT ALL PRIVILEGES ON amon.* TO 'amon'@'%' IDENTIFIED BY 'cdh123';
mysql> FLUSH PRIVILEGES;

# 查看授权是否正确
mysql> SHOW GRANTS FOR 'scm'@'%';
mysql> SHOW GRANTS FOR 'amon'@'%';

# 删除授权信息（发现授权错误的情况下）
mysql> DROP USER 'scm'@'%';
mysql> DROP USER 'amon'@'%';
```


#### 4. 安装jdbc驱动

在所有节点部署 mysql jdbc jar 包

```shell
# 创建目录
mkdir -p /usr/share/java

# 重命名去除版本号
cp mysql-connector-java-5.1.48.jar /usr/share/java/mysql-connector-java.jar

# 赋予权限
cd /usr/share/java
chmod 777 mysql-connector-java.jar
```

### CM6.x 安装部署

#### 1. 离线安装部署 CM Server & Agent

cm6.x 采用 rpm 包部署

rpm 安装包如下表所示：

|Name|Last Modified|Size|
|----|----|----|
|cloudera-manager-agent-6.3.1-1466458.el7.x86_64.rpm| 2019-10-11 08:42| 9.00MB|
|cloudera-manager-daemons-6.3.1-1466458.el7.x86_64.rpm|	2019-10-11 08:42| 1.00GB|
|cloudera-manager-server-6.3.1-1466458.el7.x86_64.rpm| 2019-10-11 08:42| 11.00KB|

- 主节点
```shell
# rpm 解压（不安装依赖）
rpm -ivh cloudera-manager-daemons-6.3.1-1466458.el7.x86_64.rpm --nodeps --force
rpm -ivh cloudera-manager-server-6.3.1-1466458.el7.x86_64.rpm --nodeps --force
rpm -ivh cloudera-manager-agent-6.3.1-1466458.el7.x86_64.rpm --nodeps --force

# 编辑配置文件 /etc/cloudera-scm-server/db.properties
cd /etc/cloudera-scm-server/
vi db.properties

# 追加写入、修改
----------------------------------------------------
com.cloudera.cmf.db.host=[节点名]:3306
com.cloudera.cmf.db.name=scm
com.cloudera.cmf.db.user=scm
com.cloudera.cmf.db.password=[密码]
com.cloudera.cmf.db.setupType=EXTERNAL
----------------------------------------------------

# 启动服务，查看日志
cd /var/log/cloudera-scm-server
service cloudera-scm-server start
tail -F cloudera-scm-server.log
# 等待 7180 端口服务启动，打开 7180 端口 web 界面
```

- 从节点
```shell
# 在从节点
rpm -ivh cloudera-manager-daemons-6.3.1-1466458.el7.x86_64.rpm --nodeps --force
rpm -ivh cloudera-manager-agent-6.3.1-1466458.el7.x86_64.rpm --nodeps --force
```

- 所有节点
```shell
# 服务创建 /usr/lib/systemd/system/
vi /etc/cloudera-scm-agent/config.ini

# 修改 server_host
-------------------------------------------
server_host=[主节点名]
-------------------------------------------

# 所有节点启动agent服务
service cloudera-scm-agent start
```


- 创建本地 parcel 源
  
在 master 节点制作本地 parcel 源，parcel 源目录下文件主要如下

|Name|	Last Modified|	Size|
|----|----|----|
|`CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel`| 2019-10-11 08:45| 1.00GB|
|`CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1`| 2019-10-11 08:45|	40B|
|`manifest.json`| 2019-10-11 08:45| 33.00KB|


```shell
# 安装 httpd 服务
yum install -y httpd
# 启动服务
systemctl start httpd
# 设置 httpd 服务开机自启
systemctl enable httpd.service 

# 创建本地 parcel 源目录
mkdir -p /var/www/html/cdh6_parcel

# 将上述 parcel 目录移动到 /var/www/html 目录下, 使得用户可以通过 HTTP 访问这些 rpm 包
# 将 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 重命为 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel /var/www/html/cdh6_parcel/
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1 /var/www/html/cdh6_parcel/CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha
cp manifest.json /var/www/html/cdh6_parcel

# 修改目录权限 
chmod -R 755 /var/www/html/cdh6_parcel

# 验证，浏览器中直接输入 IP/cdh6_parcel 可以直接访问 /var/www/html/cdh6_parcel目录及其文件
# 检查端口是否监听
netstat -lnpt | grep 7180
```
---



#### 2. 在线+离线安装部署 CM Server & Agent

###### 2.1 构建本地 yum 源（可不做）

后续增加节点，节点自动通过 http 服务下载主节点的 yum 源

- 主节点
```shell
# 安装 createrepo
yum install -y createrepo

# 创建 createrepo 目录
cd /var/www/html/cm6
createrepo .

# 安装 http 服务
yum install -y httpd
# 启动服务
systemctl start httpd
# 设置 httpd 服务开机自启
systemctl enable httpd.service 

# 使用本地浏览器访问 IP/cm6 等。需要修改 cm6 等文件夹权限
chmod -R 755 cm6
```

- 所有节点
```shell
# 修改配置文件
cat >> /etc/yum.repos.d/cm6.repo << EOF
[cm-local]
name=cm6-local
baseurl=http://cdh-port001/cm6
enabled=1
gpgcheck=0
EOF

# 查看 yum 源是否生效
yum clean all
yum repolist
```

![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/cdh_7.png)

---

###### 2.2 在线 + 离线安装部署 CM Server & Agent

- 主节点
```shell
# 主节点安装 CM server & agent，会自动下载一些依赖包
yum -y install cloudera-manager-daemons-6.3.1-1466458.el7.x86_64.rpm
yum -y install cloudera-manager-server-6.3.1-1466458.el7.x86_64.rpm
yum -y install cloudera-manager-agent-6.3.1-1466458.el7.x86_64.rpm
```

- 从节点
```shell
# 从节点安装 CM agent，会自动下载一些依赖包
yum -y install cloudera-manager-daemons-6.3.1-1466458.el7.x86_64.rpm
yum -y install cloudera-manager-agent-6.3.1-1466458.el7.x86_64.rpm
```

- 初始化 CM 的数据库
```shell
/opt/cloudera/cm/schema/scm_prepare_database.sh mysql -hlocalhost -uroot -p'cdh123' scm scm
```

- 所有节点修改 agent 配置
```shell
# 在所有节点上执行修改 agent 的配置
vi /etc/cloudera-scm-agent/config.ini

# 修改 server_host
-------------------------------------------
server_host=[主节点名]
-------------------------------------------
```

- parcel 源

parcel 源目录下文件如下所示：

|Name|	Last Modified|	Size|
|----|----|----|
|`CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel`| 2019-10-11 08:45| 1.00GB|
|`CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1`| 2019-10-11 08:45|	40B|
|`manifest.json`|	2019-10-11 08:45| 33.00KB|

将相关文件拷贝到主节点目录`/opt/cloudera/parcel-repo/`

```shell
# 安装 http 服务
yum install -y httpd
# 启动服务
systemctl start httpd
# 设置 httpd 服务开机自启
systemctl enable httpd.service 

# 将相关文件拷贝到主节点/opt/cloudera/parcel-repo/
# 将 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 重命为 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel /opt/cloudera/parcel-repo
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1 /opt/cloudera/parcel-repo/CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha
cp manifest.json /opt/cloudera/parcel-repo
```

- 启动 CM server & agent 服务
```shell
# 主节点启动 server & agent 服务
systemctl start cloudera-scm-server
systemctl start cloudera-scm-agent

# 从节点启动 agent 服务
systemctl start cloudera-scm-agent
```

---

### CM5.x 安装部署

#### 离线安装部署 CM Server & Agent

```shell
# 所有节点创建安装目录 /opt/cloudera-manager
mkdir /opt/cloudera-manager
# 解压 tar 包到安装目录
tar -xzvf cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz -C /opt/cloudera-manager/

# 所有节点修改 agent 配置
cd /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/
vi config.ini
  
# 修改 server_host 参数
-------------------------------------------
server_host=cdh-port001
-------------------------------------------

# 主节点修改 server 配置
cd /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-server/
vi db.properties
# 修改
---------------------------------------
com.cloudera.cmf.db.type=mysql
com.cloudera.cmf.db.host=localhost
com.cloudera.cmf.db.name=scm
com.cloudera.cmf.db.user=scm
com.cloudera.cmf.db.password=cdh123
com.cloudera.cmf.db.setupType=EXTERNAL
----------------------------------------

# 所有节点创建 cloudera-scm 用户，修改文件夹用户、用户组
useradd --system --home=/opt/cloudera-manager/cm-5.16.1/run/cloudera-scm-server/ --no-create-home --comment "Cloudera SCM User" cloudera-scm
chown -R cloudera-scm:cloudera-scm /opt/cloudera-manager


# 配置 parcel 文件离线源（主节点）
# 创建 parcel 离线源目录
mkdir -p /opt/cloudera/parcel-repo/
# 将相关文件拷贝到主节点/opt/cloudera/parcel-repo/
cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel /opt/cloudera/parcel-repo/
cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 /opt/cloudera/parcel-repo/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
cp manifest.json /opt/cloudera/parcel-repo/
# 校验文件是否损坏
/usr/bin/sha1sum CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel
cat CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
# 检查数值是否一致
# 例如都为：703728dfa7690861ecd3a9bcd412b04ac8de7148


# 所有节点创建大数据软件的安装目录
mkdir -p /opt/cloudera/parcels
# 修改用户、用户组及权限
chown -R cloudera-scm:cloudera-scm /opt/cloudera
chmod -R 755 /opt/cloudera


# 主节点启动server
cd /opt/cloudera-manager/cm-5.16.1/etc/init.d/
./cloudera-scm-server start
# 查看日志
cd /opt/cloudera-manager/cm-5.16.1/log/cloudera-scm-server
tail -F cloudera-scm-server.log

# 所有节点启动agent
cd /opt/cloudera-manager/cm-5.16.1/etc/init.d/
./cloudera-scm-agent start
```






### web 界面部署-CDH的安装

打开浏览器 http://[主机ip]:7180/cmf/login

登录默认账号 admin:admin

版本选择免费版本 Cloudera Express

进入到Add Cluster - Installation（集群安装）

Welcome——>Cluster Basics——>Specify Hosts——>Select Repository——>Install Parcels——>Inspect Cluster——>Enter Login Credentials——>Install Agents

```
Cluster Basics：设置 Cluster Name 

Specify Hosts：两种方式：New Hosts和Currently Managed Hosts（已经启动的agent）

Select Repository：
    Parcel Reposity Settings
        Remote Parcel Repository URLS：http://[主节点名]/cdh6_parcel
    CDH and other software
        会自动找到配置的离线源

Install Parcels：
    自动安装
    看日志：cd /var/log   cloudera-scm-agent cloudera-scm-server

Inspect Cluster：
    Inspect Network Performance
    Inspect Hosts

Select Services：
    选择 Custom Services 中：Zookeeper、YARN、HDFS

Assign Roles：

Setup Database
    Activity Monitor
        输入 Mysql 数据库 amon  amon  密码
        点击Test Connection按钮验证是否连接成功

Review Changes：
    DataNode Data Directory：修改为多块磁盘，逗号分隔，学习默认

Command Details

Summary
```


