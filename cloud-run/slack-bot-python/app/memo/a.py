# チャンネル一覧を非同期で取得するには、Pythonの非同期ライブラリasyncioを
# 使用して非同期関数を定義し、Slack API呼び出しをawaitキーワードで実行することが
# 必要です。以下は、チャンネル一覧を非同期で取得するコードの一例です。

# このコードでは、async defを使用して非同期関数を定義し、awaitを使用して
# Slack API呼び出しを非同期で実行しています。get_channel_list関数でチャンネル一覧を
# 非同期で取得し、プルダウンメニューのオプションを生成する際に使用しています。
# このようにすることで、コードは非同期で効率的に動作し、チャンネル一覧の取得を
# 待たずにモーダルを表示できます。

import os
import asyncio
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Slack Boltアプリケーションを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

# Slack WebClientを初期化します
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


# チャンネル一覧を非同期で取得する関数を定義します
async def get_channel_list():
    response = await slack_client.conversations_list()
    channels = response["channels"]
    return channels


# ショートカットアクションを処理するリスナーを設定します
@app.shortcut("your_shortcut_id")  # ショートカットIDを設定してください
async def open_modal(ack, shortcut, client):
    ack()

    # チャンネル一覧を非同期で取得します
    channels = await get_channel_list()

    # モーダルを表示するアクションを実行します
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "channel_selection",
            "title": {"type": "plain_text", "text": "チャンネルを選択してください"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "channel_select",
                    "element": {
                        "type": "static_select",
                        "action_id": "selected_channel",
                        "placeholder": {"type": "plain_text", "text": "チャンネルを選択"},
                        # チャンネル一覧からプルダウンメニューのオプションを生成します
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": channel["name"]},
                                "value": channel["id"],
                            }
                            for channel in channels
                        ],
                    },
                    "label": {"type": "plain_text", "text": "チャンネル選択"},
                }
            ],
            "submit": {"type": "plain_text", "text": "送信"},
        },
    )


# モーダル内でユーザーが選択したチャンネルを処理するリスナーを設定します
@app.view("channel_selection")
async def handle_modal_submission(ack, body, client):
    ack()
    selected_channel = body["view"]["state"]["values"]["channel_select"][
        "selected_option"
    ]["value"]
    # 選択されたチャンネルにメッセージを送信するなどのアクションを実行します
    await slack_client.chat_postMessage(
        channel=selected_channel, text="選択されたチャンネルにメッセージを送信します"
    )


# アプリケーションをSocket Modeハンドラーとして起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
