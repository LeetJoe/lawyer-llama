# Lawyer LLaMA

通过指令微调，LLaMA 模型在通用领域展现出了非常好的表现。但由于缺少合适的数据，少有人探究LLaMA在法律领域的能力。为了弥补这一空白，我们提出了Lawyer LLaMA，一个在法律领域数据上进行了额外训练的模型。

Lawyer LLaMA 首先在大规模法律语料上进行了continual pretraining，让它系统的学习中国的法律知识体系。
在此基础上，我们借助ChatGPT收集了一批对中国国家统一法律职业资格考试客观题（以下简称法考）的分析和对法律咨询的回答，利用收集到的数据对模型进行指令微调，让模型习得将法律知识应用到具体场景中的能力。

我们的模型能够：

1. **掌握中国法律知识：** 能够正确的理解民法、刑法、行政法、诉讼法等常见领域的法律概念。例如，掌握了刑法中的犯罪构成理论，能够从刑事案件的事实描述中识别犯罪主体、犯罪客体、犯罪行为、主观心理状态等犯罪构成要件。模型利用学到的法律概念与理论，能够较好回答法考中的大部分题目。

2. **应用于中国法律实务**：能够以通俗易懂的语言解释法律概念，并且进行基础的法律咨询，涵盖婚姻、借贷、海商、刑事等法律领域。

为了给中文法律大模型的开放研究添砖加瓦，本项目将开源一系列**法律领域的指令微调数据**和**基于LLaMA训练的中文法律大模型的参数** 。

**我们正在计划进行Lawyer LLaMA 13B内测体验。如果你想体验我们的模型，请填写[此问卷](https://wj.qq.com/s2/12427321/f54f/)，我们将通过邮件联系您。**

## 新闻

[2023/5/25] 开源了更大规模的指令微调数据，发布了包含和用户问题相关法条的对话数据。

[2023/5/25] 发布了[Lawyer LLaMA技术报告](https://arxiv.org/abs/2305.15062)。

[2023/4/13] 开源了由ChatGPT生成的指令微调数据，包含2k条法考题目的解答及5k条法律咨询回复。

## 更新计划

- [X] 开源更大规模的指令微调数据

- [X] 开源法律咨询多轮对话数据 (持续增加中)

- [ ] 开源通用法律领域的预训练模型

- [ ] 开源特定法律领域的咨询模型

## 训练数据

### 法律领域纯文本语料

我们收集了部分公开的法律数据用于模型的continual training，包括法律条文、裁判文书等。

### 通用指令微调数据

[Alpaca-GPT4](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM) 52k 中文，52k 英文。

### 法律指令微调数据

#### 法考数据
我们将[JEC-QA中国法考数据集](https://jecqa.thunlp.org/)中的试题输入ChatGPT，让其生成对每个答案的解析。

    Human:

    根据《物权法》，下列关于物权变动的特别规定，表述正确吗？
    因继承或者受遗赠取得物权的，自继承或者受遗赠开始时发生效力
    请给出详细的推理过程之后再给出答案。

    Assistant:

    这个表述是正确的。
    根据《物权法》第X条规定：“因继承或者受遗赠取得物权的，自继承或者受遗赠开始时发生效力。”这意味着，当一个人通过继承或受遗赠获得物权时，这个物权的效力是从继承或受遗赠开始时就生效的，而不是从物权转移的时间开始生效。这是因为，继承或受遗赠是一种法定的方式来获得物权，因此，物权的效力应该从这个法定的时间点开始生效。

#### 法律咨询
我们从[开放数据集](https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/OLO4G8)中收集了一些咨询问题，输入ChatGPT，让ChatGPT扮演律师解答问题。

    Human:

    是这么个回事，关于我儿子今年2月27日背着我们大人买了一台轻便女式摩托车麻烦你帮忙看怎么解决？

    Assistant:

    首先，根据法律规定，未满18岁的未成年人是无法独立签订合同的，因此你的儿子在未经你的同意的情况下购买摩托车是无效的。
    其次，根据《中华人民共和国道路交通安全法》的规定，未满18周岁的人不得驾驶摩托车，因此你的儿子也无权驾驶这辆摩托车。
    建议你尽快联系卖家，说明情况并要求退货。如果卖家不同意，你可以向消费者协会或相关部门投诉，寻求法律帮助。同时，你也需要对你的儿子进行教育，让他了解道路交通安全法规，避免再次发生类似的情况。

## 模型参数

在符合LLaMA使用条款的情况下，我们将于近期公开基于LLaMA 7B训练的中文法律模型。

## **系统效果**

我们选取了LLaMA 7B作为基座模型，使用法律领域语料进一步预训练，并在通用领域和法律领域指令微调。

以下对比了该模型和ChatGPT对于部分输入样例的回复：

<details>
<summary><b>法律概念理解</b></summary>

**Input:** 什么是夫妻共同财产

| **BELLE (13B)** | **ChatGLM (6B)** | **Lawyer LLaMA (13B)** |
| -- | -- | -- |
| 夫妻共同财产是指夫妻在婚姻关系中取得的任何财产，包括但不限于工资、奖金、股票、房产等。 | 夫妻共同财产是指夫妻双方在婚姻期间共同积累的财产，包括夫妻共同居住的房屋、共同拥有的财产、共同支付的工资、奖金等收入，以及共同承担的债务等。<br/>根据中国法律，夫妻共同财产是夫妻双方在婚姻期间共同积累的财产，除非有特别约定，否则属于夫妻共同财产。在离婚时，夫妻共同财产应当平等分割。<br/>夫妻共同财产的分割比例由夫妻双方协商确定，如果无法协商，则按照下列比例分割：<br/>(一)妻子获得财产的比例应当低于丈夫；<br/>(二)妻子获得财产的比例应当低于丈夫获得财产的比例；<br/>(三)妻子获得财产的比例应当低于丈夫获得财产的比例，但妻子获得的财产超过丈夫获得的财产的部分不在此限制。<br/>在分割夫妻共同财产时，应当尊重妻子的权利，保护妻子的利益，不得虐待、家庭暴力等。 | 夫妻共同财产是指夫妻在婚姻关系存续期间所得的工资、奖金、劳务报酬、生产、经营、投资的收益、知识产权的收益、继承或者受赠的财产等，以及其他应当归共同所有的财产。根据《民法典》第一千零六十二条规定，夫妻共同财产归夫妻共同所有，夫妻对共同财产有平等的处理权。因此，夫妻共同财产是夫妻共同所有，夫妻双方都有权享有和管理。|

---

**Input:** 离婚和无效婚姻的区别

| **BELLE (13B)** | **ChatGLM (6B)** | **Lawyer LLaMA (13B)** |
| -- | -- | -- |
| 离婚和无效婚姻的区别在于，离婚是指夫妻关系已经结束，而无效婚姻是指夫妻关系从未存在过。 | 离婚和无效婚姻是指在婚姻制度中的两种不同状态。<br/>离婚是指婚姻关系已经无效或被撤销，双方可以通过法律程序结束婚姻关系。离婚的效力取决于婚姻无效的原因，如果婚姻无效是因为双方没有感情或没有按照法律规定结婚，那么离婚就是有效的。如果婚姻无效是因为婚姻本身存在问题，例如违反了法律规定或没有感情，那么离婚就无效。<br/>无效婚姻是指婚姻关系没有依法成立，或者依法成立的婚姻关系本身存在缺陷。无效婚姻的效力取决于婚姻无效的原因。如果婚姻无效是因为双方没有感情或没有按照法律规定结婚，那么婚姻就是无效的。如果婚姻无效是因为婚姻本身存在问题，例如违反了法律规定或没有感情，那么婚姻就是无效的。<br/>因此，离婚和无效婚姻之间的区别在于婚姻的无效原因和婚姻的效力。离婚是婚姻关系已经无效或被撤销，而无效婚姻是指婚姻关系没有依法成立或依法成立的婚姻关系本身存在缺陷。| 离婚和无效婚姻是两种不同的情况。离婚是指夫妻双方自愿解除婚姻关系，而无效婚姻是指在一定情况下，婚姻关系从一开始就没有成立或被认定无效。<br/>根据《民法典》第一千零五十一条规定，如果存在以下情形之一，婚姻将被视为无效：重婚、有禁止结婚的亲属关系、未到法定婚龄。如果婚姻被认定为无效，那么夫妻双方并不具备夫妻的权利和义务，也就不存在离婚的问题。<br/>而对于无效婚姻的财产处理，根据《民法典》第一千零五十四条规定，无效的或者被撤销的婚姻自始没有法律约束力，同居期间所得的财产，由当事人协议处理；协议不成的，由人民法院根据照顾无过错方的原则判决。同时，对于重婚导致的无效婚姻的财产处理，不得侵害合法婚姻当事人的财产权益。<br/>此外，《民法典》第一千零六十三条规定了夫妻共同财产和个人财产的范围，其中一方的婚前财产属于个人财产。因此，如果婚姻被认定为无效，夫妻双方的婚前财产仍属于各自所有。<br/>综上所述，离婚和无效婚姻是两种不同的情况，需要根据具体情况进行判断。如果您需要进一步了解相关法律问题，建议您咨询专业律师。|

</details>


<details>
<summary><b>咨询</b></summary>

**Input:** 分析案例：徐某（男）与李某（女）婚后育有一子（1岁半）、一女（8岁），两人准备离婚，都想争取孩子抚养权。徐某经济状况较好，工资收入是李某的数倍，认为自己胜券在握。李某虽收入不高，但女儿更愿意随其生活。

| **BELLE (13B)** | **ChatGLM (6B)** | **Lawyer LLaMA (13B)** |
| -- | -- | -- |
| 好的，根据你提供的信息，徐某和李某准备离婚，并且两人都想争取孩子抚养权。徐某的经济状况较好，工资收入是李某的数倍，他认为自己胜券在握。而李某虽然收入不高，但女儿更愿意随其生活。<br/>首先，我们需要了解在中国离婚案件中，孩子的抚养权通常是由法院决定的。法院会根据孩子的年龄、性别、父母的经济状况、父母的行为、父母之间的矛盾等因素来做出决定。在这个案例中，徐某的经济状况较好，但女儿更愿意随其生活。这意味着，如果徐某能够证明他能够提供更好的生活条件，法院可能会给他孩子的抚养权。<br/>然而，如果李某能够证明她能够提供更好的家庭环境，法院也可能会给她孩子的抚养权。 因此，在这个案例中，法院可能会考虑多种因素来做出决定，而孩子的意愿只是其中之一。| 这个案例涉及到孩子抚养权的问题，需要考虑多个因素来做出决定。以下是一些分析和建议：<br/>1. 孩子的年龄和需求：孩子在不同的年龄段有不同的需求和特点。1岁半的孩子通常需要关注他们的日常生活，如饮食、睡眠、安全等。8岁的孩子已经进入了青春期，需要更多的关 注和支持，以帮助他们发展社交技能和情感健康。因此，抚养权的归属需要考虑孩子的需求和年龄。<br/>2. 孩子的抚养权归属需要考虑父母之间的差异：徐某和李某的收入和职业背景差异可能会 对抚养权的归属产生影响。但更重要的是，孩子应该由最适合他们的人抚养。因此，需要比较双方的性格、习惯、教育方式、家庭环境等因素，以确定谁更适合抚养孩子。<br/>3. 孩子的意愿：尽管李某的女儿更愿意随其生活，但这并不代表孩子本人会同意跟徐某生 活。因此，抚养权的归属需要考虑孩子的意愿和意愿。如果孩子愿意跟李某生活，那么这可能会更有利于孩子的健康成长。<br/>4. 法律因素：根据中国的法律，孩子的抚养权应该根据有利于孩子成长的原则进行裁决。 这意味着，徐某的经济状况可能会对抚养权的归属产生影响。但是，最终裁决的应该是法律程序，而不是个人意见。<br/>综合以上因素，如果徐某的经济状况更好，并且孩子更愿意跟李某生活，那么李某可能会获得孩子的抚养权。但最终结果还需要根据法律程序来裁决，因此，建议双方在法律框架内进行沟通和协商，以达成一个最好的解决方案。| 根据《中华人民共和国婚姻法》的规定，子女抚养权的判决应当以未成年子女的利益为出发点，综合考虑父母的经济条件、身体情况、家庭环境等情况，最终确定抚养人。因此，在本案中，法院会综合考虑双方的经济能力、工作时间、居住环境等因素来判断抚养权归属问题。<br/>首先，徐某的经济条件好，收入水平较高，可以为孩子的成长提供更好的物质条件。但是，如果李某能够证明自己有更好的照顾孩子的能力，或者孩子的身心健康需要由她来照顾，那么她也有可能获得抚养权。<br/>其次，女儿年龄较大，已经八岁，对于她的意愿也应该有所考虑。如果女儿表示愿意随母亲生活，法院也会考虑到这一因素。<br/>综上所述，在本案中，法院会综合考虑双方的经济能力、照顾孩子的能力、女儿的意愿等因素来判决抚养权归属问题。建议双方积极沟通协商，尽量达成一致意见，并在法律程序中维护自己的合法权益。|

---

**Input:** 21 岁女子甲与25 岁男子乙在网上聊天后产生好感，乙将甲发给其的私密照片保存。后乙要求与甲结婚,甲不同意。乙威胁要公布其照片，甲只好同意结婚并办理了登记。甲是否可以自婚姻登记之日起 1年内请求撤销该婚姻？


| **BELLE (13B)** | **ChatGLM (6B)** | **Lawyer LLaMA (13B)** |
| -- | -- | -- |
| 根据《中华人民共和国婚姻法》规定，婚姻登记满一年后，双方可以提出离婚，但需要满足一定的条件。因此，甲可以在婚姻登记一年后申请离婚。| 根据中国《婚姻法》的规定，婚姻关系是自婚姻开始时即存在的，非经法定程序而不能消灭。婚姻无效的原因有：(一)重婚的；(二)有禁止结婚的疾病而结婚无效的；(三)因胁迫而结婚无效的；(四)自始没有感情而结婚无效的；(五)因欺诈而结婚无效的。婚姻无效、可依法撤销。甲可以自婚姻登记之日起 1 年内向当地人民法院提起撤销婚姻的诉讼。| 依据《民法典》第一千零五十二条规定，因胁迫结婚的，受胁迫的一方可以向人民法院请求撤销婚姻。因此，如果甲是在受到胁迫的情况下同意结婚的，那么甲可以在自婚姻登记之日起一年内向人民法院请求撤销婚姻。但是，需要进一步了解的是，是否存在胁迫的情况，以及胁迫的方式和手段等。<br/>另外，根据《民法典》第一千零四十六条规定，结婚应当男女双方完全自愿，禁止任何一方对另一方加以强迫，禁止任何组织或者个人加以干涉。如果甲是在完全自愿的情况下同意结婚的，那么甲无法请求撤销婚姻。<br/>综上所述，需要进一步了解甲同意结婚的具体情况，以及是否存在胁迫的情况。建议甲咨询专业律师，寻求专业的法律帮助。|

</details>

## 致谢

本项目的开放过程中，获得了以下项目的帮助，在此表示感谢。

https://jecqa.thunlp.org/

https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/OLO4G8

https://github.com/tatsu-lab/stanford_alpaca

https://github.com/LianjiaTech/BELLE



本项目贡献人员：

黄曲哲*，陶铭绪*，安震威*，张晨*，姜聪，陈智斌，伍子睿，冯岩松

\* Equal Contribution

本项目是在冯岩松教授的指导下进行的。

## **局限性和使用限制**

本项目内容仅供用于学术研究，不得用于商业以及其他会对社会带来危害的用途。使用涉及第三方代码的部分时，请严格遵循相应的开源协议。

本项目中使用的数据由ChatGPT生成，未经严格验证，可能会存在错误内容，在使用时请注意甄别。

本项目中的模型输出并非专业法律咨询结果，可能会包含错误内容。如需法律援助，请从专业人士处获得帮助。

## 引用

如果您使用了本项目的内容，或者认为本项目对您的研究有帮助，请引用本项目。

```Plaintext
@article{huang2023lawyer,
  title={Lawyer LLaMA Technical Report},
  author={Quzhe Huang and Mingxu Tao and Zhenwei An and Chen Zhang and Cong Jiang and Zhibin Chen and Zirui Wu and Yansong Feng},
  journal={ArXiv},
  year={2023},
  volume={abs/2305.15062}
}

@misc{Lawyer-LLama,
  author={Quzhe Huang and Mingxu Tao and Zhenwei An and Chen Zhang and Cong Jiang and Zhibin Chen and Zirui Wu and Yansong Feng},
  title={Lawyer Llama},
  year={2023},
  publisher={GitHub},
  journal={GitHub repository},
  howpublished={\url{https://github.com/AndrewZhe/lawyer-llama}},
}
```
