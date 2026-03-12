# DingTalk グループチャットロボット - スケジュールメッセージプッシュ

**Language/语言**: [English](README.md) | [日本語](README_JP.md) | [中文](README_CN.md)

![GitHub repo size](https://img.shields.io/github/repo-size/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)
![Bitbucket  issues](https://img.shields.io/github/issues-closed/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly?style=for-the-badge)

## 📒 紹介

> :smiley: GitHub Actions を使用して DingTalk グループチャットに定期的にメッセージをプッシュします (Python)。

### ✨ 主な機能

- 🤖 DingTalk カスタムロボットに基づくメッセージプッシュ
- ⏰ GitHub Actions を使用したスケジュールタスク、サーバー不要
- 🌤️ AMAP (AutoNavi) 天気 API との統合、複数都市対応
- 📝 Markdown 形式のメッセージをサポート、美しいレイアウト
- 💬 毎日の名言/インスピレーションメッセージ
- 🔄 完全なエラー処理とフォールバック機能
- 🆓 完全無料、有料リソース不要

## 🚀 クイックスタート

### 準備

開始する前に、以下を準備してください：

1. DingTalk アカウントと DingTalk グループチャット
2. GitHub アカウント
3. AMAP API キー（無料で申請可能）

### ステップ 1: DingTalk ロボットの設定

#### 1.1 DingTalk グループチャットの作成
DingTalk を開き、+ をクリックしてグループチャットを開始します（会社アカウントがある場合、通常のグループを作成するには会社以外の友達が 2 人必要です）。作成後、グループチャット設定を開き、スマートグループアシスタントに移動します。

#### 1.2 カスタムロボットの追加
ロボット管理ページに入り、ロボットの追加をクリックし、ロボット選択ページに入り、カスタムロボットを選択します。

![ロボットの追加](https://img-blog.csdnimg.cn/16042ba005e94ae480a83dd9c65ea220.png)

#### 1.3 ロボットの設定
ロボットのアバターと名前を変更する必要があります。セキュリティ設定で、**カスタムキーワードオプションをチェックすることをお勧めします**。たとえば、キーワードを **おやすみなさい** に設定し、他の設定はデフォルトのままにします。完了をクリックすると、新しいページに webhook が表示されます。

![ロボットの設定](https://img-blog.csdnimg.cn/d03d721b6c20482d8b6517af8ec284a3.png)

#### 1.4 Webhook アドレスの保存
Webhook アドレスを取得したら、このアドレスに HTTP POST リクエストを送信して、DingTalk グループにメッセージを送信できます。

**⚠️ 重要な注意事項:**
- Webhook アドレスには access_token が含まれています。安全に保管し、オンラインで漏洩しないでください
- 各ロボットは 1 分間に最大 20 メッセージを送信できます
- 文字エンコーディングは UTF-8 に設定する必要があります

### ステップ 2: AMAP API キーの申請

#### 2.1 AMAP オープンプラットフォームアカウントの登録
[AMAP オープンプラットフォーム](https://lbs.amap.com/)にアクセスし、登録してログインします。

#### 2.2 アプリケーションの作成
1. コンソールに入り、「アプリケーション管理」 -> 「マイアプリケーション」をクリック
2. 「新しいアプリケーションを作成」をクリックし、アプリケーション名とタイプを入力
3. アプリケーション下で Key を追加し、サービスプラットフォームとして「Web サービス」を選択
4. 生成された Key を保存します（これが AMAP_KEY です）

> 💡 AMAP API は毎日一定の無料通話量を提供しており、個人使用には十分です

### ステップ 3: GitHub Actions の設定

#### 3.1 このプロジェクトを Fork またはクローン
このプロジェクトを GitHub アカウントに Fork するか、クローンして自分のリポジトリにプッシュします。

#### 3.2 Secrets の設定
リポジトリで `Settings` -> `Secrets and variables` -> `Actions` に移動し、`New repository secret` をクリックして以下の 3 つの Secret を追加します：

| Secret 名 | 説明 | 例 |
|-----------|------|------|
| `TOKEN_DD` | DingTalk ロボット Webhook の access_token 部分 | `abc123def456...` |
| `CITY` | 都市名または都市コード、複数の都市をサポート（カンマ区切り） | `北京` または `110000,310000` |
| `AMAP_KEY` | AMAP API キー | `your_amap_key_here` |

**都市設定の説明:**
- 単一都市：都市名を直接入力、例：`北京`、`上海`、`広州`
- 複数都市：都市コードをカンマで区切って使用、例：`110000,310000`（北京と上海）
- 都市コード検索：[AMAP 都市コード表](https://lbs.amap.com/api/webservice/guide/api/district)

#### 3.3 スケジュールタスクの設定（オプション）

`.github/workflows/main.yml` ファイルで、スケジュールタスクの実行時間を変更できます：

```yaml
schedule:
  # UTC 時間 0:00、北京時間 8:00 AM に相当
  - cron: '0 0 * * *'
```

**一般的な時間設定（cron 式は UTC 時間を使用）:**
- `0 0 * * *` - 毎日 UTC 0:00 = 北京時間 8:00 AM
- `30 0 * * *` - 毎日 UTC 0:30 = 北京時間 8:30 AM
- `0 1 * * *` - 毎日 UTC 1:00 = 北京時間 9:00 AM
- `0 0 * * 1-5` - 月曜日から金曜日 UTC 0:00 = 北京時間 8:00 AM

> ⚠️ 注意:
> - GitHub Actions の cron 式は UTC 時間を使用、北京時間 = UTC 時間 + 8 時間
> - GitHub Actions の同時タスクが多いため、実際の実行時間は数分遅れる可能性があります

#### 3.4 手動トリガー（テスト）

スケジュール実行に加えて、GitHub Actions ページでワークフローを手動でトリガーしてテストすることもできます：
1. リポジトリに入る
2. `Actions` タブをクリック
3. `morning` ワークフローを選択
4. `Run workflow` ボタンをクリック
5. DingTalk グループがメッセージを受信したか確認

## 📱 メッセージ効果

プログラムは Markdown 形式のメッセージを DingTalk グループに送信します。以下の内容を含みます：

- 🌅 おやすみなさいの挨拶
- 📍 都市の天気情報（複数都市対応）
  - ☁️ 天気状況
  - 🌡️ リアルタイム温度
  - 💨 風向と風力
  - 💧 空気湿度
  - 🕐 更新時間
- 💬 毎日の名言/インスピレーションメッセージ

## 📚 DingTalk ロボットメッセージタイプリファレンス

このプロジェクトは、デフォルトで Markdown 形式を使用してメッセージを送信します。DingTalk ロボットは他のメッセージタイプもサポートしています。以下は各タイプの詳細説明です：

### サポートされているメッセージタイプ

現在、DingTalk ロボットは 5 種類のメッセージ送信をサポートしています：
1. **text** - プレーンテキストメッセージ
2. **link** - リンク付きカードメッセージ
3. **markdown** - Markdown 形式のメッセージ（このプロジェクトで使用）
4. **ActionCard** - インタラクティブカードメッセージ
5. **FeedCard** - 複数リンク集約メッセージ

シナリオに応じて選択し、最適な表示スタイルを実現する必要があります。

カスタムロボットがメッセージを送信する際、電話番号で「メンション対象リスト」を指定できます。「メンション対象リスト」の人は @ メッセージ通知を受け取ります。邪魔しないモードの会話でも通知され、最初の画面に「誰かが@しました」が表示されます。

#### Text タイプ

テキストメッセージタイプ、具体的なコードは以下の通りです：

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
        "content":"テスト"
    },
    "msgtype":"text"
}
```

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**  | **パラメータタイプ** | **必須** | **説明**                                                     |
| --------- | ------------ | ------------ | ------------------------------------------------------------ |
| msgtype   | String       | はい           | メッセージタイプ、固定値：text                                 |
| content   | String       | はい           | メッセージ内容                                                   |
| atMobiles | Array        | いいえ           | @メンション対象の電話番号。**注意** content に@対象の電話番号を追加し、グループ内のメンバーのみ@可能、グループ外のメンバーの電話番号は脱感作されます |
| atUserIds | Array        | いいえ           | @メンション対象のユーザー userid。**注意** content に@対象の userid を追加     |
| isAtAll   | Boolean      | いいえ           | 全員に@するか                                                |

#### Link タイプ

リンクメッセージタイプ、具体的なコードは以下の通りです：

```json
{
    "msgtype": "link", 
    "link": {
        "text": "テスト", 
        "title": "テスト", 
        "picUrl": "", 
        "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
    }
}
```

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**   | **パラメータタイプ** | 必須 | **説明**                                                     |
| ---------- | ------------ | -------- | ------------------------------------------------------------ |
| msgtype    | String       | はい       | メッセージタイプ、固定値：link                                 |
| title      | String       | はい       | メッセージタイトル                                                   |
| text       | String       | はい       | メッセージ内容。長すぎる場合は一部のみ表示されます             |
| messageUrl | String       | はい       | メッセージをクリックしたときにジャンプする URL、開き方は以下の通り：モバイル、DingTalk クライアント内で開く、PC はデフォルトでサイドバーで開く、外部ブラウザで開く場合は[メッセージリンク説明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)を参照 |
| picUrl     | String       | いいえ       | 画像 URL                                                    |

#### Markdown タイプ

Markdown メッセージタイプ、具体的なコードは以下の通りです：

```json
{
     "msgtype": "markdown",
     "markdown": {
         "title":"テスト",
         "text": "#### 杭州の天気 @150XXXXXXXX \n > 9度、北西風レベル1、良好な空気89、相対湿度73%\n > ![スクリーンショット](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10:20 に公開 [天気](https://www.dingtalk.com) \n"
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

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**  | **タイプ** | 必須 | **説明**                                                     |
| --------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype   | String   | はい       | メッセージタイプ、固定値：markdown                             |
| title     | String   | はい       | 最初の画面の会話に表示される内容                                     |
| text      | String   | はい       | Markdown 形式のメッセージ                                         |
| atMobiles | Array    | いいえ       | @メンション対象の電話番号。**注意** text 内容に@対象の電話番号が必要、グループ内のメンバーのみ@可能、グループ外のメンバーの電話番号は脱感作されます |
| atUserIds | Array    | いいえ       | @メンション対象のユーザー userid。**注意** content に@対象の userid を追加     |
| isAtAll   | Boolean  | いいえ       | 全員に@するか                                                |



#### 全体ジャンプ ActionCard タイプ

全体ジャンプ ActionCard メッセージタイプ、具体的なコードは以下の通りです：

```json
{
    "actionCard": {
        "title": "テスト", 
        "text": "テスト", 
        "btnOrientation": "0", 
        "singleTitle" : "テスト",
        "singleURL" : "https://www.dingtalk.com/"
    }, 
    "msgtype": "actionCard"
}
```

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**       | **タイプ** | **必須** | **説明**                                                     |
| -------------- | -------- | ------------ | ------------------------------------------------------------ |
| msgtype        | String   | はい           | メッセージタイプ、固定値：actionCard                           |
| title          | String   | はい           | 最初の画面の会話に表示される内容                                     |
| text           | String   | はい           | Markdown 形式のメッセージ                                         |
| singleTitle    | String   | はい           | 単一ボタンのタイトル。**注意** これと singleURL を設定すると、btns は無効になります   |
| singleURL      | String   | はい           | メッセージをクリックしたときにジャンプする URL、開き方は以下の通り：モバイル、DingTalk クライアント内で開く、PC はデフォルトでサイドバーで開く、外部ブラウザで開く場合は[メッセージリンク説明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)を参照 |
| btnOrientation | String   | いいえ           | 0：ボタンを縦に配置、1：ボタンを横に配置                               |


#### 独立ジャンプ ActionCard タイプ

独立ジャンプ ActionCard メッセージタイプ、具体的なコードは以下の通りです：

```json
{
    "msgtype": "actionCard",
    "actionCard": {
        "title": "テスト", 
        "text": "テスト", 
        "btnOrientation": "0", 
        "btns": [
            {
                "title": "良いコンテンツ", 
                "actionURL": "https://www.dingtalk.com/"
            }, 
            {
                "title": "興味なし", 
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    }
}
```

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**       | **タイプ** | 必須 | 説明                                                         |
| -------------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype        | String   | はい       | このメッセージタイプは固定値 actionCard                                 |
| title          | String   | はい       | 最初の画面の会話に表示される内容                                     |
| text           | String   | はい       | Markdown 形式のメッセージ                                         |
| btns           | Array    | はい       | ボタン                                                       |
| title          | String   | はい       | ボタンのタイトル                                                   |
| actionURL      | String   | はい       | ボタンをクリックしたときにトリガーされる URL、開き方は以下の通り：モバイル、DingTalk クライアント内で開く、PC はデフォルトでサイドバーで開く、外部ブラウザで開く場合は[メッセージリンク説明](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)を参照 |
| btnOrientation | String   | いいえ       | 0：ボタンを縦に配置、1：ボタンを横に配置                               |

#### FeedCard タイプ

FeedCard メッセージタイプ、具体的なコードは以下の通りです：

```json
{
    "msgtype":"feedCard",
    "feedCard": {
        "links": [
            {
                "title": "テスト1", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "テスト2", 
                "messageURL": "https://www.dingtalk.com/", 
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ]
    }
}
```

上記に含まれるパラメータタイプは以下の通りです：

| **パラメータ**   | **タイプ** | 必須 | **説明**                                                     |
| ---------- | -------- | -------- | ------------------------------------------------------------ |
| msgtype    | String   | はい       | このメッセージタイプは固定値 feedCard                                   |
| title      | String   | はい       | 単一メッセージのテキスト                                               |
| messageURL | String   | はい       | 単一メッセージをクリックしたときにジャンプするリンク。**注意** PC がターゲットページを開く方法については、[メッセージリンクが PC サイドバーまたは外部ブラウザで開く](https://open.dingtalk.com/document/app/message-link-description#section-7w8-4c2-9az)を参照 |
| picURL     | String   | はい       | 単一メッセージの後ろの画像の URL                                      |

## 🛠️ 技術実装

### プロジェクト構造

```
.
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions ワークフロー設定
├── main.py                   # メインプログラムファイル
├── requirements.txt          # Python 依存関係リスト
└── README.md                 # プロジェクトドキュメント
```

### コア機能の説明

#### 天気 API 統合

このプロジェクトは AMAP 天気 API を使用してリアルタイム天気情報を取得します。他の天気 API と比較した利点：
- ✅ 安定性と信頼性、高いサービス品質
- ✅ 十分な無料割り当て、個人使用に十分
- ✅ 複数都市の同時クエリをサポート
- ✅ 完全な返却データ（温度、湿度、風力など）

#### エラー処理機構

コードは完全なエラー処理を実装しています：
- ネットワークリクエストのタイムアウト時の自動再試行
- API 呼び出し失敗時にデフォルトデータを使用
- 例外的な状況でプログラムの実行を中断しない
- すべてのエラーはトラブルシューティングのためにログに記録されます

#### メッセージフォーマット

Markdown 形式を使用してメッセージを送信し、サポート：
- 絵文字が視覚効果を向上
- 明確な階層的情報組織
- 複数都市情報の表示をサポート
- 単位の自動フォーマット（温度、湿度など）

## 🔧 よくある質問

### Q1: メッセージが時間通りに送信されないのはなぜですか？
**A:** GitHub Actions のスケジュールタスクは、同時実行タスクが多いため、5〜10 分の遅延が発生する可能性があります。これは正常です。

### Q2: メッセージ内容を変更するにはどうすればよいですか？
**A:** `main.py` ファイルのメッセージテンプレート部分を編集して、メッセージ形式と内容をカスタマイズできます。

### Q3: 同時にクエリできる都市はいくつですか？
**A:** 理論的には制限はありませんが、メッセージの読みやすさを維持するために 5 都市以下を推奨します。

### Q4: 毎日の名言 API を置き換えるにはどうすればよいですか？
**A:** `get_words()` 関数の API アドレスを変更し、返却形式が互換性があることを確認してください。

### Q5: 送信時間を変更できますか？
**A:** はい、`.github/workflows/main.yml` の cron 式を変更してください。UTC 時間を使用することに注意してください。

### Q6: Secrets が正しく設定されていない場合はどうなりますか？
**A:** GitHub Actions は実行に失敗します。Actions ページで詳細なエラーログを確認できます。

## 📝 変更ログ

### 最新バージョンの機能

- ✅ AMAP 天気 API を統合、より正確なデータ
- ✅ 複数都市の天気クエリをサポート
- ✅ Markdown メッセージ形式を最適化、絵文字を追加
- ✅ エラー処理とフォールバック機構を改善
- ✅ 天気データ単位の自動フォーマット
- ✅ 手動ワークフロートリガーをサポート

## 🤝 プロジェクトリポジトリ

[GitHub リポジトリ](https://github.com/liwei6677/Dingding-group-chat-robot-pushes-messages-regularly)

## ☕ 謝辞

以下の参考資料に感謝します：

- [https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
- [https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions)
- [https://lbs.amap.com/api/webservice/guide/api/weatherinfo](https://lbs.amap.com/api/webservice/guide/api/weatherinfo)
- [https://open.dingtalk.com/document/robots/custom-robot-access](https://open.dingtalk.com/document/robots/custom-robot-access)

> すべてインターネット資料です。侵害がある場合は削除のためにご連絡ください。質問がある場合は Issues をクリックしてください。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細については [LICENSE](LICENSE) ファイルを参照してください。

---

⭐ このプロジェクトがお役に立った場合は、Star でサポートしてください！
