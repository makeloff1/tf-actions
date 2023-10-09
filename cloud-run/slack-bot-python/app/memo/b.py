# 1.プルダウンメニューに typeahead の min_query_length プロパティを設定します。
# 2.ユーザーがプルダウンメニューで入力すると、action_id がトリガーされ、
#   アプリはユーザーの入力に基づいてチャンネルリストをフィルタリングします。
# 3.フィルタリングされた結果をプルダウンメニューのオプションとして再度表示します。

# この変更により、ユーザーがプルダウンメニューに文字を入力すると、その入力に基づいて
# チャンネルがフィルタリングされ、プルダウンメニューのオプションが更新されます。
# 入力が min_query_length で指定した文字数以上であることが要件です。
# このコードを使用することで、ユーザーが入力した文字でチャンネルをフィルタリングする
# 機能を実装できます。


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
                        "options": [],
                        "typeahead": {"min_query_length": 1},  # 1文字以上の入力が必要
                    },
                    "label": {"type": "plain_text", "text": "チャンネル選択"},
                }
            ],
            "submit": {"type": "plain_text", "text": "送信"},
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


# ...
