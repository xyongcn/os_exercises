# lab8 文件系统 (lec 22) spoc 思考题


- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。

## 个人思考题

### 总体介绍
 1. 文件系统中的文件、目录、索引节点和安装点这几种数据结构分别支持些什么操作？
 2. 请简要描述ucore文件系统支持的文件系统抽象

 > 文件、目录、索引节点和安装点

### ucore 文件系统架构

 1. 请简要阐述ucore 文件系统架构的四个组成部分

 > 系统调用接口、VFS、SFS和I/O接口

 2. 请简要说明进程proc_struct、文件file、inode之间的关系。 
 
 3. ucore中的进程打开文件表和系统打开文件表对应到具体的哪个数据结构上？

### Simple File System分析

 1. SFS在硬盘上的四大部分主要是什么，有何作用？
 
 > superblock, root-dir inode, freeman, data block

 2. 硬盘上的SFS是如何加载到ucore中并初始化的？
 3. 硬盘上的inode和内存中的inode的关系和区别是什么?
 4. 描述file, dir, inode在内存和磁盘上的格式和相关操作。

### Virtual File System分析

 1. file数据结构的主要内容是什么？与进程的关系是什么？
 2. inode数据结构的主要内容是什么？与file的数据结构的关系是什么？
 3. inode_ops包含哪些与文件相关的操作？
 4. VFS是如何把键盘、显示输出和磁盘文件统一到一个系统调用访问框架下的？ 

### I/O 设备接口分析

 1. device数据结构的主要内容是什么？与fs的关系是什么？与inode的关系是什么？
 2. 比较ucore中I/O接口、SFS文件系统接口和文件系统的系统调用接口的操作函数有什么异同？
 
## 小组思考题

1. (spoc) 理解文件访问的执行过程，即在ucore运行过程中通过`cprintf`函数来完整地展现出来读一个文件在ucore中的整个执行过程，(越全面细致越好)
完成代码填写，并形成spoc练习报告，需写练习报告和简单编码，完成后放到git server 对应的git repo中

打开文件为一个系统调用，通过中断调用sysfile_open，然后新建一个文件句柄，并调用vfs_open来打开文件。vfs则调用sfs来具体打开一个文件。
sfs首先要查找路径，找到对应的inode。找到之后返回就可以新建出一个vfs的inode了。之后对文件进行读入的话就可以直接通过inode执行了。

输出如下：
```
syscall!!!
sysfile_open!!!
file_open!!!
fd_array_alloc!!!
vfs_open!!!
sfs_lookup!!!
sfs_lookup_once!!!
sfs_dirent_search_nolock!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
sfs_rbuf!!!
ide_read_secs!!!
```
可以看到从syscall 到 ide_read读扇区的输出信息。

代码在[这里](https://github.com/williamljb/ucore_lab/tree/master/labcodes_answer/lab8_result)

2. （spoc） 在下面的实验代码的基础上，实现基于文件系统的pipe IPC机制

### 练习用的[lab8 spoc exercise project source code](https://github.com/chyyuu/ucore_lab/tree/master/labcodes_answer/lab8_result)
