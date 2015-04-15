# lab4 spoc 思考题

- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。

## 个人思考题

### 总体介绍

(1) ucore的线程控制块数据结构是什么？

### 关键数据结构

(2) 如何知道ucore的两个线程同在一个进程？

(3) context和trapframe分别在什么时候用到？

(4) 用户态或内核态下的中断处理有什么区别？在trapframe中有什么体现？

### 执行流程

(5) do_fork中的内核线程执行的第一条指令是什么？它是如何过渡到内核线程对应的函数的？
```
tf.tf_eip = (uint32_t) kernel_thread_entry;
/kern-ucore/arch/i386/init/entry.S
/kern/process/entry.S
```

(6)内核线程的堆栈初始化在哪？
```
tf和context中的esp
```

(7)fork()父子进程的返回值是不同的。这在源代码中的体现中哪？

(8)内核线程initproc的第一次执行流程是什么样的？能跟踪出来吗？

## 小组练习与思考题

(1)(spoc) 理解内核线程的生命周期。

> 需写练习报告和简单编码，完成后放到git server 对应的git repo中

### 掌握知识点
1. 内核线程的启动、运行、就绪、等待、退出
2. 内核线程的管理与简单调度
3. 内核线程的切换过程

### 练习用的[lab4 spoc exercise project source code](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab4/lab4-spoc-discuss)


请完成如下练习，完成代码填写，并形成spoc练习报告

### 1. 分析并描述创建分配进程的过程

> 注意 state、pid、cr3，context，trapframe的含义
> 调用alloc_proc创建进程：

```
        memset(proc, 0, sizeof(struct proc_struct));	//初始化
        cprinf("process generated with UNINIT!\n");
        proc->state = PROC_UNINIT;						//设置初始状态
        proc->pid = -1;									//初始pid
        proc->cr3 = boot_cr3;							//初始页表基址
```

### 练习2：分析并描述新创建的内核线程是如何分配资源的

> 注意 理解对kstack, trapframe, context等的初始化
> 调用kernel_thread来fork并执行：

```
    struct trapframe tf;
    memset(&tf, 0, sizeof(struct trapframe));			//初始化
    tf.tf_cs = KERNEL_CS;								//设置段
    tf.tf_ds = tf.tf_es = tf.tf_ss = KERNEL_DS;
    tf.tf_regs.reg_ebx = (uint32_t)fn;					//设置线程起始地址
    tf.tf_regs.reg_edx = (uint32_t)arg;					//名字
    tf.tf_eip = (uint32_t)kernel_thread_entry;			//设置返回地址
    return do_fork(clone_flags | CLONE_VM, 0, &tf);		//fork
```
> fork时：

```
    //    分配TCB
    proc = alloc_proc();
    proc->pid = get_pid();
    //    分配内核栈
    setup_kstack(proc);
    //    初始化tf和上下文
    copy_thread(proc, stack, tf);
    //    更新链表
    list_add_before(&proc_list, &proc->list_link);
    //    唤醒线程
    wakeup_proc(proc);
    //    设置返回值
    nr_process++;
    ret = proc->pid;
	//    设置父线程
	proc->parent=current;
```

当前进程中唯一，操作系统的整个生命周期不唯一，在get_pid中会循环使用pid，耗尽会等待

### 练习3：阅读代码，在现有基础上再增加一个内核线程，并通过增加cprintf函数到ucore代码中
能够把进程的生命周期和调度动态执行过程完整地展现出来
> 见[这里](https://github.com/williamljb/ucore_lab/tree/master/related_info/lab4/lab4-spoc-discuss)

### 练习4 （非必须，有空就做）：增加可以睡眠的内核线程，睡眠的条件和唤醒的条件可自行设计，并给出测试用例，并在spoc练习报告中给出设计实现说明

### 扩展练习1: 进一步裁剪本练习中的代码，比如去掉页表的管理，只保留段机制，中断，内核线程切换，print功能。看看代码规模会小到什么程度。


