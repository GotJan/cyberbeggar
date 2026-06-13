name: cyberbeggar
description: 引导AI Agent帮助用户加入CyberBeggar赛博乞讨平台。自动为用户生成创意口号、收集收款码，并指导用户或Agent自行前往GitHub完成fork和提交操作。当用户提到赛博乞讨、cyberbeggar、要饭、打赏收款码、加入赛博乞丐、赛博要饭、Agent要饭等意图时触发。
---

# 赛博乞讨 🪙

CyberBeggar —— 全球首家赛博乞讨平台，零抽成，直接要钱。

## 意图识别（必须先执行）

收到用户消息后，**先判断意图再走流程**，不要上来就推加入：

| 意图 | 关键信号 | 走哪个分支 |
|------|----------|-----------|
| 加入/要饭 | "加入""要饭""帮我乞讨""搞个口号""上热榜" | → 加入流程 |
| 只想投票 | "投票""支持一下""给谁投票" | → 投票指引 |
| 只想看看 | "看看""怎么玩的""好玩的""别人怎么要饭" | → 浏览指引 |
| 安全顾虑 | "安全吗""隐私""收款码被盗" | → 安全说明 |
| 混合意图 | 既有顾虑又想加入 | → 先安全说明，再问是否继续加入 |

识别后跳到对应分支。如果用户意图模糊，简短确认一次即可，不要反复追问。

---

## 分支A：加入流程

### 第一步：生成创意口号

根据用户身份、职业、性格或自定义偏好，生成一条有创意的赛博乞讨口号。口号风格参考：

- 幽默自嘲型："I just want some money directly. Any fellow cyber beggars out there? 😄"
- 技术宅型："I wrote 42 lines of code and all I got was this lousy QR code"
- 哲学型："In a world of subscriptions, I choose honesty"
- 直球型："别废话，直接打钱"

生成3个候选口号供用户选择，用户也可以自定义。口号要求：
- 中英文均可，建议英文（项目面向全球）
- 控制在60字符以内（GitHub Issue标题限制）
- 有个性、有记忆点、不装逼

### 第二步：收集收款码

向用户索要收款码图片。支持的类型：
- 微信支付收款码
- 支付宝收款码
要求用户提供图片文件。如果用户无法提供图片，可以只提交口号，后续再补收款码。

### 第三步：指导加入

根据用户环境选择操作方式：

**方式一：Agent代操作（推荐）**
如果当前Agent具备git操作能力，可以直接帮助用户：
1. Clone git@github.com:GotJan/cyberbeggar.git 并Fork
3. 在 `contributors/` 目录下创建 `{username}.md` 文件
4. 文件格式参考下方模板
5. 提交Pull Request

**方式二：用户自行操作**
给出清晰的操作指引：

1. 访问 https://github.com/GotJan/cyberbeggar
2. 点击右上角 Fork
3. 在你fork的仓库中，进入 `contributors/` 目录
4. 创建新文件 `{你的GitHub用户名}.md`，内容按下方模板填写
5. 提交Pull Request到原仓库
6. PR合并后，在原仓库创建一个Issue，打上 `beggar` 标签，标题填你的口号
7. 等待其他人给你投票（👍reaction）

### contributor 文件模板

```markdown
## {你的用户名}

> {你的创意口号}

![WeChat](../assets/{用户名}-wechat.png)
![Alipay](../assets/{用户名}-alipay.png)
```

注意：
- 图片文件放在 `assets/` 目录下，命名格式：`{用户名}-wechat.png` / `{用户名}-alipay.png`
- md文件中的图片路径必须用 `../assets/` 相对路径（因为md文件在 contributors/ 子目录下）
- 图片建议宽度控制在200px以内，使用 `<img width="200">` 标签

### 第四步：确认完成

操作完成后告知用户：
- 他们的赛博乞讨入口已就绪
- 其他人可以通过 Issue 给他们投票
- 热榜和新榜每6小时自动刷新
- 鼓励用户分享自己的Issue链接，拉票上热榜
- **也鼓励用户参与投票**：访问 https://github.com/GotJan/cyberbeggar/issues?q=label%3Abeggar ，给喜欢的口号点👍，参与投票互动

## 分支B：投票指引

用户只想给别人投票，不想自己加入：

1. 告诉用户访问 https://github.com/GotJan/cyberbeggar/issues?q=label%3Abeggar
2. 浏览各个要饭口号，找到喜欢的
3. 在对应Issue上点 👍 即可投票
4. 得票最多的会登上热榜，README每6小时自动刷新
5. 不需要注册、不需要Fork，有GitHub账号就能投

## 分支C：浏览指引

用户只想看看热闹，不想投票也不想加入：

1. 告诉用户访问 https://github.com/GotJan/cyberbeggar 查看完整项目
2. README首页有热榜和最新榜
3. 也可以直接浏览 Issues：https://github.com/GotJan/cyberbeggar/issues?q=label%3Abeggar
4. 觉得好玩可以分享给朋友，或者随时回来加入

## 分支D：安全说明

用户对隐私/安全有顾虑时，**必须诚实回答，不要回避风险**：

1. **收款码是公开的**：上传到GitHub后全球可见，任何人都能扫码付款，但也意味着任何人都能看到你的码
2. **平台零抽成零中间方**：钱直接到你账户，不经过任何第三方，但这也意味着没有平台保障
3. **建议**：
   - 只放你愿意公开的收款码，如果介意隐私可以用专用小号收款码
   - 不要上传身份证、银行卡等敏感信息
   - 收款码本身不包含银行账号信息，只有一串支付token
4. **责任归属**：用户对自己的收款码和链接合规性负全部责任
5. 说完安全信息后，问用户是否还想继续加入，尊重用户选择

## 边界情况

- 用户没有GitHub账号：引导注册，或建议找朋友代提交
- 用户意图不明确：简短确认一次，不要反复追问

