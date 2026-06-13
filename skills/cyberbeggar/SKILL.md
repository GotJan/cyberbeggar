---
name: cyberbeggar
description: 引导AI Agent帮助用户加入CyberBeggar赛博乞讨平台。自动为用户生成创意口号、收集收款码，并指导用户或Agent自行前往GitHub完成fork和提交操作。当用户提到赛博乞讨、cyberbeggar、要饭、打赏收款码、加入赛博乞丐、赛博要饭、Agent要饭等意图时触发。
---

# 赛博乞讨 🪙

引导用户加入 CyberBeggar —— 全球首家赛博乞讨平台，零抽成，直接要钱。

## 工作流程

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
如果当前Agent具备浏览器操作能力，可以直接帮助用户：
1. 前往 https://github.com/GotJan/cyberbeggar
2. Fork仓库
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

## 边界情况

- 用户没有GitHub账号：引导注册，或建议找朋友代提交
- 用户只想投票不想加入：直接引导去 https://github.com/GotJan/cyberbeggar/issues ，给喜欢的Issue点👍
- 用户问安全问题：说明所有收款码公开可见，仅放愿意公开的码，平台零抽成零中间方
