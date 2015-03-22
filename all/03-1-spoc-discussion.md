# lec5 SPOC思考题


NOTICE
- 有"w3l1"标记的题是助教要提交到学堂在线上的。
- 有"w3l1"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 个人思考题
---

请简要分析最优匹配，最差匹配，最先匹配，buddy systemm分配算法的优势和劣势，并尝试提出一种更有效的连续内存分配算法 (w3l1)
```
  + 采分点：说明四种算法的优点和缺点
  - 答案没有涉及如下3点；（0分）
  - 正确描述了二种分配算法的优势和劣势（1分）
  - 正确描述了四种分配算法的优势和劣势（2分）
  - 除上述两点外，进一步描述了一种更有效的分配算法（3分）
 ```
- [x]  

```
最优匹配优势：充分利用小碎片
最优匹配劣势：小碎片会非常多，合并麻烦
最差匹配优势：碎片数量少
最差匹配劣势：难以分配大块内存，合并麻烦
最先匹配优势：速度快，容易分配大块内存
最先匹配劣势：碎片多，查找开销大
buddysystem优势：速度快，容易管理
buddysystem劣势：产生内碎片
新内存分配算法：维护一个块状链表，每次申请分配一段连续的链表。这样平衡了申请和释放的时间复杂度。
 ```

## 小组思考题

请参考ucore lab2代码，采用`struct pmm_manager` 根据你的`学号 mod 4`的结果值，选择四种（0:最优匹配，1:最差匹配，2:最先匹配，3:buddy systemm）分配算法中的一种或多种，在应用程序层面(可以 用python,ruby,C++，C，LISP等高语言)来实现，给出你的设思路，并给出测试用例。 (spoc)

```
#define FREE 0
#define USED 1
#define FULL 2
struct Node
{
    int status, free_pages, length;
    Page *base;
    Node *left, right;
} *root;

void buddy_init_memmap(Page *base, int n)
{
    assert(n > 0);
    struct Page *p = base;
    for (; p != base + n; p ++) {
        assert(PageReserved(p));
        p->flags = p->property = 0;
        set_page_ref(p, 0);
    }
    base->property = n;
    SetPageProperty(base);
    root = new Node();
    root->base = base;
    root->status = FREE;
    root->free_pages = n;
    root->length = n;
    root->base->property = n;
}

static struct Page *
alloc_pages(struct Node *root, size_t n) {
    if (n > root->free_pages) {
        return NULL;
    }
    if (root->status == FREE)
    {
        if (root->free_pages >= n*2)
        {
            if (root->left == NULL) root->left = new Node();
            root->left->base = root->base;
            root->left->status = FREE;
            root->left->free_page = root->free_pages/2;
            root->left->length = root->length/2;
            root->left->base->property = root->left->length;

            if (root->right == NULL) root->right = new Node();
            root->right->base = root->base+root->length/2;
            root->right->status = FREE;
            root->right->free_page = root->free_pages/2;
            root->right->length = root->length/2;
            root->right->base->property = root->rigth->length;

            Page *ans = alloc_pages(root->left, n);
            root->free_pages = root->left->freepages + root->right->freepages;
            root->status = USED;
            return ans;
        }
        root->status = FULL;
        root->free_pages = 0;
        return root->base;
    }
    Page *ans = alloc_pages(root->left, n);
    if (ans == NULL)
        ans = alloc_pages(root->right, n);
    root->free_pages = root->left->freepages + root->right->freepages;
    return ans;
}

static struct Page *
buddy_alloc_pages(size_t n) {
    assert(n > 0);
    return alloc_page(root, n);
}

void free_pages(struct Node *root, struct Page *base)
{
    if (root->base == base)
    {
        if (root->length == base->property)
        {
            root->free_pages = root->length;
            root->status = FREE;
            return;
        }
        free_pages(root->left, base);
        root->free_pages = root->left->free_pages + root->right->free_pages;
        if (root->free_pages == root->length)
        {
            root->status = FREE;
            root->base->property = root->length;
        }
        else
            root->status = USED;
        return;
    }
    if (root->base > base)
        return;
    free_pages(root->left, base);
    free_pages(root->right, base);
    root->free_pages = root->left->free_pages + root->right->free_pages;
    if (root->free_pages == root->length)
    {
        root->status = FREE;
        root->base->property = root->length;
    }
    else
        root->status = USED;
}

static void
buddy_free_pages(struct Page *base, size_t n) {
    assert(n > 0);
    struct Page *p = base;
    for (; p != base + n; p ++) {
        assert(!PageReserved(p) && !PageProperty(p));
        p->flags = 0;
        set_page_ref(p, 0);
    }
    free_pages(root, base);
}

static size_t
buddy_nr_free_pages(void) {
    return root->free_pages;
}

const struct pmm_manager buddy_pmm_manager = {
    .name = "buddy_pmm_manager",
    .init = default_init,
    .init_memmap = buddy_init_memmap,
    .alloc_pages = buddy_alloc_pages,
    .free_pages = buddy_free_pages,
    .nr_free_pages = buddy_nr_free_pages,
    .check = default_check,
};

 ```
=======
如何表示空闲块？ 如何表示空闲块列表？ 
[(start0, size0),(start1,size1)...]
在一次malloc后，如果根据某种顺序查找符合malloc要求的空闲块？如何把一个空闲块改变成另外一个空闲块，或消除这个空闲块？如何更新空闲块列表？
在一次free后，如何把已使用块转变成空闲块，并按照某种顺序（起始地址，块大小）插入到空闲块列表中？考虑需要合并相邻空闲块，形成更大的空闲块？
如果考虑地址对齐（比如按照4字节对齐），应该如何设计？
如果考虑空闲/使用块列表组织中有部分元数据，比如表示链接信息，如何给malloc返回有效可用的空闲块地址而不破坏
元数据信息？
伙伴分配器的一个极简实现
http://coolshell.cn/tag/buddy
```

--- 

## 扩展思考题

阅读[slab分配算法](http://en.wikipedia.org/wiki/Slab_allocation)，尝试在应用程序中实现slab分配算法，给出设计方案和测试用例。

## “连续内存分配”与视频相关的课堂练习

### 5.1 计算机体系结构和内存层次
MMU的工作机理？

- [x]  

>  http://en.wikipedia.org/wiki/Memory_management_unit

L1和L2高速缓存有什么区别？

- [x]  

>  http://superuser.com/questions/196143/where-exactly-l1-l2-and-l3-caches-located-in-computer
>  Where exactly L1, L2 and L3 Caches located in computer?

>  http://en.wikipedia.org/wiki/CPU_cache
>  CPU cache

### 5.2 地址空间和地址生成
编译、链接和加载的过程了解？

- [x]  

>  

动态链接如何使用？

- [x]  

>  


### 5.3 连续内存分配
什么是内碎片、外碎片？

- [x]  

>  

为什么最先匹配会越用越慢？

- [x]  

>  

为什么最差匹配会的外碎片少？

- [x]  

>  

在几种算法中分区释放后的合并处理如何做？

- [x]  

>  

### 5.4 碎片整理
一个处于等待状态的进程被对换到外存（对换等待状态）后，等待事件出现了。操作系统需要如何响应？

- [x]  

>  

### 5.5 伙伴系统
伙伴系统的空闲块如何组织？

- [x]  

>  

伙伴系统的内存分配流程？

- [x]  

>  

伙伴系统的内存回收流程？

- [x]  

>  

struct list_entry是如何把数据元素组织成链表的？

- [x]  

>  



