![[0381c2be01a4233d1b0f2e3ef5c2677f_MD5.gif]]

是不是总觉得AI写代码像抽盲盒？生成一团乱麻就甩锅"模型不够顶"？

爆火的VibeCoding让人人都能化身程序员，但代码生成质量也让用户槽点不少。

我的同事Booker最近摸索出了一套让VibeCoding更准确的操作指南——**Kiro Spec工作流（由AWS开发）可以集成到任何AI开发工具中，例如Claude Code或Cursor。即使使用Claude 3这样的模型，也能通过requirements.md、design.md和tasks.md这三个文件，将随机的氛围编程（vibe coding）转化为结构化的工程化流程。**

👇看看他的实操👇

我最近研究 Kiro 的推文又爆了

![[d7effc6087b14124e086679cab516aff_MD5.webp]]

再加上最近经常听到朋友们吐槽：**AI IDE 里的大模型选择有时会受限，担心开发效率会不会大打折扣**。我实践之后发现，只要方法用对了——比如 Kiro Spec 工作流——**即使没有高级大模型，依然能让开发体验和产出大幅提升**。

于是这次特地整理成一篇系统的文章，详细分享我的实操经验和方法论。无论你用的是 Cursor、Claude Code 还是其他 AI IDE，都可以参考这套方案。

//拉霸式 vibe coding，真的靠谱吗？

你是否有过这样的体验：在 AI IDE 里输入一句模糊的需求，点击“生成”，满怀期待地等着 AI 给你一个完美的程序？结果却像在拉霸机前拉动拉杆——有时中个小奖，大多数时候却一无所获。

最近X上面流行这么一张图，非常形象：

![[20be871217d93d4924e7e39a18203bd3_MD5.webp]]

> 拉霸游戏和 vibe coding 的异同：
> 
> 拉霸游戏：买代币，拉拉杆，偶尔中大奖，更多时候是“再来一次”，最终庄家总是赢家。
> 
> 氛围编程（vibe coding）：买 Tokens，写模糊提示，点“生成”，有时得完美代码，有时一团乱麻。AI 鼓励你“再试一次”，你安慰自己“这次一定能修好 bug”，但最终模型厂商总是赢家。偶尔你觉得自己赚到了，回头却发现花了更多时间。

Vibe coding 最大的问题是：**它让开发变成了“碰运气”，而不是“可控的工程”。**

### 常见的 vibe coding 流程示意图

![[3a0a0558eeca503a029eb0f9ce9d2691_MD5.webp]]

> 黄色节点为“人”操作，蓝色为 AI 产出，红色为不理想结果。

## //有没有更好的办法？——传统研发流程是怎么做的

## 传统软件工程强调需求澄清、技术设计、任务拆分、过程可追溯。这样做虽然“慢”，但能让项目稳步推进、可复盘、可协作。每一步都有人参与评审，确保方向和细节都不会跑偏。

Kiro AI IDE 就把这种流程做成了**“Spec 工作流”**，让 AI 编程也能像工程师一样靠谱。

### 传统研发流程示意图

![[2e81a567e7367f1537a7db65850cf76b_MD5.webp]]

> 该流程强调需求评审和迭代反馈，体现传统软件工程的闭环和持续优化。

## //Kiro 的 Spec 工作流有多香？

## Kiro 是 AWS 推出的 AI IDE，除了免费集成 Claude 4，更大的亮点是它的 Spec 工作流：

Your browser does not support video tags

一个 Spec 可以说是一个规格/规范，如果用过BDD (行为驱动开发) 可能就会比较熟悉这个名词。

Spec 是用来解决如何把模糊的想法转化为详细的实施计划、跟踪和验收标准的问题。

-   每个 Spec 都是一个文件夹，下有 3 个核心文件：
    

1.  `requirements.md` —— **需求文档**（用 EARS 语法写用户故事和验收标准）
    
2.  `design.md` —— **技术方案**（架构、流程、注意事项）
    
3.  `tasks.md` —— **任务清单**（todolist，便于跟踪）
    

感觉有没有很熟悉？其实这和很多大厂的研发流程、敏捷开发的拆解方式如出一辙，但 Kiro 把它和 AI IDE 深度结合，极大提升了落地效率。

### 什么是 EARS 需求语法？

EARS（简易需求语法）最早用于喷气发动机控制系统，后来被软件工程广泛采用。它用简单句式约束需求，避免“模糊表达”，让需求更清晰、可落地。

参考资料：EARS 语法指南<sup><span leaf=""><span textstyle="">[1]</span></span></sup>

我还整理了一个速查表，可以快速理解一下：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 例：When 用户点击“静音”，系统应当抑制所有音频输出。

例如一个完整的例子：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## //Claude Code/Cursor 也能复刻这套 Spec  

## 即使没有 Kiro，其他 AI IDE 也能复刻这套流程。以 Claude Code 为例，整个过程可以非常丝滑：

1.  **在项目下建立 CLAUDE.md**
    

-   你可以把下面的提示词模板直接写进 CLAUDE.md，作为 AI 协作的“工作说明书”。
    
-   最新版本的提示词可以在这个 Github 链接<sup><span leaf="">[2]</span></sup> 获取。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**2\. 启动 Claude Code，输入原始需求**

-   直接把你的想法、用户故事写进对话框。
    
-   Claude 会自动读取 CLAUDE.md，开始和你进行需求澄清和确认。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**3\. 需求确认后，Claude 输出 requirements.md**

-   Claude 会用 EARS 语法梳理需求，生成标准的 requirements.md。
    
-   你可以随时补充、修改，Claude 会持续和你对齐。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**4\. 技术方案设计**

-   需求确认后，Claude 会自动进入 design.md 阶段，输出详细的技术方案。
    
-   包括架构、技术选型、接口、测试策略等。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**5\. 任务拆分**

-   Claude 会根据 design.md 自动生成 tasks.md，把方案拆分为可执行的 todolist。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**6\. 逐步实现与验收**

-   Claude 会按照 tasks.md 协助你逐步实现代码、测试，并输出所有过程产物到 output/ 目录。
    
-   你只需参与需求、设计、验收等关键评审环节。
    

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

整个流程下来，你会发现，AI 不再是“黑箱”式地帮你生成代码，而是和你像搭档一样，**步步确认、逐步推进**。

这样，哪怕没有 Kiro，借助 Claude Code 也能轻松复刻 Spec 工作流，让 AI 编程变得高效、可控、可复盘。

其他的 AI IDE 也是可以类似如此操作，例如 Cursor 的 `.cursor/rules/project.mdc`、Augment 的 `.augment-guidelines` 文件等。

如果你嫌麻烦，想要更**开箱即用**的体验，可以试试 CloudBase AI ToolKit<sup><span leaf="">[3]</span></sup>，直接内置了这套工作流：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

-   支持多种 AI IDE，提供 MCP + AI rules
    
-   Rules 自带这套 Kiro 类似的 Spec 工作流
    
-   一键生成、部署、托管全栈web和小程序前后端应用，无需运维  
    
    👇以下工具均支持 CloudBase AI ToolKit👇
    

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

## //人机协作，才是正解

## 在 Spec 工作流下，AI 负责：

-   模糊需求 → 需求方案
    
-   技术设计文档
    
-   任务清单
    
-   编码实现
    
-   验收测试
    

人只需参与：

-   需求输入
    
-   需求/技术/任务/测试评审
    

### Vibe coding 与 Spec 工作流对比流程图

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 黄色节点为“人”参与评审，蓝色为 AI 产出，红色为不理想结果，绿色为高质量结果，灰色为流程分组。

这样既能发挥 AI 的高效，又能保证工程质量。你会发现，AI 不是替代人，而是让人更专注于决策和把控方向，把繁琐的细节交给 AI。

//总结：让 AI 编程更快、更稳、更靠谱

Spec 工作流让 AI 编程不再是“碰运气”，而是“有章可循”。人类工程师的经验和判断，配合 AI 的高效执行，才能让开发真正提速、提质、可复盘。

> 记住：AI 不是替代人，而是让人更强大。

最后放一个🥚彩蛋：

这篇文章也是我使用这套工作流，和我的 AI 搭档一起协作完成的。留下的不只是文章的草稿、终稿，还有我和 AI 一起结对编程的思考过程。

结果固然重要，过程的价值也不容忽视

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

参考资料

\[1\] EARS 语法指南: _https://alistairmavin.com/ears/_  

\[2\] Github 链接: 

_https://github.com/TencentCloudBase/CloudBase-AI-ToolKit/blob/main/config/.cursor/rules/cloudbase-rules.mdc#L21C1-L59C12_  

\[3\] CloudBase AI ToolKit: 

_https://github.com/TencentCloudBase/CloudBase-AI-ToolKit/_

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**—END—**

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

-   [五千字深度长文：详解科技圈爆火的MCP](https://mp.weixin.qq.com/s?__biz=MzA5NzU3MDczNA==&mid=2247489006&idx=1&sn=dde509cfb197dd3bf95a3982ce1f39c6&scene=21#wechat_redirect)  
    

-   [腾讯云两项网络技术成果入选国际顶会SIGCOMM](https://mp.weixin.qq.com/s?__biz=MzA5NzU3MDczNA==&mid=2247489066&idx=1&sn=b4ff90e0ec3cbc39713021560d091a2c&scene=21#wechat_redirect)
    

-   [DeepSeek致谢腾讯大模型网络提速技术方案贡献](https://mp.weixin.qq.com/s?__biz=MzA5NzU3MDczNA==&mid=2247489049&idx=1&sn=fee05fb189ebdc8a8d78e589e30bb2fb&scene=21#wechat_redirect)  
    

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)