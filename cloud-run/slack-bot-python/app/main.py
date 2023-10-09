import os
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


# チャンネルに属するユーザー一覧を非同期で取得する関数
async def get_users_in_channel(channel_id):
    response = await slack_client.conversations_members(channel=channel_id)
    user_ids = response["members"]
    users = []

    for user_id in user_ids:
        user_info = await slack_client.users_info(user=user_id)
        users.append(user_info["user"])

    return users


# ショートカットアクションを処理するリスナーを設定します
@app.shortcut("your_shortcut_id")  # ショートカットIDを設定してください
async def open_modal(ack, shortcut, client):
    ack()

    # チャンネル一覧を非同期で取得します
    _ = await get_channel_list()

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
                        "options": [],
                        "typeahead": {"min_query_length": 1},  # 1文字以上の入力が必要
                    },
                    "label": {"type": "plain_text", "text": "チャンネル選択"},
                }
            ],
            "submit": {"type": "plain_text", "text": "CSVダウンロードリンク生成"},
        },
    )


# プルダウンメニューのオプションをフィルタリングして更新します
@app.options("selected_channel")
async def filter_channel_options(ack, body, client):
    query = body["value"]  # ユーザーが入力した文字列を取得します

    # チャンネル一覧を非同期で取得します
    channels = await get_channel_list()

    # 入力に基づいてチャンネルをフィルタリングします
    filtered_channels = [
        channel for channel in channels if query.lower() in channel["name"].lower()
    ]

    # フィルタリングされた結果をプルダウンメニューのオプションとして返します
    options = [
        {
            "text": {"type": "plain_text", "text": channel["name"]},
            "value": channel["id"],
        }
        for channel in filtered_channels
    ]

    ack(options)


# モーダル内でユーザーが送信ボタンをクリックしたときの処理
@app.view("channel_selection")
async def handle_modal_submission(ack, body, client):
    ack()
    selected_channel_id = body["view"]["state"]["values"]["channel_select"][
        "selected_option"
    ]["value"]

    # 選択されたチャンネルIDを使用してユーザー一覧を非同期で取得します
    users = await get_users_in_channel(selected_channel_id)

    # ユーザー一覧をCSV形式に整形します
    csv_content = "User ID,Username\n"  # CSVヘッダー

    for user in users:
        csv_content += f"{user['id']},{user['name']}\n"  # ユーザー情報をCSV行として追加

    # CSVデータを一時ファイルに書き込みます
    with open("user_list.csv", "w") as csv_file:
        csv_file.write(csv_content)

    # ダウンロードリンクを生成し、ユーザーに提供します
    download_link = (
        "https://your-app-url.com/download/user_list.csv"  # アプリのURLに適切なものを設定
    )
    client.chat_postMessage(
        channel=body["user"]["id"],  # ユーザーに直接メッセージを送信
        text=f"ユーザー一覧CSVをダウンロード: {download_link}",
    )


# アプリケーションをSocket Modeハンドラーとして起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
