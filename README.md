# Regex (Source Code)
> This bot was made for handling tags for the **[BytesToBits](https://discord.gg/u4qdg3EM8J)** Discord server.

## How to setup
1. Clone the repository
2. Create an `enums.py` file inside the `core` folder.
3. Edit the file and fill in the following values:
```py
from typing import ClassVar

class Bot:
    TOKEN: ClassVar[str] = "your-bot-token"
    DEV_TOKEN: ClassVar[str] = "test-bot-token" # (OPTIONAL TO RUN WITH THE DEV FLAG)
    GUILDS: ClassVar[str] = [1234] # the server IDs to register slash commands
    MONGO_URI: ClassVar[str] = "mongo-uri" # the mongo DB URI, view below for how to create a free mongo DB
```
4. Do the following commands:
- Install poetry dependencies
```
poetry install
```
- Run the project
```
poetry run python3 main.py
```
- Alternatively, if you want to run the bot with the `DEV_TOKEN`
```
poetry run python3 main.py --dev
```

## Preparing the Database
You can get a free **500MB** Database from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). That will last for a really long time.

Head over to Atlas and create a new account. You will then be greeted with this panel.
![Panel View](https://user-images.githubusercontent.com/44692189/64170897-1297a600-ce73-11e9-910e-38b78c3ac315.jpg)

Select the `FREE` one and give it a name. Follow these steps;
- Go to `Database Access` section under the `Security` tab and click `+ ADD NEW USER`. Give it `Read and write to any database` permissions so the bot can properly store the data. Give it a username and a **secure** password. Save the password only.
![New User](https://i.imgur.com/zfhxyNX.png)
- To allow the bot to actually access the database, you should whitelist all IP's. Go to `Network Access` section under the `Security` tab and click `+ ADD IP ADDRESS`. Click the `Allow Access From Everywhere` and `0.0.0.0/0` should appear in the `Whitelist Entry`. If it doesn't, enter it manually. Lastly, click confirm.
![Whitelist All IP's](https://i.imgur.com/UgIYkoA.png)
- Time to connect to the Database! Go to `Cluster` under the `DATA STORAGE` tab. If your database is still setting up, please wait until it's done! Once it is, click the `CONNECT` button and `Connect Your Application`. Copy a link that **looks** like this; `mongodb+srv://<username>:<password>@cluster0.r4nd0m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`
- Lastly, remove the `myFirstDatabase?retryWrites=true&w=majority` part and replace `<username>` with your user's name (sometimes it is already replaced in if there's only one user), and `<password>` with your saved password.
- Your database is done!

# Contributions
If you wish to contribute to the bot, please make sure you have a reason to do so. Avoid any small commits such as, renaming variables, changing the way a function works with no benefit, and such.
***And make sure your commit messages are short but descriptive.***
> ***Read [this article](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/) to learn more***

<center style="margin-top:30px">
<h1><strong><em>💖 CONTRIBUTORS 💖</em></strong></h1>
<a href="https://github.com/BytesToBits/LockPass/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BytesToBits/LockPass" />
</a>
</center>
