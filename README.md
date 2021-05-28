# slackbot
slackbot for DNN training alarm  

## Install 
1. install Slack's SDK
```terminal
$ pip install slack_sdk
```
2. modify values of `'author_icon'`, `footer` and `'footer_icon'` in `slackbot.py`

## Path
author_name = `알림 - [PROJECT_NAME]`  
title = `[PROJECT_NAME]/[SUB] - 학습 중`

```
work
 ├── project_1
 │   ├── sub_1 
 │   │   ├── train.py
 │   │   └── ...
 │   └── ...
 ├── project_2
 │   ├── sub_1
 │   └── ...
 └── project_3
     ├── sub_1
     └── ...
```

## Use
### init slackbot
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

###  on training
```python
...
# epochs = 10
metrics_dict = {'Acc':0.15, 'mAP': 0.12, 'loss':1.221, ... }
info = slacker.get_info(epochs, metrics_dict)
slacker.send(channel_name, info)

...
```
![sample1](img/sample_1.png)

### error occured
```python
# epochs = 50
try:
    ...
except BaseException as e:
    metrics_dict = {'Acc':0.38, 'mAP': 0.32, 'loss':0.821, ... }
    info = slacker.get_info(epochs, metrics_dict, error=e)
    slacker.send(channel_name, info)
```
![sample2](img/sample_2.png)

### training end
```python
...
# epochs = 100
metrics_dict = {'Acc':0.78, 'mAP': 0.72, 'loss':0.421, ... }
info = slacker.get_info(epochs, metrics_dict, endTrain=True)
slacker.send(channel_name, info)
```
![sample3](img/sample_3.png)
