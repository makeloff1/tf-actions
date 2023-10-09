import os
import logging

# Import Bolt for Python (github.com/slackapi/bolt-python)
# from slack_bolt import App, Ack, Say, BoltContext
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.basicConfig(level=logging.DEBUG)

# Initializes your Bolt app with a bot token and signing secret
app = App(token="xoxb-your-token", signing_secret="your-signing-secret")


@app.shortcut("open_modal")
def open_modal(ack, shortcut, client, logger):
    # Acknowledge shortcut request
    ack()

    try:
        # Call the views.open method using the WebClient passed to listeners
        result = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "My App"},
                "close": {"type": "plain_text", "text": "Close"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/block-elements|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>.",
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>",
                            }
                        ],
                    },
                ],
            },
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


# echoコマンドは受け取ったコマンドをそのまま返す
@app.command("/invite")
def repeat_text(ack, respond, command):
    # command リクエストを確認
    ack()
    respond(f"{command['text']}")


# 応答用
def ack(ack, body):
    ack()


# 登録されているチャンネル一覧を返す関数
def show_puldown_channel_list(body: dict, client: WebClient) -> None:
    # ログインユーザID？
    user_id = body["user"]["id"]

    channel_list = get_channel_list()
    send_message = format_template_list(channel_list)

    client.files_upload(
        channels=os.environ["SLACK_CHANNEL"],
        content=send_message,
        filename=f"{datetime.now().strftime('%Y%m%d%H%M%S')}_RTMテンプレート一覧.tsv",
        filetype="tsv",
        initial_comment=comment,
    )


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
