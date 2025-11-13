# How to run:

```shell
cp config.ini.example config.ini
vi config.ini  # and fill in your data
```

```sh
echo "YOUR_TOKEN_FROM_BotFather" > token.txt

python3 -m venv ./venv
./venv/bin/pip install -r requirements.txt

./venv/bin/python home_portal_bot.py
```


# How to create a daemon

Create file `/etc/systemd/system/my_home_portal_bot.service` with the following content (change `<path_to>`):
```
[Service]
WorkingDirectory=/home/user/<path_to>/tuya-home-portal-bot/
ExecStart=/home/user/<path_to>/tuya-home-portal-bot/venv/bin/python home_portal_bot.py

User=root

Restart=always

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl start my_home_portal_bot.service
systemctl status my_home_portal_bot.service
sudo journalctl -u my_home_portal_bot.service
```