# DingTalk Group Chat Robot - Scheduled Message Push

**Language/语言**: [English](README.md) | [日本語](README_JP.md) | [中文](README_CN.md)

![GitHub repo size](https://img.shields.io/github/repo-size/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![Bitbucket  issues](https://img.shields.io/github/issues-closed/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)

## 📒 Introduction

> :smiley: Push scheduled messages to DingTalk group chats using GitHub Actions (Python).

### ✨ Main Features

- 🤖 Message push based on DingTalk custom robots
- ⏰ Scheduled tasks using GitHub Actions, no server required
- 🌤️ Integration with AMAP (AutoNavi) Weather API, supports multiple cities
- 📝 Supports Markdown formatted messages with beautiful layout
- 💬 Daily quotes/inspirational messages
- 🔄 Complete error handling and fallback mechanisms
- 🆓 Completely free, no paid resources required

## 🚀 Quick Start

### Prerequisites

Before starting, you need to prepare:

1. A DingTalk account and a DingTalk group chat
2. A GitHub account
3. AMAP API key (free application)

### Step 1: Configure DingTalk Robot

#### 1.1 Create DingTalk Group Chat
Open DingTalk, click + to start a group chat (if you have a company account, you need two non-company friends to create a normal group). After creation, open the group chat settings and go to Smart Group Assistant.

#### 1.2 Add Custom Robot
Enter the robot management page, click Add Robot, enter the robot selection page, and select Custom Robot.

![Add Robot](https://img-blog.csdnimg.cn/16042ba005e94ae480a83dd9c65ea220.png)

#### 1.3 Configure Robot
You need to modify the robot's avatar and name. In the security settings, **it is recommended to check the custom keyword option**, for example, set the keyword as: **Good night**, then you can keep other settings as default. After clicking complete, you will see a webhook on the new page.

![Configure Robot](https://img-blog.csdnimg.cn/d03d721b6c20482d8b6517af8ec284a3.png)

#### 1.4 Save Webhook Address
After obtaining the Webhook address, you can send HTTP POST requests to this address to send messages to the DingTalk group.

**⚠️ Important Notes:**
- The Webhook address contains access_token, please keep it safe and do not leak it online
- Each robot can send up to 20 messages per minute
- Character encoding must be set to UTF-8

### Step 2: Apply for AMAP API Key

#### 2.1 Register AMAP Open Platform Account
Visit [AMAP Open Platform](https://lbs.amap.com/), register and login.

#### 2.2 Create Application
1. Enter the console, click "Application Management" -> "My Applications"
2. Click "Create New Application", fill in the application name and type
3. Add a Key under the application, select "Web Service" as the service platform
4. Save the generated Key (this is your AMAP_KEY)

> 💡 AMAP API provides a certain amount of free calls per day, which is sufficient for personal use

### Step 3: Configure GitHub Actions

#### 3.1 Fork or Clone This Project
Fork this project to your GitHub account, or clone and push to your own repository.

#### 3.2 Configure Secrets
In your repository, go to `Settings` -> `Secrets and variables` -> `Actions`, click `New repository secret` to add the following three Secrets:

| Secret Name | Description | Example |
|-----------|------|------|
| `TOKEN_DD` | access_token part from DingTalk robot Webhook | `abc123def456...` |
| `CITY` | City name or city code, supports multiple cities (separated by commas) | `Beijing` or `110000,310000` |
| `AMAP_KEY` | AMAP API key | `your_amap_key_here` |

**City Configuration Instructions:**
- Single city: Fill in the city name directly, such as `Beijing`, `Shanghai`, `Guangzhou`
- Multiple cities: Use city codes separated by commas, such as `110000,310000` (Beijing and Shanghai)
- City code query: [AMAP City Code Table](https://lbs.amap.com/api/webservice/guide/api/district)

#### 3.3 Configure Scheduled Tasks (Optional)

In the `.github/workflows/main.yml` file, you can modify the execution time of scheduled tasks:

```yaml
schedule:
  # UTC time 0:00, corresponding to Beijing time 8:00 AM
  - cron: '0 0 * * *'
```

**Common Time Configurations (cron expressions use UTC time):**
- `0 0 * * *` - Daily UTC 0:00 = Beijing time 8:00 AM
- `30 0 * * *` - Daily UTC 0:30 = Beijing time 8:30 AM
- `0 1 * * *` - Daily UTC 1:00 = Beijing time 9:00 AM
- `0 0 * * 1-5` - Monday to Friday UTC 0:00 = Beijing time 8:00 AM

> ⚠️ Note:
> - GitHub Actions cron expressions use UTC time, Beijing time = UTC time + 8 hours
> - Due to high concurrent tasks on GitHub Actions, actual execution time may be delayed by a few minutes

#### 3.4 Manual Trigger (Test)

In addition to scheduled execution, you can also manually trigger the workflow for testing on the GitHub Actions page:
1. Enter your repository
2. Click the `Actions` tab
3. Select the `morning` workflow
4. Click the `Run workflow` button
5. Check if the DingTalk group receives the message

## 📱 Message Effect

The program sends Markdown formatted messages to the DingTalk group, containing the following:

- 🌙 Good evening greeting
- 📍 Tomorrow's weather forecast for cities (supports multiple cities)
  - ☁️ Weather conditions
  - 🌡️ Real-time temperature
  - 💨 Wind direction and force
  - 💧 Air humidity
  - 🕐 Update time
- 💬 Daily quote/inspirational message

## 📚 DingTalk Robot Message Type Reference

This project uses Markdown format by default to send messages. DingTalk robots also support other message types. The following are detailed descriptions of each type:

### Supported Message Types

Currently, DingTalk robots support sending 5 types of messages:
1. **text** - Plain text message
2. **link** - Card message with links
3. **markdown** - Markdown formatted message (used by this project)
4. **ActionCard** - Interactive card message
5. **FeedCard** - Multiple link aggregation message

You need to choose based on your scenario to achieve the best display style.

Custom robots can specify "mentioned person list" by phone number when sending messages. People in the "mentioned person list" will receive @ message reminders. Do not disturb conversations will still notify, and "someone @you" will appear on the first screen.

#### Text Type

Text message type, specific code as follows:

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
        "content":"Test"
    },
    "msgtype":"text"
}
```

Parameter types involved in the above:

| **Parameter**  | **Parameter Type** | **Required** | **Description**                                                     |
| --------- | ------------ | ------------ | ------------------------------------------------------------ |
| msgtype   | String       | Yes           | Message type, fixed as: text.                                 |
| content   | String       | Yes           | Message content.                                                   |
| atMobiles | Array        | No           | Phone numbers of @mentioned people. **Note** Add @person's phone number in content, and only members in the group can be @mentioned, non-group member phone numbers will be desensitized. |
| atUserIds | Array        | No           | User IDs of @mentioned people. **Note** Add @person's userid in content.     |
| isAtAll   | Boolean      | No           | Whether to @everyone.                                                |

#### Link Type

Link message type, specific code as follows:

```json
{
    "msgtype": "link", 
    "link": {
        "text": "Test", 
        "title": "Test", 
        "picUrl": "", 
        "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
    }
}
```

Parameter types involved in the above:

| **Parameter**   | **Parameter Type** | Required | **Description**                                                     |
| ---------- | ------------ | -------- | ------------------------------------------------------------ |
| msgtype    | String       | Yes       | Message type, fixed as: link.                                 |
| title      | String       | Yes       | Message title.                                                   |
| text       | String       | Yes       | Message content. If too long, only part will be displayed.             |
| messageUrl | String       | Yes       | URL to jump to when clicking the message, opens as follows: Mobile, opens in DingTalk client, PC defaults to sidebar, for external browser, see [Message Link Description](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| picUrl     | String       | No       | Image URL.                                                    |

#### Markdown Type

Markdown message type, specific code as follows:

```json
{
     "msgtype": "markdown",
     "markdown": {
         "title":"Test",
         "text": "#### Hangzhou Weather @150XXXXXXXX \n > 9 degrees, northwest wind level 1, good air 89, relative humidity 73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### Published at 10:20 [Weather](https://www.dingtalk.com) \n"
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

Parameter types involved in the above:

| **Parameter**  | **Type** | Required | **Description**                                                     |
| --------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype   | String   | Yes       | Message type, fixed as: markdown.                             |
| title     | String   | Yes       | Display content on first screen conversation.                                     |
| text      | String   | Yes       | Markdown formatted message.                                         |
| atMobiles | Array    | No       | Phone numbers of @mentioned people. **Note** Must have @person's phone number in text content, only members in the group can be @mentioned, non-group member phone numbers will be desensitized. |
| atUserIds | Array    | No       | User IDs of @mentioned people. **Note** Add @person's userid in content.     |
| isAtAll   | Boolean  | No       | Whether to @everyone.                                                |



#### Overall Jump ActionCard Type

Overall jump ActionCard message type, specific code as follows:

```json
{
    "actionCard": {
        "title": "Test", 
        "text": "Test", 
        "btnOrientation": "0", 
        "singleTitle" : "Test",
        "singleURL" : "https://www.dingtalk.com/"
    }, 
    "msgtype": "actionCard"
}
```

Parameter types involved in the above:

| **Parameter**       | **Type** | **Required** | **Description**                                                     |
| -------------- | -------- | ------------ | ------------------------------------------------------------ |
| msgtype        | String   | Yes           | Message type, fixed as: actionCard.                           |
| title          | String   | Yes           | Display content on first screen conversation.                                     |
| text           | String   | Yes           | Markdown formatted message.                                         |
| singleTitle    | String   | Yes           | Title of single button. **Note** After setting this and singleURL, btns is invalid.   |
| singleURL      | String   | Yes           | URL to jump to when clicking the message, opens as follows: Mobile, opens in DingTalk client, PC defaults to sidebar, for external browser, see [Message Link Description](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | No           | 0: Buttons arranged vertically, 1: Buttons arranged horizontally                               |


#### Independent Jump ActionCard Type

Independent jump ActionCard message type, specific code as follows:

```json
{
    "msgtype": "actionCard",
    "actionCard": {
        "title": "Test", 
        "text": "Test", 
        "btnOrientation": "0", 
        "btns": [
            {
                "title": "Good content", 
                "actionURL": "https://www.dingtalk.com/"
            }, 
            {
                "title": "Not interested", 
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    }
}
```

Parameter types involved in the above:

| **Parameter**       | **Type** | Required | Description                                                         |
| -------------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype        | String   | Yes       | This message type is fixed as actionCard.                                 |
| title          | String   | Yes       | Display content on first screen conversation.                                     |
| text           | String   | Yes       | Markdown formatted message.                                         |
| btns           | Array    | Yes       | Buttons.                                                       |
| title          | String   | Yes       | Button title.                                                   |
| actionURL      | String   | Yes       | URL triggered by clicking the button, opens as follows: Mobile, opens in DingTalk client, PC defaults to sidebar, for external browser, see [Message Link Description](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az) |
| btnOrientation | String   | No       | 0: Buttons arranged vertically, 1: Buttons arranged horizontally                               |

#### FeedCard Type

FeedCard message type, specific code as follows:

```json
{
    "msgtype":"feedCard",
    "feedCard": {
        "links": [
            {
                "title": "Test1", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "Test2", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ]
    }
}
```

Parameter types involved in the above:

| **Parameter**   | **Type** | Required | **Description**                                                     |
| ---------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype    | String   | Yes       | This message type is fixed as feedCard.                                   |
| title      | String   | Yes       | Single message text.                                               |
| messageURL | String   | Yes       | Link to jump to when clicking single message. **Note** For how PC opens target page, see [Message link opens in PC sidebar or external browser](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az). |
| picURL     | String   | Yes       | URL of image behind single message.                                      |

## 🛠️ Technical Implementation

### Project Structure

```
.
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions workflow configuration
├── main.py                   # Main program file
├── requirements.txt          # Python dependency list
└── README.md                 # Project documentation
```

### Core Function Description

#### Weather API Integration

This project uses AMAP Weather API to get real-time weather information, advantages compared to other weather APIs:
- ✅ Stable and reliable, high service quality
- ✅ Sufficient free quota, enough for personal use
- ✅ Supports multiple cities simultaneous query
- ✅ Complete returned data (temperature, humidity, wind force, etc.)

#### Error Handling Mechanism

The code implements complete error handling:
- Network request timeout automatic retry
- Use default data when API call fails
- Does not interrupt program execution in exceptional situations
- All errors are logged for troubleshooting

#### Message Formatting

Use Markdown format to send messages, supports:
- Emoji enhances visual effects
- Clear hierarchical information organization
- Supports multi-city information display
- Automatic formatting of units (temperature, humidity, etc.)

## 🔧 FAQ

### Q1: Why are messages not sent on time?
**A:** GitHub Actions scheduled tasks may have 5-10 minutes delay due to many concurrent running tasks, this is normal.

### Q2: How to modify message content?
**A:** Edit the message template part in the `main.py` file to customize message format and content.

### Q3: How many cities can be queried simultaneously?
**A:** Theoretically no limit, but recommend not exceeding 5 cities to maintain message readability.

### Q4: How to replace the daily quote API?
**A:** Modify the API address in the `get_words()` function, ensure the return format is compatible.

### Q5: Can I change the sending time?
**A:** Yes, modify the cron expression in `.github/workflows/main.yml`. Note to use UTC time.

### Q6: What happens if Secrets are configured incorrectly?
**A:** GitHub Actions will fail to execute, you can view detailed error logs on the Actions page.

## 📝 Changelog

### Latest Version Features

- ✅ Integrated AMAP Weather API, more accurate data
- ✅ Supports multi-city weather query
- ✅ Optimized Markdown message format, added emoji
- ✅ Improved error handling and fallback mechanisms
- ✅ Automatic formatting of weather data units
- ✅ Supports manual workflow trigger

## 🤝 Project Repository

[GitHub Repository](https://github.com/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly)

## ☕ Acknowledgments

Thanks to the following references:

- [https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
- [https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions)
- [https://lbs.amap.com/api/webservice/guide/api/weatherinfo](https://lbs.amap.com/api/webservice/guide/api/weatherinfo)
- [https://open.dingtalk.com/document/robots/custom-robot-access](https://open.dingtalk.com/document/robots/custom-robot-access)

> All are internet materials, please contact for deletion if infringement occurs. Issues can be raised by clicking Issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If this project is helpful to you, please Star to support!
