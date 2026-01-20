# 钉钉群聊机器人定时推送消息

![GitHub repo size](https://img.shields.io/github/repo-size/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![Bitbucket  issues](https://img.shields.io/github/issues-closed/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)

## 📒 简介

> :smiley: 通过GitHub Actions给钉钉群聊定时推送消息（Python）。

### ✨ 主要特性

- 🤖 基于钉钉自定义机器人的消息推送
- ⏰ 使用GitHub Actions实现定时任务，无需自建服务器
- 🌤️ 集成高德地图天气API，支持多个城市天气查询
- 📝 支持Markdown格式的消息展示，排版美观
- 💬 每日一句名言/鸡汤推送
- 🔄 完善的错误处理和降级机制
- 🆓 完全免费，无需付费资源

## 🚀 快速开始

### 准备工作

在开始之前，您需要准备：

1. 一个钉钉账号和一个钉钉群聊
2. 一个GitHub账号
3. 高德地图API密钥（免费申请）

### 步骤一：配置钉钉机器人

#### 1.1 创建钉钉群聊
打开钉钉，点击+发起群聊（如你有公司，需要有两个不是公司的好友才能创建普通群），创建完成后，打开群聊中的设置，智能群助手。

#### 1.2 添加自定义机器人
进入到机器人管理页面，点击添加机器人，进入机器人选择页面，这里选择自定义机器人。

![在这里插入图片描述](https://img-blog.csdnimg.cn/16042ba005e94ae480a83dd9c65ea220.png)

#### 1.3 配置机器人
需要给机器人修改头像和名称，在安全设置里面，**建议最好把自定义关键字也勾选上**，比如设置关键字为：**早上好**，然后其他的可以默认，点击完成后在新的页面有一个webhook

![在这里插入图片描述](https://img-blog.csdnimg.cn/d03d721b6c20482d8b6517af8ec284a3.png)

#### 1.4 保存Webhook地址
获取到Webhook地址后，用户可以向这个地址发起HTTP POST 请求，即可实现给该钉钉群发送消息。

**⚠️ 重要提示：**
- Webhook地址包含access_token，请妥善保管，不要泄露在网上
- 每个机器人每分钟最多发送20条消息
- 必须将字符集编码设置成UTF-8

### 步骤二：申请高德地图API密钥

#### 2.1 注册高德开放平台账号
访问 [高德开放平台](https://lbs.amap.com/)，注册并登录账号。

#### 2.2 创建应用
1. 进入控制台，点击"应用管理" -> "我的应用"
2. 点击"创建新应用"，填写应用名称和类型
3. 在应用下添加Key，选择服务平台为"Web服务"
4. 保存生成的Key（这就是你的AMAP_KEY）

> 💡 高德地图API每天提供一定的免费调用额度，个人使用完全足够

### 步骤三：配置GitHub Actions

#### 3.1 Fork或克隆本项目
将本项目Fork到你的GitHub账户，或者克隆后推送到你自己的仓库。

#### 3.2 配置Secrets
在你的仓库中进入 `Settings` -> `Secrets and variables` -> `Actions`，点击 `New repository secret` 添加以下三个Secrets：

| Secret名称 | 说明 | 示例 |
|-----------|------|------|
| `TOKEN_DD` | 钉钉机器人Webhook中的access_token部分 | `abc123def456...` |
| `CITY` | 城市名称或城市编码，支持多个城市（用逗号分隔） | `北京` 或 `110000,310000` |
| `AMAP_KEY` | 高德地图API密钥 | `your_amap_key_here` |

**城市配置说明：**
- 单个城市：直接填写城市名称，如 `北京`、`上海`、`广州`
- 多个城市：使用城市编码并用逗号分隔，如 `110000,310000`（北京和上海）
- 城市编码查询：[高德地图城市编码表](https://lbs.amap.com/api/webservice/guide/api/district)

#### 3.3 配置定时任务（可选）

在 `.github/workflows/main.yml` 文件中，可以修改定时任务的执行时间：

```yaml
schedule:
  # UTC 时间的零点，对应北京时间的上午8点
  - cron: '0 0 * * *'
```

**常用时间配置（cron表达式使用UTC时间）：**
- `0 0 * * *` - 每天UTC 0:00 = 北京时间8:00
- `30 0 * * *` - 每天UTC 0:30 = 北京时间8:30
- `0 1 * * *` - 每天UTC 1:00 = 北京时间9:00
- `0 0 * * 1-5` - 每周一到周五UTC 0:00 = 北京时间8:00

> ⚠️ 注意：
> - GitHub Actions的cron表达式使用UTC时间，北京时间 = UTC时间 + 8小时
> - 由于GitHub Actions同一时间任务较多，实际执行时间可能会有几分钟的延迟

#### 3.4 手动触发（测试）

除了定时执行，你也可以在 GitHub Actions 页面手动触发工作流进行测试：
1. 进入你的仓库
2. 点击 `Actions` 标签
3. 选择 `morning` 工作流
4. 点击 `Run workflow` 按钮
5. 查看钉钉群是否收到消息

## 📱 消息效果

程序会发送Markdown格式的消息到钉钉群，包含以下内容：

- 🌅 早安问候
- 📍 城市天气信息（支持多城市）
  - ☁️ 天气状况
  - 🌡️ 实时温度
  - 💨 风向风力
  - 💧 空气湿度
  - 🕐 更新时间
- 💬 每日一句名言/鸡汤

## 📚 钉钉机器人消息类型参考

本项目默认使用Markdown格式发送消息，钉钉机器人还支持其他多种消息类型。以下是各类型的详细说明：

### 支持的消息类型

目前钉钉机器人支持发送的消息有5种：
1. **文本 (text)** - 纯文本消息
2. **链接 (link)** - 带链接的卡片消息
3. **markdown** - Markdown格式消息（本项目使用）
4. **ActionCard** - 交互式卡片消息
5. **FeedCard** - 多条链接聚合消息

具体需要根据自己的场景进行选择，以便能达到最好的展示样式。

自定义机器人发送消息时，可以通过手机号码指定"被@人列表"。在"被@人列表"里面的人员收到该消息时，会有@消息提醒。免打扰会话仍然通知提醒，首屏出现"有人@你"

#### 文本TEXT

文本型的消息类型，具体代码如下：

```json
{
    "at": {
        "atMobiles":[
            "180xxxxxx"
        ],
        "atUserIds":[
            "user123"
        ],
        "isAtAll": false
    },
    "text": {
        "content":"测试"
    },
    "msgtype":"text"
}
```

上述中涉及的参数类型分别如下：

| **参数**  | **参数类型** | **是否必填** | **说明**                                                     |
| --------- | ------------ | ------------ | ------------------------------------------------------------ |
| msgtype   | String       | 是           | 消息类型，此时固定为：text。                                 |
| content   | String       | 是           | 消息内容。                                                   |
| atMobiles | Array        | 否           | 被@人的手机号。**注意** 在content里添加@人的手机号，且只有在群内的成员才可被@，非群内成员手机号会被脱敏。 |
| atUserIds | Array        | 否           | 被@人的用户userid。**注意** 在content里添加@人的userid。     |
| isAtAll   | Boolean      | 否           | 是否@所有人。                                                |

#### 链接LINK

链接型的消息类型，具体代码如下：

```json
{
    "msgtype": "link", 
    "link": {
        "text": "测试", 
        "title": "测试", 
        "picUrl": "", 
        "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**   | **参数类型** | 是否必填 | **说明**                                                     |
| ---------- | ------------ | -------- | ------------------------------------------------------------ |
| msgtype    | String       | 是       | 消息类型，此时固定为：link。                                 |
| title      | String       | 是       | 消息标题。                                                   |
| text       | String       | 是       | 消息内容。如果太长只会部分展示。                             |
| messageUrl | String       | 是       | 点击消息跳转的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| picUrl     | String       | 否       | 图片URL。                                                    |

#### markdown类型

markdown的消息类型，具体代码如下：

```json
{
     "msgtype": "markdown",
     "markdown": {
         "title":"测试",
         "text": "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
     },
      "at": {
          "atMobiles": [
              "188XXXXXXXX"
          ],
          "atUserIds": [
              "user123"
          ],
          "isAtAll": false
      }
 }
```

上述中涉及的参数类型分别如下：

| **参数**  | **类型** | 是否必填 | **说明**                                                     |
| --------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype   | String   | 是       | 消息类型，此时固定为：markdown。                             |
| title     | String   | 是       | 首屏会话透出的展示内容。                                     |
| text      | String   | 是       | markdown格式的消息。                                         |
| atMobiles | Array    | 否       | 被@人的手机号。**注意** 在text内容里要有@人的手机号，只有在群内的成员才可被@，非群内成员手机号会被脱敏。 |
| atUserIds | Array    | 否       | 被@人的用户userid。**注意** 在content里添加@人的userid。     |
| isAtAll   | Boolean  | 否       | 是否@所有人。                                                |



#### 整体跳转ActionCard类型

整体跳转ActionCard的消息类型，具体代码如下：

```json
{
    "actionCard": {
        "title": "测试", 
        "text": "测试", 
        "btnOrientation": "0", 
        "singleTitle" : "测试",
        "singleURL" : "https://www.dingtalk.com/"
    }, 
    "msgtype": "actionCard"
}
```

上述中涉及的参数类型分别如下：

| **参数**       | **类型** | **是否必填** | **说明**                                                     |
| -------------- | -------- | ------------ | ------------------------------------------------------------ |
| msgtype        | String   | 是           | 消息类型，此时固定为：actionCard。                           |
| title          | String   | 是           | 首屏会话透出的展示内容。                                     |
| text           | String   | 是           | markdown格式的消息。                                         |
| singleTitle    | String   | 是           | 单个按钮的标题。**注意** 设置此项和singleURL后，btns无效。   |
| singleURL      | String   | 是           | 点击消息跳转的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | 否           | 0：按钮竖直排列1：按钮横向排列                               |


#### 独立跳转ActionCard类型

独立跳转ActionCard的消息类型，具体代码如下：

```json
{
    "msgtype": "actionCard",
    "actionCard": {
        "title": "测试", 
        "text": "测试", 
        "btnOrientation": "0", 
        "btns": [
            {
                "title": "内容不错", 
                "actionURL": "https://www.dingtalk.com/"
            }, 
            {
                "title": "不感兴趣", 
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**       | **类型** | 是否必填 | 说明                                                         |
| -------------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype        | String   | 是       | 此消息类型为固定actionCard。                                 |
| title          | String   | 是       | 首屏会话透出的展示内容。                                     |
| text           | String   | 是       | markdown格式的消息。                                         |
| btns           | Array    | 是       | 按钮。                                                       |
| title          | String   | 是       | 按钮标题。                                                   |
| actionURL      | String   | 是       | 点击按钮触发的URL，打开方式如下：移动端，在钉钉客户端内打开PC端默认侧边栏打开希望在外部浏览器打开，请参考[消息链接说明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | 否       | 0：按钮竖直排列1：按钮横向排列                               |

#### FeedCard类型

FeedCard的消息类型，具体代码如下：

```json
{
    "msgtype":"feedCard",
    "feedCard": {
        "links": [
            {
                "title": "测试1", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "测试2", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ]
    }
}
```

上述中涉及的参数类型分别如下：

| **参数**   | **类型** | 是否必填 | **说明**                                                     |
| ---------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype    | String   | 是       | 此消息类型为固定feedCard。                                   |
| title      | String   | 是       | 单条信息文本。                                               |
| messageURL | String   | 是       | 点击单条信息到跳转链接。**说明** PC端跳转目标页面的方式，参考[消息链接在PC端侧边栏或者外部浏览器打开](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)。 |
| picURL     | String   | 是       | 单条信息后面图片的URL。                                      |

## 🛠️ 技术实现

### 项目结构

```
.
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions 工作流配置
├── main.py                   # 主程序文件
├── requirements.txt          # Python依赖列表
└── README.md                 # 项目说明文档
```

### 核心功能说明

#### 天气API集成

本项目使用高德地图天气API获取实时天气信息，相比其他天气API的优势：
- ✅ 稳定可靠，服务质量高
- ✅ 免费额度充足，个人使用足够
- ✅ 支持多城市同时查询
- ✅ 返回数据全面（温度、湿度、风力等）

#### 错误处理机制

代码实现了完善的错误处理：
- 网络请求超时自动重试
- API调用失败时使用默认数据
- 异常情况下不会中断程序执行
- 所有错误都会记录日志便于排查

#### 消息格式化

使用Markdown格式发送消息，支持：
- 表情符号增强视觉效果
- 层次清晰的信息组织
- 支持多城市信息展示
- 自动格式化单位（温度、湿度等）

## 🔧 常见问题

### Q1: 为什么消息没有按时发送？
**A:** GitHub Actions的定时任务由于同时运行的任务较多，可能会有5-10分钟的延迟，这是正常现象。

### Q2: 如何修改消息内容？
**A:** 编辑 `main.py` 文件中的消息模板部分，可以自定义消息格式和内容。

### Q3: 支持多少个城市同时查询？
**A:** 理论上没有限制，但建议不超过5个城市，以保持消息的可读性。

### Q4: 如何更换每日一句的API？
**A:** 修改 `get_words()` 函数中的API地址即可，确保返回格式兼容。

### Q5: 可以修改发送时间吗？
**A:** 可以，修改 `.github/workflows/main.yml` 中的 cron 表达式即可。注意使用UTC时间。

### Q6: Secrets配置错误会怎样？
**A:** GitHub Actions会执行失败，可以在Actions页面查看详细的错误日志。

## 📝 更新日志

### 最新版本特性

- ✅ 集成高德地图天气API，数据更准确
- ✅ 支持多城市天气查询
- ✅ 优化Markdown消息格式，增加emoji
- ✅ 完善错误处理和降级机制
- ✅ 自动格式化天气数据单位
- ✅ 支持手动触发工作流

## 🤝 项目地址

[GitHub Repository](https://github.com/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly)

## ☕ 鸣谢

感谢以下参考的帮助：

- [https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
- [https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions)
- [https://lbs.amap.com/api/webservice/guide/api/weatherinfo](https://lbs.amap.com/api/webservice/guide/api/weatherinfo)
- [https://open.dingtalk.com/document/robots/custom-robot-access](https://open.dingtalk.com/document/robots/custom-robot-access)

> 均为互联网资料，如有侵权请联系删除。有问题可以点击Issues提问。

## 📄 License

本项目仅供学习交流使用，请勿用于商业用途。

---

⭐ 如果这个项目对你有帮助，欢迎Star支持！
