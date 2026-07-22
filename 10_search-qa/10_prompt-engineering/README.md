# Prompt工程

GPT 内部已经蕴含了巨大的智力能量，只是还不知道如何组织使用，需要我们将其进一步引导出来。这是软件交互的革命，有了这样的交互，现在的软件这种让你不停的点点点、看看看、退退退的交互都土掉渣了。Prompt 工程就是指导如何构造输入，以引导模型得到期望的输出。构造或选择输入到模型的 Prompt 以获得最佳结果，Prompt 的形式、长度、详细程度等都可能影响模型的响应。这个技术的目的是通过巧妙构 prompt 提示语来影响模型的行为，使其在特定任务上表现出色。

Prompt 工程将特定领域的知识作为输入消息提供给模型。类似于短期记忆，容量有限但是清晰。举个例子给 ChatGPT 发送请求，将特定的知识放在请求中，让 ChatGPT 对消息中蕴含的知识进行分析，并返回处理结果。

- 优势：正确性和精度高。
- 劣势：一次可以处理的文本量有限制，如果知识库较大，无论从可行性还是效率而言都是不合适的。[Chatgpt 的限制](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb?spm=wolai.workspace.0.0.357e11a2XSQ9wO&file=Question_answering_using_embeddings.ipynb)如下表所示：

| **Model**         | **Maximum text length** |
| ----------------- | ----------------------- |
| **gpt-3.5-turbo** | 4,096(~5 pages)         |
| **gpt-4**         | 8,192(~10 pages)        |
| **gpt-4-32k**     | 32,768(~40 pages)       |

## 基础

### Prompt构成

- 指令：希望 LLM 执行什么任务 
- 上下文：给LLM提供一些额外的信息，比如可以是垂直领域信息，从而引导LLM给出更好的回答
- 输入数据（问题）：希望从LLM得到什么内容的回答
- 输出要求（如格式）：引导LLM给出指定格式的输出

### temperature

也就是按照一定的概率回答问题

```python
response = get_completion(prompt, temperature=0.7) 
```

## 原则

### 指令

#### 简洁

尽量保持问题简洁明了，以避免引起歧义或误导。

#### 明确

确保指令明确，有助于 AI 更准确地理解您的需求。尽可能的将想要得到的结果和需求清楚的告诉 model，可以有效的减少得到不相关或者不正确的模型反应。但是清晰且具体。

### 输入

#### 使用完整句子

使用完整句子和清晰的语法结构可以提高 AI 理解问题的准确性。

#### 结构化输入

##### 使用delimiter

比如在输入多行提示时，每行提示都使用固定的格式，创建一个符号来表示特写的规则。

```prompt
"""我们来玩一个名为 gkzw 的写作游戏，每当我说 gkzw，你开始写作，规则如下：

1. 字数不少于 200 字。
2. 文中必须出现 "小明"。

明白了吗？"""
```

```python
prompt = f""" Summarize the text delimited by triple backticks \
into a single sentence. ```{text}``` """
```

#### 限制条件

如果您需要特定类型的答案，可以在 prompt 中明确指出。例如，如果您需要一个简短的答案，可以在问题中加入“简短地回答”。

比如可以强硬要求 GPT 在不知道的时候直接回答不知道（当然这通过修改调用方式来完成更好）。也可以就输出答案的长度、语言等条件进行约束。或在使用语言模型时，针对模型输出不希望的结果而设置的一种文本输入方式。通过使用负向提示，可以帮助模型避免输出不良、不准确或不恰当的文本。

```prompt
我们能玩一个名为 kfc 的谜语创作游戏，当我说 "kfc"，你写一个谜题，要求：

1. 不少于 200 字
2. 谜题不能出现肯德基、星期四、KFC
3. 正文可以夹杂小语种语言，如 """他说：Ciao"""
4. 谜底必须是  原来今天是肯德基疯狂星期四！！
```



```python
prompt = f""" You will be provided with text delimited by triple quotes.  If it contains a sequence of instructions, \  re-write those instructions in the following format:  Step 1 - ... Step 2 - … … Step N - …  If the text does not contain a sequence of instructions, \  then simply write \"No steps provided.\"  \"\"\"{text_1}\"\"\" """
```

#### 提供示例

```python
prompt = f"""
您的任务是以一致的风格回答问题。

<孩子>: 请教我何为耐心。
<祖父>: 挖出最深峡谷的河流源于一处不起眼的泉眼；最宏伟的交响乐从单一的音符开始；最复杂的挂毯以一根孤独的线开始编织。
<孩子>: 请教我何为韧性。
"""
response = get_completion(prompt)
print(response)
```

#### 提供完成步骤

按照需求，逐步的去引导模型输出相应的答案如：第一步、第二步....

```python
text = f"""
在一个迷人的村庄里，兄妹杰克和吉尔出发去一个山顶井里打水。\
他们一边唱着欢乐的歌，一边往上爬，\
然而不幸降临——杰克绊了一块石头，从山上滚了下来，吉尔紧随其后。\
虽然略有些摔伤，但他们还是回到了温馨的家中。\
尽管出了这样的意外，他们的冒险精神依然没有减弱，继续充满愉悦地探索。
"""
# example 1
prompt_1 = f"""
执行以下操作：
1-用一句话概括下面用三个反引号括起来的文本。
2-将摘要翻译成英语。
3-在英语摘要中列出每个人名。
4-输出一个 JSON 对象，其中包含以下键：english_summary，num_names。

请用换行符分隔您的答案。

Text:
```{text}```
"""
response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)
```



### 输出

#### 结构化输出

##### 明确格式

如果需要特定格式的回答，可以在prompt中加入相应的限制。例如，要求AI以列表形式回答问题。

```python
prompt = f"""
请生成包括书名、作者和类别的三本虚构的、非真实存在的中文书籍清单，\
并以 JSON 格式提供，其中包含以下键:book_id、title、author、genre。
"""
response = get_completion(prompt)
print(response)
```

输出结果为：

```json
{
  "books": [
    {
      "book_id": 1,
      "title": "迷失的时光",
      "author": "张三",
      "genre": "科幻"
    },
    {
      "book_id": 2,
      "title": "幻境之门",
      "author": "李四",
      "genre": "奇幻"
    },
    {
      "book_id": 3,
      "title": "虚拟现实",
      "author": "王五",
      "genre": "科幻"
    }
  ]
}
```

#### 限制条件

在 prompt 中添加，如：“使用最多50个词”。

#### 优化输出风格

在 prompt 中添加，如：“侧重于产品的材料构造”。

## 应用场景

### summarize/总结

总结一段文字的中心思想

```python
prompt = f""" Your task is to generate a short summary of a product \ review from an ecommerce site to give feedback to the \ Shipping deparmtment.   Summarize the review below, delimited by triple  backticks, in at most 30 words, and focusing on any aspects \ that mention shipping and delivery of the product.   Review: ```{prod_review}``` """
```

#### 内容查询

- 事实性内容
- 知识性内容：如：麻婆豆腐怎么做？
- 常识性内容

#### 内容总结概括

用于降低人类学习成本和时间成本：作为搜索引擎有效补充

- 如：小说《三体》三部曲分别讲述了什么故事？

#### 生成思维导图

```prompt
做数据库索引优化的原则、方法、注意事项的思维导图，用makedown code。
```

#### extract

从一段文字中抽取出某一方面的信息

```python
prompt = f""" Your task is to extract relevant information from \  a product review from an ecommerce site to give \ feedback to the Shipping department.   From the review below, delimited by triple quotes \ extract the information relevant to shipping and \  delivery. Limit to 30 words.   Review: ```{prod_review}``` """
```

### tranform/转换

#### 语法纠错



```prompt
将此更正为标准英语：She no went to the market。
```

```python
prompt = f"""Proofread and correct the following text     and rewrite the corrected version. If you don't find     and errors, just say "No errors found". Don't use      any punctuation around the text:     ```{t}```"""
```

#### 翻译

相信使用过一段时间的 ChatGPT 之后的你已经发现 LLM 具有强大的翻译能力，支持很多种语言，英语、法语、西班牙语。不仅如此，还支持拼写纠正、语法调整、格式转换等各类文本转换的任务，用起来很方便。

```python
prompt = f""" Translate the following  text to French and Spanish and English pirate: \ ```I want to order a basketball``` """
```

#### 语气转换



```python
prompt = f""" Translate the following from slang to a business letter: 'Dude, This is Joe, check out this spec on this standing lamp.' """
```

#### 格式转换

```python
prompt = f""" Translate the following python dictionary from JSON to an HTML \ table with column headers and title: {data_json} """
```

### expand/扩展

#### 指定人设

```prompt
你是一位总是以苏格拉底风格回应的导师。你从不直接给学生答案，但始终尝试提出正确的问题，已帮助他们学会独立思考。你应该始终根据学生的兴趣和知识调整你的问题，将问题分解为更简单的部分，直到它处于适合他们的水。下面是问题：如何求解线性方程式：3x+2y=7, 9x-4y=1
```

```prompt
作为营销代表，生成信息量大，有说服力的产品描述，突出智能手机的创新功能。该智能手机有以下特点：轻薄、折叠屏、快充、搞清摄像头。
```

```python
prompt = f""" You are a customer service AI assistant. Your task is to send an email reply to a valued customer. Given the customer email delimited by ```, \ Generate a reply to thank the customer for their review. If the sentiment is positive or neutral, thank them for \ their review. If the sentiment is negative, apologize and suggest that \ they can reach out to customer service.  Make sure to use specific details from the review. Write in a concise and professional tone. Sign the email as `AI customer agent`. Customer review: ```{review}``` Review sentiment: {sentiment} """
```

#### 写作



```prompt
请以“世界上只剩最后一个人，门外传来敲门声。”为开头创作一篇科幻小说，要求体现神秘和真挚的感情。
```

#### 生成图片



### inferring/判断

#### 判断对错



#### 理解感情

判断一段文字在某一或某多方面的态度

```python
prompt = f""" What is the sentiment of the following product review,  which is delimited with triple backticks?  Review text: '''{lamp_review}''' """
```



```python
prompt = f""" Identify a list of emotions that the writer of the \ following review is expressing. Include no more than \ five items in the list. Format your answer as a list of \ lower-case words separated by commas.  Review text: '''{lamp_review}''' """
```

#### 信息评级

避免大量低质量的信息泛滥

评级信息包括了真实度、某某领域的专业性、价值度等。信息的需求者可以在阅读信息后对某个印象进行评价反馈。这样有真实度、专业性、有价值的信息源生产的信息会更容易被关注，即使有海量垃圾信息也不会形成太负面影响。不会出现“信息劣币驱逐良币”“优质信息被淹没”的情况。

#### 类比推导

对于few-shot的prompt提供example，类比现有内容

```prompt
下文中首先单独提问了《孤独摇滚！》的类型，作为一部2022年首播的动画，GPT给出了不知道的答案，而之后在提示中加入了2021年就存在的两部动画，没有提示“类型”相关的信息，这时的GPT能给出更详细更接近事实的回答。
```

```python
prompt = f""" Your task is to answer in a consistent style.  <child>: Teach me about patience.  <grandparent>: The river that carves the deepest \  valley flows from a modest spring; the \  grandest symphony originates from a single note; \  the most intricate tapestry begins with a solitary thread.  <child>: Teach me about resilience. """
```

#### 提供推理步骤

指出完成task的具体步骤。但对于复杂问题，可以将其分解为几个简单问题逐一提问，这样可以帮助AI更准确地回答每个子问题。

```python
prompt_1 = f""" Perform the following actions:  1 - Summarize the following text delimited by triple \ backticks with 1 sentence. 2 - Translate the summary into French. 3 - List each name in the French summary. 4 - Output a json object that contains the following \ keys: french_summary, num_names.  Separate your answers with line breaks.  Text: ```{text}``` """
```

```prompt
线索：

1. 小A现在在D1栋工作，并且D1栋只有小A。
2. 会写Python的人现在在D1栋。
3. 小B在D2栋，并且是唯一的人。
4. 小C不在D1栋也不在D2栋。
5. 会写CPP的人现在在D2栋工作。

多选题：小B会写CPP吗？
a. 是的。小B会写CPP。
b. 不是。小B不会写CPP，但他肯定会写Python。
c. 不是。小B不会写CPP，也不会写Python。
d. 没有足够的信息推断小B会写什么语言，这可能要问他本人。

你需要按照以下程序解决这个问题：

1. 查看全部的线索，并考虑线索之间是否具有潜在的相关性，确定线索之间的关联。
2. 结合全部的线索推理出问题的答案。
3. 理解选项的各个主体和意义，将问题的答案映射到多选题的选项上。
```

#### 数学计算/推导



#### 让模型自己思考



### 编程

> 一部分程序员成为了 **AI 代码验证师 + AI 代码修复师**

编程今后大部分将会由 GTP 完成，人类剩下的仅仅是对 GPT 生成的代码片段的组装。Google 预测 3 到 5 年时间，大部分程序员岗位会被生成式 AI 替代。

#### 软件部署安装

```prompt
如何在linux上安装python？
```

#### debug



#### 模拟运行

```prompt
你扮演Linux终端的角色，我输入命令，你运行。
```

#### 写代码

```python
编写一个Python代码来确认一个整数是否是质数。
```



```prompt
用VUE前端框架，帮我生成一个人员信息录入的前端界面，包括人员编号，人员名称，人员性别，电话号码，家庭住址，学历字段。其中人员性别采用下拉列表框，选项为男和女两个选项。前端要包括保存按钮，保存按钮提供调用后端接口的方法入口。
```



```prompt
我现在mysql数据库中有两个数据库表，一个是company表，里面包括了company_id，company_name，address三个字段，还有一个表是contacter表，里面包括了contact_id，contact_name，email，phone，company_id这些字段。请包括写一个逻辑层方法，方法的入口参数是company_id，需要查询数据库返回一个按company_id过滤后的集合，里面包括了company_id,comany_name,contact_id,contact_name,email,phone这些信息。注意需要单独的创建数据库连接和数据库访问方法。注意使用mybatis框架来生成。
```

#### 生成单元测试

```python
为以上代码添加单元测试。
```

#### 写SQL query

```prompt
MySQL表及属性为：##Employee(id,name,department_id) # Department(id, name, address) # Salary_Payments(id, employee_id, amount, date) # ### 查询列出过去3个月内雇佣超过10名员工的部门名称。
```



