# slackbot
slackbot for DNN training alarm  
modify values of `'author_icon'` and `'footer_icon'` in `slackbot.py`

## init slackbot
```python
...

from slackbot import slackAlarm

# for init
token = '[YOUR_SLACK_OAUTH_TOKEN]'
hyper_dict = {'epoch': 100, 'batch_size' : 16, 'lr': 0.001, ... }
url = '[RELATED_URL]'
memo = '[WRITE_SOMETHING]'
channel_name = 'general'

# create instance
slackbot = slackAlarm(token, hyper_dict, url=url, memo=memo)

...
```

##  on training
```python
...

metrics_dict = {'Acc':0.15, 'mAP': 0.12, 'loss':1.221, ... }
info = slacker.get_info(metrics_dict)
slacker.send(channel_name, info)

...
```
## error occured
```python
try:
    ...
except BaseException as e:
    info = slacker.get_info(metrics_dict, error=e)
    slacker.send(channel_name, info)
```

## training end
```python
...

info = slacker.get_info(metrics_dict, endTrain=True)
slacker.send(channel_name, info)
```
