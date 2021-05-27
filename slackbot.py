from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import sys
from pathlib import Path
import time


class slackAlarm():

    def __init__(self, token, dict_hyper, url=None, memo=None):
        self.SLACK_BOT_TOKEN = token
        self.client = WebClient(token=self.SLACK_BOT_TOKEN)
        self.newline = '\n'

        self.start_time = time.time()
        self.command = f"python {' '.join(sys.argv)}"
        self.path = str(Path(__file__).parent.absolute()).split('/')

        self.url = url
        self.hyper_str = self.dict_to_str(dict_hyper)
        self.memo = memo


    def dict_to_str(self, dict_data):
        return ' '.join([f"{self.newline if idx%2==0 else ''}`{k}` : {v} " for idx, (k, v) in enumerate(dict_data.items())])


    def get_info(self, dict_metrics = None, error = None, endTrain=False):
        work = self.path[-2]
        sub_work = '/'.join(self.path[-2:])
        cur_time = time.time()

        metrics_str = ''
        if dict_metrics is not None:
            metrics_str = self.dict_to_str(dict_metrics)

        attachments = [
            {
                "pretext": f"{time.ctime(self.start_time)}\nMemo : {self.memo}", # text in message 
                "mrkdwn_in": ["text"],
                "color": "#FA9547",  # bar color

                # in block 
                "author_name": f"알림 - {work}",
                # "author_link": "",
                "author_icon": "https://avatars.githubusercontent.com/u/33483699?s=60&v=4",
                "title": f"{sub_work} {'에러 발생' if error is not None else '학습 중' if not endTrain else '학습 종료'}",
                "title_link": self.url,

                "fields" : [
                    {
                        "title": "Hyperparameter",
                        "value": self.hyper_str,
                        "short": True
                    },
                    {
                        "title": "Metrics",
                        "value": metrics_str,
                        "short": True
                    },
                    {
                        "title": "Command",
                        "value": f"`{self.command}`",
                        "short": False
                    }
                ],

                # "text": "",
                "footer": "RTX8000",
                "footer_icon": "https://www.google.com/s2/favicons?domain=sites.google.com/view/kvl",
                "ts": cur_time
            }
        ]

        if error is not None:
            error_block = {
                        "title": "Error",
                        "value": f"{type(error).__name__} : {str(error)}",
                        "short": False
                    }
            attachments[0]["fields"].append(error_block)

        return attachments

    def send(self, channel_name, attachments):
        try:
            response = self.client.chat_postMessage(channel=f'#{channel_name}', attachments=attachments, fallback=None)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")