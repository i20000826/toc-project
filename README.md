# Line聊天機器人 -- 哈利波特:魔法覺醒 攻略

## 環境
* windows
* anaconda
* Python 3.6
* ngrok/Heroku

## 設定

### 安裝相關套件

#### anaconda
```
conda install -c conda-forge pygraphviz

pip install flask python-dotenv line-bot-sdk transitions pygraphviz
```

#### ngrok
下載ngrok <br>
在ngrok輸入: `ngrok http 8000` <br>
在terminal執行: `python app.py` <br>

#### Heroku
下載Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli <br>
註冊Heroku帳號: https://signup.heroku.com <br>
在Heroku網站Create new app <br>
在terminal登入Heroku CLI: `heroku login` <br>
如果無法辨識heroku: `set PATH=%PATH%;C:\Program Files\heroku\bin`(heroku路徑) <br>
設定line環境
```
heroku config:set LINE_CHANNEL_SECRET=[YOUR_LINE_CHANNEL_SECRET]

heroku config:set LINE_CHANNEL_ACCESS_TOKEN=[YOUR_LINE_CHANNEL_ACCESS_TOKEN]
```
放上Heroku
```
heroku git:remote -a [HEROKU_APP_NAME]

git add .

git commit -m "Add code"

git push -f heroku master
```
如果push時顯示pygraphviz安裝失敗
```
heroku buildpacks:set heroku/python

heroku buildpacks:add --index 1 heroku-community/apt
```
在line的webhook url輸入: `[HEROKU_APP_NAME].herokuapp.com/webhook` <br>
debug輸入: `heroku logs --tail --app [HEROKU_APP_NAME]` <br>

## Finite State Machine
![fsm](./fsm.png)

## 實作
起因: 每次都要上網查攻略很麻煩, 而且有些~壞傢伙提供的~攻略資訊有誤, 於是透過本次作業將正確的攻略整合在一起, 方便查詢!

初始state為"user" <br>
"user"可以去到"achievement", "furniture", "divination_1", "forbidden_forest_1", "menu" <br>
隨時都可以輸入「fsm」「主選單」

### achievement 神秘成就

### furniture 大世界收集

### divination 占卜學圖鑑
~幸好在project deadline前成功解完, 我好好看~

### forbidden_forest 禁忌森林



Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"


