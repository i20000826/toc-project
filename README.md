# TOC Project 2020

## Setup

### Prerequisite
* Python 3.6
* anaconda
* HTTPS Server(ngrok/Heroku)

#### Install Dependency
```
conda install -c conda-forge pygraphviz

pip install flask python-dotenv line-bot-sdk transitions pygraphviz
```

#### Run on ngrok
```
ngrok http 8000
```

#### Execute
```
python app.py
```

## Finite State Machine
![fsm](./fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation
* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login
	```
	heroku login
	```

### Upload project to Heroku

1. Add local project to Heroku project
	```
	heroku git:remote -a {HEROKU_APP_NAME}
	```
	
2. If fail with `pygraphviz` install errors
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```
	
3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

5. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`


	
