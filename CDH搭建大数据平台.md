[TOC]

# CDH 搭建大数据平台

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

这里以 4 个系统节点搭建 Hadoop 大数据分布式平台，一个 MAster Node，三个 Slave Node。

CDH5.x 的部署和 CDH6.x 的部署不一样，这里以 CDH6.x 部署为例子


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

#### 1.修改主机名并配置 hosts

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

#### 2.关闭防火墙（基础阶段）

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

#### 3.关闭 SELinux 模块

安全增强型 Linux（Security-Enhanced Linux）简称 SELinux，它是一个 Linux 内核模块，也是 Linux 的一个安全子系统。SELinux 主要作用就是最大限度地减小系统中服务进程可访问的资源（最小权限原则）。

第一步，先查看 SELinux 模块状态

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

#### 4.启用 NTP 服务

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
restrict x.x.x.x mask 255.255.255.0 nomodify
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

#### 5.设置 ssh 免密码访问

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

#### 6.大页面

禁用透明页(所有节点）

```shell
echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

---


### JDK 与 数据库的安装

#### 1.安装 JDK

使用 Oracle 的 jdk，例如使用`jdk-8u181-linux-x64`版本。

- 首先查看各节点 linux 系统中是否已安装 jdk，如果安装了需要卸载。

```shell
# 查看系统已经装的jdk： 
rpm -qa|grep jdk
# 卸载jdk：
rpm -e --nodeps [openjdk文件名]
```

- yum 安装

```
yum install -y oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm

```



- 离线安装：将已下载好的 jdk 软件包解压到`/usr/java`，CDH 默认加载此路径。

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
ln -s /usr/java/jdk1.8.0_181/ /usr/java/current
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

#### 2.安装 Mysql

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
# 创建数据存放目录 /usr/local/mysql/data
cd /usr/local/mysql
mkdir data arch tmp

# 添加用户组 mysql 和用户 mysql
groupadd mysql
useradd -r -g mysql -G root mysql    

# 更改目录及目录下文件的用户和用户组
chown -R mysql:mysql /usr/local/mysql/
chown -R mysql:mysql /usr/local/mysql/data
```

- 编辑配置文件 my.cnf，添加配置如下：
```shell
# 创建并编辑配置文件
vi /etc/my.cnf 

# 追加写入
------------------------------------------------------------
[client]
port = 3306
socket = /usr/local/mysql/data/mysql.sock
default-character-set = utf8mb4

[mysqld]
port = 3306
socket = /usr/local/mysql/data/mysql.sock


key_buffer_size = 256M
sort_buffer_size = 2M
read_buffer_size = 2M
read_rnd_buffer_size = 4M
query_cache_size= 32M
max_allowed_packet = 16M
myisam_sort_buffer_size = 128M
tmp_table_size = 32M
thread_cache_size = 64

# network & connection
table_open_cache = 512

wait_timeout = 86400
interactive_timeout = 86400
max_connections = 600

basedir = /usr/local/mysql
datadir = /usr/local/mysql/data

#isolation level and default engine 
default-storage-engine = INNODB
transaction-isolation = READ-COMMITTED

innodb_file_per_table = 1
innodb_flush_log_at_trx_commit  = 2
innodb_log_buffer_size = 64M
innodb_buffer_pool_size = 4G
innodb_thread_concurrency = 8
innodb_flush_method = O_DIRECT
innodb_log_file_size = 512M

[mysql]
auto-rehash
default-character-set=utf8mb4

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
sql_mode=STRICT_ALL_TABLES
------------------------------------------------------------

chown mysql:mysql /etc/mysql
```

- 初始化MySQL
```shell
# 更改安装文件夹 mysql 的权限，进入 mysql 目录，并初始化 mysql
chmod -R 755 /usr/local/mysql/
cd /usr/local/mysql/
bin/mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data

# 需要链接库文件 libaio（系统没安装时会报错并且需要安装）
                                        ↓
# 注意会生成 root@localhost 登录 mysql 数据库的临时密码，密码是随机的（每个人生成的临时密码不一样）
[Note] A temporary password is generated for root@localhost: g7symwg+tJ<N
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
mysql> set password=password('cdh123456');
mysql> flush privileges;

# 远程登陆权限
mysql> grant all privileges on *.*  to  'root'@'%'  identified by 'cdh123456'  with grant option;
mysql> flush privileges;
mysql> exit

# 重启服务
systemctl restart mysqld
或
service mysqld restart
```

---

#### 3.在 Mysql 创建 CDH 数据库

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

# 先创建4个数据库及对应用户，操作步骤如下
mysql> CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE metastore DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 然后为数据库授权设置密码并FLUSH
mysql> GRANT ALL PRIVILEGES ON scm.* TO 'scm'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON amon.* TO 'amon'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON rman.* TO 'rman'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON metastore.* TO 'hive'@'%' IDENTIFIED BY '密码';
mysql> FLUSH PRIVILEGES;

# 查看授权是否正确
mysql> SHOW GRANTS FOR 'scm'@'%';
mysql> SHOW GRANTS FOR 'amon'@'%';
mysql> SHOW GRANTS FOR 'rman'@'%';
mysql> SHOW GRANTS FOR 'hive'@'%';

# 删除授权信息
mysql> DROP USER 'scm'@'%';
mysql> DROP USER 'amon'@'%';
mysql> DROP USER 'rman'@'%';
mysql> DROP USER 'hive'@'%';

# 授权 root 用户在主节点拥有所有数据库的访问权限
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'master' IDENTIFIED BY '密码' WITH GRANT OPTION;
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```


#### 4.安装jdbc驱动

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

#### 3.在 Mysql 创建 CDH 数据库

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

# 先创建4个数据库及对应用户，操作步骤如下
mysql> CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> CREATE DATABASE metastore DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 然后为数据库授权设置密码并FLUSH
mysql> GRANT ALL PRIVILEGES ON scm.* TO 'scm'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON amon.* TO 'amon'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON rman.* TO 'rman'@'%' IDENTIFIED BY '密码';
mysql> GRANT ALL PRIVILEGES ON metastore.* TO 'hive'@'%' IDENTIFIED BY '密码';
mysql> FLUSH PRIVILEGES;

# 查看授权是否正确
mysql> SHOW GRANTS FOR 'scm'@'%';
mysql> SHOW GRANTS FOR 'amon'@'%';
mysql> SHOW GRANTS FOR 'rman'@'%';
mysql> SHOW GRANTS FOR 'hive'@'%';

# 删除授权信息
mysql> DROP USER 'scm'@'%';
mysql> DROP USER 'amon'@'%';
mysql> DROP USER 'rman'@'%';
mysql> DROP USER 'hive'@'%';

# 授权 root 用户在主节点拥有所有数据库的访问权限
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'master' IDENTIFIED BY '密码' WITH GRANT OPTION;
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```



### CM 安装部署

#### 1.安装部署 CM Server & Agent

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
# 安装 http 服务
yum install -y httpd
# 启动服务
systemctl start httpd
# 设置httpd服务开机自启
systemctl enable httpd.service 

# 创建本地 parcel 源目录
mkdir -p /var/www/html/cdh6_parcel

# 将上述 parcel 目录移动到 /var/www/html目录下, 使得用户可以通过 HTTP 访问这些 rpm 包
# 将 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 重命为 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel /var/www/html/cdh6_parcel/
cp CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1 /var/www/html/cdh6_parcel/CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha
cp manifest.json /var/www/html/cdh6_parcel

# 验证，浏览器中直接输入IP/cdh6_parcel可以直接访问/var/www/html/cdh6_parcel目录及其文件
# 检查端口是否监听
netstat -lnpt | grep 7180

```






---



#### 在线+离线

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
/opt/cloudera/cm/schema/scm_prepare_database.sh mysql -hlocalhost scm scm

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
|CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel| 2019-10-11 08:45| 1.00GB|
|CDH-6.3.1-1.cdh6.3.1.p0.1470567-el7.parcel.sha1| 2019-10-11 08:45|	40B|
|manifest.json|	2019-10-11 08:45| 33.00KB|

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



构建本地 yum 源

后续增加节点，节点自动通过 http 服务下载主节点的 yum 源

主节点
```shell
yum install -y createrepo

cd /var/www/html/cm6
createrepo .


# 安装 http 服务
yum install -y httpd
# 启动服务
systemctl start httpd
# 设置 httpd 服务开机自启
systemctl enable httpd.service 


使用本地浏览器访问IP/cm6等。需要修改cm6等文件夹权限

chmod -R 755 cm6ll


```


所有节点

```shell
cat >> /etc/yum.repos.d/cm6.repo << EOF
[cm-local]
name=cm6-local
baseurl=http://cdh001/cm6
enabled=1
gpgcheck=0
EOF
```

查看yum源是否生效

```
yum clean all
yum repolist




在所有节点安装cm6和其他依赖

```shell
yum install -y bind-utils libxslt cyrus-sasl-plain cyrus-sasl-gssapi portmap fuse-libs /lib/lsb/init-functions httpd mod_ssl openssl-devel python-psycopg2 MySQL-python fuse log4j

```

主节点
```shell
yum install -y cloudera-manager-daemons 
yum install -y cloudera-manager-server 
yum install -y cloudera-manager-server-db-2
```


执行CM数据库初始化脚本
```shell
/opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h localhost -uroot -pcdh123 --scm-host localhost scm scm cdh123

```























---

### web 界面部署-CDH的安装

http://[主机ip]:7180/cmf/login 访问CM

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





cm5


```shell

mkdir /opt/cloudera-manager

tar -xzvf cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz -C /opt/cloudera-manager/

# 所有节点修改 agent 配置
cd /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/
vi config.ini
-------------------------------------------
server_host=cdh001
-------------------------------------------

# 主节点修改 server 配置
cd /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-server/
vi db.properties
---------------------------------------
com.cloudera.cmf.db.type=mysql
com.cloudera.cmf.db.host=localhost
com.cloudera.cmf.db.name=cmf
com.cloudera.cmf.db.user=cmf
com.cloudera.cmf.db.password=cdh123
com.cloudera.cmf.db.setupType=EXTERNAL
----------------------------------------

# 所有节点创建cloudera-scm用户，修改文件夹用户、用户组
useradd --system --home=/opt/cloudera-manager/cm-5.16.1/run/cloudera-scm-server/ --no-create-home --shell=/bin/false cloudera-scm
chown -R cloudera-scm:cloudera-scm /opt/cloudera-manager

# parcel文件离线源（主节点）
mkdir -p /opt/cloudera/parcel-repo/

# 将相关文件拷贝到主节点/opt/cloudera/parcel-repo/
cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel /opt/cloudera/parcel-repo/
cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 /opt/cloudera/parcel-repo/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
cp manifest.json /opt/cloudera/parcel-repo/

# 校验文件是否损坏
/usr/bin/sha1sum CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel

cat CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha

# 检查数值是否一致
703728dfa7690861ecd3a9bcd412b04ac8de7148

# 修改权限
chown -R cloudera-scm:cloudera-scm /opt/cloudera



# 所有节点创建大数据软件的安装目录，用户和用户组权限
mkdir -p /opt/cloudera/parcels
chown -R cloudera-scm:cloudera-scm /opt/cloudera


# 启动server
cd /opt/cloudera-manager/cm-5.16.1/etc/init.d/
./cloudera-scm-server start
# 查看日志
cd /opt/cloudera-manager/cm-5.16.1/log/cloudera-scm-server
tail -F cloudera-scm-server.log


# 启动agent
cd /opt/cloudera-manager/cm-5.16.1/etc/init.d/
./cloudera-scm-agent start



# 打开浏览器 http://192.168.130.126:7180
进行相应操作

```








