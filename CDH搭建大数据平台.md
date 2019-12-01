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

CDH5.x 的部署和 CDH6.x 的部署不一样


软件包
/usr/local/src/ 

CDH-
CDH-
manifest.json
clouder-manager-centos7-cm5
jdk：例如`jdk-8u181-linux-x64.tar.gz`
mysql-


- jdk 安装包下载地址：https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

- mysql 安装包下载地址：https://dev.mysql.com/downloads/mysql/#downloads
![](https://github.com/CZH-HW/CloudImg/raw/master/BigData/CDH_5.png)  

- mysql JDBC 安装包下载地址：

- CM6.x（cloudera manager6.x）安装包下载地址：https://archive.cloudera.com/cm6/

- cdh6.x 安装包下载地址：https://archive.cloudera.com/cdh6/

- 官方部署文档地址：https://docs.cloudera.com/documentation/enterprise/6/6.2/topics/installation.html

### 基础环境配置

#### 1.修改主机名并配置 hosts

```shell
# 输入 hostname 命令可以查看当前系统的主机名，CentOS 系统的默认主机名为 localhost.localdomain
hostname
hostnamectl  # 返回内容更为详细

# hostnamectl 命令修改主机名（推荐）
sudo hostnamectl set-hostname [newHostname]
# 在所有节点上把 IP 和 主机名的对应关系追加写入 /etc/hosts
vi /etc/hosts
# 追加具体内容形式如下：
x.x.x.x master.hadoop
x.x.x.x slave1.hadoop
x.x.x.x slave2.hadoop
x.x.x.x slave3.hadoop
# 追加内容也可以为 IP、主机名（域名）和主机名简写（域名简写）

# 验证设置，使用 uname -a 命令查看是否有输出匹配的主机名
uname -a
# ping [主机名] 看是否能够成功
ping [主机名]
```


#### 2.关闭防火墙（基础阶段）

集群是内网搭建的，对外还有一个防火墙，由它来访问内网集群。如果内网内部节点开启防火墙后，就需要在内部节点把通讯需要的端口一个个打开，如果节点数量大的话，是个很繁杂的工程。

临时关闭防火墙是为了安装更方便，安装完毕后可以根据需要设置防火墙策略，保证集群安全。关闭防火墙需要在所有节点执行

```shell
# 关闭防火墙并关闭防火墙的自启动（永久关闭）
sudo systemctl stop firewalld
sudo systemctl disable firewalld
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


#### 4.启用 NTP 服务

NTP 全名 Network TimeProtocol，即网络时间协议，是由 RFC 1305 定义的时间同步协议，用来在分布式时间服务器和客户端之间进行时间同步。它是把计算机的时钟同步到世界协调时 UTC，其精度在局域网内可达 0.1ms。

CDH 要求集群中的每台计算机都配置 NTP 服务。**REHL7 兼容操作系统（包括 CentOS7）默认使用 chronyd 而不是 ntpd**。如果系统上有同时安装 ntpd 和 chronyd，Cloudera Manager 会依赖 chronyd 验证时间同步，即使它没有正确同步。

一般采用所有节点卸载 chrony，只使用 ntp。

#### 4.1 方法一：配置 ntpd

master 节点作为 ntp 服务器与外界对时中心同步时间，随后对所有 slave 节点提供时间同步服务，所有 slave 节点以 master 节点为基础同步时间。

1. 安装 ntp 

```shell
# 查看是否有 chronyd 服务及其状态
systemctl status chronyd
# 在有 chronyd 服务的情况下卸载 chrony
yum -y remove chrony
# 在所有节点安装 ntp
yum install -y ntp
```

2. 修改主节点配置文件，增加同步时间服务器
```shell
vi /etc/ntp.conf

# 添加以下内容，可更改具体服务器
server 0.asia.pool.ntp.org
server 1.asia.pool.ntp.org
server 2.asia.pool.ntp.org
server 3.asia.pool.ntp.org
```

3. 启动主节点 ntpd 服务
```shell
# 开启 NTP 服务
systemctl start ntpd

# 配置 NTP 服务自启动
systemctl enable ntpd
```

单台机器的时间同步
```
# 安装 ntpdate
yum install ntpdate

# 向某个服务器同步时间，例如 ntp1.aliyun.com
ntpdate -u <ntp_server> 
```


4. 所有 slave 节点同步 master 节点时间
```
ntpdate [主节点主机名]
```




手动同步时区
```shell
# 查看时区
timedatectl

# 修改时区
timedatectl list-timezones 
timedatectl set-timezones [ZONE]
```

#### 4.2 方法二：配置 chronyd

所有节点安装

yum install -y chrony




vi /etc/chrony.conf

删除默认Server
新增阿里云服务器
server ntp.aliyun.com iburst
makestep 1.0 -1

重启服务并查看状态是否正常并设置开机自动启动
systemctl enable chronyd
systemctl restart chronyd
systemctl status chronyd
chronyc tracking




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
cat root/.ssh/id_rsa.pub >> root/.ssh/authorized_keys

# 登录其他主机，拷贝其他主机的公钥内容到 master 主机上的 authorized_keys 文件中
ssh-copy-id -i [master主机名]
...

# 授权 authorized_keys 文件
chmod 600 root/.ssh/authorized_keys
# 6 = 4（r） + 2（w）

# 最后将授权文件分配到其他主机上，scp 命令
scp root/.ssh/authorized_keys root@[slave主机名]:root/.ssh/
...
# 可以使用同步脚本对配置文件同步发放

# 验证
ssh root@[主机名]
# 第一次远程仍然需要输入密码

# （可做）
# ssh 远程登录一个节点后会自动生成 root/.ssh/known_hosts 文件，可以远程登录所有节点后将其分发到各节点
scp root/.ssh/known_hosts root@[slave主机名]:root/.ssh/
```


#### 6.安装 JDK

使用 Oracle 的 jdk，例如使用`jdk-8u181-linux-x64`版本。

- 首先查看各节点 linux 系统中是否已安装 jdk，如果安装了需要卸载。

```shell
# 查看系统已经装的jdk： 
rpm -qa|grep jdk
# 卸载jdk：
rpm -e --nodeps [openjdk文件名]
```

- 离线安装：将已下载好的 jdk 软件包解压到`/usr/java`，CDH 默认加载此路径。

```shell
# 创建 java目录
mkdir -p /usr/java

# 解压 jdk 安装包到 /usr/java 目录下，注意不能更换路径
tar -xvfz /path/to/jdk-8u<update_version>-linux-x64.tar.gz -C /usr/java/

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
# env 已设置软链接
export JAVA_HOME=/usr/java/current
export JRE_HOME=$JAVA_HOME/jre
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib

-------------------------------------------------

# env 未设置软链接
export JAVA_HOME=/usr/java/jdk1.8.0_181
export JRE_HOME=$JAVA_HOME/jre
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
```

- 生效环境变量

```shell
source /etc/profile
```

- 验证是否安装成功

```shell
which java
# 查看版本
java -verion
java
```

- 其他节点可以将配置同步过去即可 

```shell
scp /etc/profile [主机名]:/etc/
```


#### 7.安装 Mysql

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

- 解压缩安装包，部署Mysql
```shell
# 解压 tar 包到 /usr/local（软件目录），重命名为 mysql
# 在安装包位置处解压，也可使用绝对路径
tar -zxvf mysql-5.7.28-el7-x86_64.tar.gz -C /usr/local/
mv /usr/local/mysql-5.7.28-el7-x86_64/ /usr/local/mysql 
```

- 更改所属用户和用户组（需要先添加用户组和用户）
```shell
# 添加用户组 mysql 和用户 mysql
# 选择性可做（设置 mysql 用户禁止登陆系统）
groupadd mysql
useradd -g mysql -s /sbin/nologin mysql  ？？？
或
useradd -r -g mysql mysql    ？？？

# 创建数据存放目录 /usr/local/mysql/data 
mkdir /usr/local/mysql/data

# 更改目录及目录下文件的用户和用户组
chown -R mysql:mysql /usr/local/mysql/
chown -R mysql:mysql /usr/local/mysql/data
```



mkdir mysql/arch mysql/tmp



- 初始化MySQL

```shell
# 更改安装文件夹 mysql 的权限，进入 mysql 目录，并初始化 mysql
chmod -R 755 /usr/local/mysql/
cd /usr/local/mysql/
bin/mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data

# 注意会生成 root@localhost 登录 mysql 数据库的临时密码，密码是随机的（每个人生成的临时密码不一样）
# 需要记录一下
[Note] A temporary password is generated for root@localhost: o*s#gqh)F4Ck



```

- 设置变量
```shell
cat << EOF >> /etc/profile

# MySQL
export PATH=$PATH:/usr/local/mysql/bin
EOF

# 加载变量
source /etc/profile

# 软链接
ln -s /usr/local/mysql/lib/mysql /usr/lib/mysql
ln -s /usr/local/mysql/include/mysql /usr/include/mysql
```

- 设置开机启动
```shell
# 复制开机启动脚本到系统服务
cp /usr/local/mysql/support-files/mysql.server /etc/rc.d/init.d/mysqld
chown mysql:mysql /etc/rc.d/init.d/mysqld

# 修改默认的"basedir"与"datadir"
vim /etc/rc.d/init.d/mysqld
basedir=/usr/local/mysql
datadir=/usr/local/mysql/data

# 添加开机启动脚本
chkconfig --add mysqld
chkconfig --level 35 mysqld on
```

- 文件路径：log && pid && socket
```shell
# 日志路径
mkdir -p /var/log/mysqld
touch /var/log/mysqld/mysqld.log
chown -R mysql:mysql /var/log/mysqld/

# pid路径
mkdir -p /var/run/mysqld
chown -R mysql:mysql /var/run/mysqld/

# socker路径
mkdir -p /var/lib/mysqld
chown -R mysql:mysql /var/lib/mysqld/
ln -s /var/lib/mysqld/mysql.sock /tmp/mysql.sock
```

- 设置my.cnf文件
```shell
# 注意"log-error"，"pid-file"与"socket"的路径
mkdir -p /usr/local/mysql/etc
cat << EOF >> /usr/local/mysql/etc/my.cnf
[mysqld]
character-set-server=utf8
max_connections = 3000
log-error=/var/log/mysqld/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
socket=/var/lib/mysqld/mysql.sock
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysql]
default-character-set=utf8
EOF

# 软链接
ln -s /usr/local/mysql/etc/my.cnf /etc/my.cnf

# 赋权
chown -R mysql:mysql /usr/local/mysql/etc/

启动MySQL服务

# 启动服务
service mysqld start

# 验证
service mysqld status
```

- 设置MySQL账号密码与登陆权限
```shell
# 使用初始化密码登陆
mysql -uroot -p

# 修改密码，注意不能使用"$"等特殊符号
set password=password('cdh12#hadoop');
flush privileges;

# 远程登陆权限
grant all privileges on *.*  to  'root'@'%'  identified by 'cdh12#hadoop'  with grant option;
flush privileges;

# 查看账号
select user, host, authentication_string from mysql.user;
```


事先要创建 db 用户 >mysql
```
creat database cmf default character set utf;
GRANT ALL PRIVILEGES ON cmf.* TO 'cmf'@'%' IDENTIFIED BY 'ruozedata123';

creat database amon default character set utf;
GRANT ALL PRIVILEGES ON amon.* TO 'amon'@'%' IDENTIFIED BY 'ruozedata123';

flush privileges;
```


安装jdbc驱动
部署 mysql jdbc jar 包
```
mkdir -p /usr/share/java
cp mysql-connector-java-5.1.47.jar /usr/share/java/mysql-connector-java.jar
# 去除版本号
```

cmf
amon



### Cloudera Manager 安装

#### 1.部署 CM Server & Agent



在 master 节点向其余节点分发 CM 包`cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz`
```shell
for i in {1..3}; 
do scp /usr/local/src/cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz root@slave0$i:/usr/local/src/ ; 
done
```

在所有节点创建 CM 目录`/opt/cloudera-manager`，将 tar 包解压到此目录下。
```shell
mkdir /opt/cloudera-manager
tar -zxvf cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz -C /opt/cloudera-manager/
```

修改 agent 配置
在所有节点修改`/opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/config.ini`文件中的`server_host`参数为[master 节点主机名或 ip]（推荐主机名）。
```shell
vi /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/config.ini

# 修改
server_host=[主机名]

sed -i "s/server_host=localhost/server_host=master/g" /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/config.ini
```

修改 server 配置
在master节点修改`/opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-server/db.properties`
cmf





3.2 创建账号 && 权限
在所有节点创建 cloudera-scm 账号，这是 CM 相关服务使用的默认账号
```shell
# 禁止使用"cloudera-scm"账号登陆
useradd --system --home=/opt/cloudera-manager/cm-5.16.1/run/cloudera-scm-server/ --no-create-home --shell=/bin/false --comment "Cloudera SCM User" cloudera-scm

# 在所有节点为/opt/cloudera-manager目录赋权
chown -R cloudera-scm:cloudera-scm /opt/cloudera-manager
```

3.3 设置开机启动
在master节点设置系统服务
```shell
# 设置使用"cloudera-scm-server"为系统启动服务
cp /opt/cloudera-manager/cm-5.16.1/etc/init.d/cloudera-scm-server /etc/rc.d/init.d/
chown cloudera-scm:cloudera-scm /etc/rc.d/init.d/cloudera-scm-server

# 修改"CMF_DEFAULTS=${CMF_DEFAULTS:-/etc/default}"的路径
vim /etc/rc.d/init.d/cloudera-scm-server
CMF_DEFAULTS=/opt/cloudera-manager/cm-5.16.1/etc/default


# 添加系统启动服务
chkconfig --add cloudera-scm-server
chkconfig --level 35 cloudera-scm-server on
checkconfig --list
在所有slave节点设置系统服务

# 设置使用"cloudera-scm-agent"为系统启动服务
cp /opt/cloudera-manager/cm-5.16.1/etc/init.d/cloudera-scm-agent /etc/rc.d/init.d/
chown cloudera-scm:cloudera-scm /etc/rc.d/init.d/cloudera-scm-agent

# 修改"CMF_DEFAULTS=${CMF_DEFAULTS:-/etc/default}"的路径"-/etc/default"
vim /etc/rc.d/init.d/cloudera-scm-agent
CMF_DEFAULTS=${CMF_DEFAULTS:/opt/cloudera-manager/cm-5.16.1/etc/default}

# 添加系统启动服务
chkconfig --add cloudera-scm-agent
chkconfig --level 35 cloudera-scm-agent on
checkconfig --list
```









3.4 初始化数据库
在所有节点设置MySQL驱动(JDBC)；
注意：部署JDBC在任意节点，则后续"CDH安装配置"阶段Reports Manager被分配在任意节点都可以
```shell
cp /usr/local/src/mysql-connector-java-8.0.13.jar /opt/cloudera-manager/cm-5.16.1/share/cmf/lib/
chown cloudera-scm:cloudera-scm /opt/cloudera-manager/cm-5.16.1/share/cmf/lib/mysql-connector-java-8.0.13.jar
在master节点重启MySQL服务

service mysqld restart
在任意节点初始化CM
注意：Cloudera服务需要的相关database如下：
表中给出的是CM相关服务配置文件中默认的database与user，但不是必须使用；
database在数据库中可直接创建，但CM初始化时如果没有database，则自动创建。
Service	Database	User
Cloudera Manager Server	scm	scm
Activity Monitor	amon	amon
Reports Manager	rman	rman
Hue	hue	hue
Hive Metastore Server	metastore	metastore
Sentry Server	sentry	sentry
Cloudera Navigator Audit Server	nav	nav
Cloudera Navigator Metadata Server	navms	navms
Oozie	oozie	oozie
# 格式：scm_prepare_database.sh [options] (postgresql|mysql|Oracle) database username [password]
# scm_prepare_database.sh：创建与配置CMS需要的数据库脚本，默认在"/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/"目录；
# postgresql|mysql|oracle：必选项，数据库类型；
# database：必选项，针对postgresql|mysql，创建SCM数据库;针对oracle，填写sid；
# username：必选项，SCM数据库的账号；
# password：选填项，SCM数据库的账号密码，如果不指定，会提示输入；
# options：
# -h：数据库主机ip或hostname，默认是"localhost"；
# -u：数据库账号，需要具备增删改查的权限，默认是"root"；
# -p：账号密码，默认无密码；
# --scm-host：SCM server主机名，默认是"localhost"
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % scm scm scm_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % amon amon amon_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % rman rman rman_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % hue hue hue_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % metastore metastore metastore_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % sentry sentry sentry_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % nav nav nav_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % navms navms navms_pass
/opt/cloudera-manager/cm-5.16.1/share/cmf/schema/scm_prepare_database.sh mysql -h master -uroot -pcdh12#hadoop --scm-host % oozie oozie oozie_pass
返回如下信息，表示配置成功

[main] INFO  com.cloudera.enterprise.dbutil.DbCommandExecutor  - Successfully connected to database.
All done, your SCM database is configured correctly!
```



3.5 创建本地parcel源
在master节点制作本地parcel源

```shell
# 创建本地parcel源目录
mkdir -p /opt/cloudera/parcel-repo

# 将parcel相关安装包放置到"/opt/cloudera/parcel-repo"目录；
# 说明："/opt/cloudera/parcel-repo"目录可放置多套parcel安装包；
# 将"CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1"重命名为"CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha"，否则会重新下载"CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel"安装包
mv /usr/local/src/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel /opt/cloudera/parcel-repo/
mv /usr/local/src/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 /opt/cloudera/parcel-repo/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
mv /usr/local/src/manifest.json /opt/cloudera/parcel-repo/

# 赋权
chown -R cloudera-scm:cloudera-scm /opt/cloudera/
在所有salve节点创建软件安装目录

mkdir -p /opt/cloudera/parcels

# 赋权
chown -R cloudera-scm:cloudera-scm /opt/cloudera/
```





3.6 启动CM服务
在master节点启动cloudera-scm-server服务

```shell
# "cloudera-scm-server"启动需要连接数据库，监听端口启动会延迟
service cloudera-scm-server restart
service cloudera-scm-server status -l

# 通过启动后的状态查看，脚本需要执行"pstree"命令，需要安装依赖包
yum install psmisc -y
在所有salve节点启动cloudera-scm-agent服务

yum install psmisc -y
service cloudera-scm-agent restart
service cloudera-scm-agent status -l
```


