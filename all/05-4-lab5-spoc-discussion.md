# lab5 spoc 思考题

- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。


## 个人思考题

### 总体介绍

 - 第一个用户进程创建有什么特殊的？
 - 系统调用的参数传递过程？
 - getpid的返回值放在什么地方了？

### 进程的内存布局

 - 尝试在进程运行过程中获取内核堆栈和用户堆栈的调用栈？
 - 尝试在进程运行过程中获取内核空间中各进程相同的页表项（代码段）和不同的页表项（内核堆栈）？

### 执行ELF格式的二进制代码-do_execve的实现

 - 在do_execve中进程清空父进程时，当前进程是哪一个？在什么时候开始使用新加载进程的地址空间？
 - 新加载进程的第一级页表的建立代码在哪？

### 执行ELF格式的二进制代码-load_icode的实现

 - 第一个内核线程和第一个用户进程的创建有什么不同？
 - 尝试跟踪分析新创建的用户进程的开始执行过程？

### 进程复制

 - 为什么新进程的内核堆栈可以先于进程地址空间复制进行创建？
 - 进程复制的代码在哪？复制了哪些内容？
 - 进程复制过程中有哪些修改？为什么要修改？

### 内存管理的copy-on-write机制
 - 什么是写时复制？
 - 写时复制的页表在什么时候进行复制？共享地址空间和写时复制有什么不同？

## 小组练习与思考题

### (1)(spoc) 在真实机器的u盘上启动并运行ucore lab,

请准备一个空闲u盘，然后请参考如下网址完成练习

https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-boot-with-grub2-in-udisk.md

> 注意，grub_kernel的源码在ucore_lab的lab1_X的git branch上，位于 `ucore_lab/labcodes_answer/lab1_result`

(报告可课后完成)请理解grub multiboot spec的含义，并分析ucore_lab是如何实现符合grub multiboot spec的，并形成spoc练习报告。

```
当引导程序调用32位操作系统时，机器状态必须如下：

EAX 
必须包含魔数0x2BADB002；这个值指出操作系统是被一个符合Multiboot规范的引导程序载入的（这样就算是另一种引导程序也可以引导这个操作系统）。

EBX 
必须包含由引导程序提供的Multiboot信息结构的物理地址（参见引导信息格式）。

CS 
必须是一个偏移量位于0到0xFFFFFFFF之间的32位可读/可执行代码段。这里的精确值未定义。

DS 
ES 
FS 
GS 
SS 
必须是一个偏移量位于0到0xFFFFFFFF之间的32位可读/可执行代码段。这里的精确值未定义。

A20 gate
必须已经开启。

CR0 
第31位（PG）必须为0。第0位（PE）必须为1。其他位未定义。

EFLAGS 
第17位（VM）必须为0。第9位（IF）必须为1 。其他位未定义。
所有其他的处理器寄存器和标志位未定义。这包括：

ESP 
当需要使用堆栈时，OS映象必须自己创建一个。

GDTR 
尽管段寄存器像上面那样定义了，GDTR也可能是无效的，所以OS映象决不能载入任何段寄存器（即使是载入相同的值也不行！）直到它设定了自己的GDT。

IDTR 
OS映象必须在设置完它的IDT之后才能开中断。
尽管如此，其他的机器状态应该被引导程序留做正常的工作顺序，也就是同BIOS（或者DOS，如果引导程序是从那里启动的话）初始化的状态一样。换句话说，操作系统应该能够在载入后进行BIOS调用，直到它自己重写BIOS数据结构之前。还有，引导程序必须将PIC设定为正常的BIOS/DOS 状态，尽管它们有可能在进入32位模式时改变它们。

当lab1中的bootloader转换到了保护模式之后，机器状态即符合上述multiboot的要求。

```

### (2)(spoc) 理解用户进程的生命周期。

> 需写练习报告和简单编码，完成后放到git server 对应的git repo中

### 练习用的[lab5 spoc exercise project source code](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab5/lab5-spoc-discuss)


#### 掌握知识点
1. 用户进程的启动、运行、就绪、等待、退出
2. 用户进程的管理与简单调度
3. 用户进程的上下文切换过程
4. 用户进程的特权级切换过程
5. 用户进程的创建过程并完成资源占用
6. 用户进程的退出过程并完成资源回收

> 注意，请关注：内核如何创建用户进程的？用户进程是如何在用户态开始执行的？用户态的堆栈是保存在哪里的？

```
创建用户进程： initmain -> usermain -> KERNEL_EXECVE
设置用户态： load_icode中设置了用户的代码段和数据段
用户态堆栈： USTACKTOP
```

阅读代码，在现有基础上再增加一个用户进程A，并通过增加cprintf函数到ucore代码中，
能够把个人思考题和上述知识点中的内容展示出来：即在ucore运行过程中通过`cprintf`函数来完整地展现出来进程A相关的动态执行和内部数据/状态变化的细节。(约全面细致约好)

> 见[这里](https://github.com/williamljb/ucore_lab/tree/master/related_info/lab5/lab5-spoc-discuss)

请完成如下练习，完成代码填写，并形成spoc练习报告
