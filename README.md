# Instalike - Instagram bot (No API requirements)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4ZCR74EKJKPDA)

![Some likes](https://s32.postimg.org/53zwfkat1/Screenshot_2016_05_25_05_20_06_1.png)

# Available features
- Automated likes
- Automated follows
- Automated unfollows
- **Compatible with PythonAnywhere - end of README**

# Configuration Guide
Edit `default.cfg` file
<table>
  <tr>
    <th>Option</th>
    <th>Meaning</th>
  </tr>
  <tr>
    <td>BOT::WorkWholeTime</td>
    <td>If set to <code>True</code> bot will work whole time, no breaks. In other case periods will be in use.</td>
  </tr>
  <tr>
    <td>BOT::BotWorkAtDay</td>
    <td>If set to <code>True</code> bot will work from between specified hours. Requires option <code>BOT::WorkWholeTime</code> set to <code>True</code>.</td>
  </tr>
  <tr>
    <td>BOT::StopAfterNumerOfMinutes</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>BOT::WorkHoursPerDay</td>
    <td>If option <code onmouseover='alert(1);'>BOT::WorkWholeTime</code> is set to <code>False</code> bot will work in 2 to 5 periods that sum up to that amount.</td>
  </tr>
  <tr>
    <td>BOT::StartHour</td>
    <td>Requires option <code>BOT::WorkAtDay</code> set to <code>True</code>. Specify hour at which bot should start working.</td>
  </tr>
  <tr>
    <td>BOT::EndHour</td>
    <td>Requires option <code>BOT::WorkAtDay</code> set to <code>True</code>. Specify hour at which bot should stop working.</td>
  </tr>
  <tr>
    <td>BOT::InstaLike</td>
    <td>If set to <code>True</code> bot will be liking photos.</td>
  </tr>
  <tr>
    <td>BOT::InstaFollow</td>
    <td>If set to <code>True</code> bot will be following users.</td>
  </tr>
  <tr>
    <td>BOT::InstaComment</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>BOT::InstaMessage</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>NOTIFICATIONS::EnableEmailSummaryNotifications</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>NOTIFICATIONS::SendAttachment</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>NOTIFICATIONS::EmailAdress</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>NOTIFICATIONS::EmailServerAddress</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>NOTIFICATIONS::EmailServerPassword</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>BAN::DoNotGetBanned</td>
    <td>not working</td>
  </tr>
  <tr>
    <td>INSTAGRAM::Username</td>
    <td>Instagram username.</td>
  </tr>
  <tr>
    <td>INSTAGRAM::Password</td>
    <td>Instagram password.</td>
  </tr>
  <tr>
    <td>INSTALIKE::MaxLikesPerHour</td>
    <td>Estimate what max likes per hour should be, based on this setting wait times are calculated. <code>200</code> is default.</td>
  </tr>
    <tr>
  <td>INSTALIKE::LikeFeedMedia</td>
  <td>If set to <code>True</code> bot will also scrap media from your feed.</td>
  </tr>
  <tr>
    <td>INSTALIKE::Tags</td>
    <td>Specify tags that bot will use to find and like photos or follow users. Make sure to put comma between tags e.g. <code>tag1, tag2, tag3, tag4</code></td>
  </tr>

  <tr>
    <td>INSTAFOLLOW::MaxFollowsPerHour</td>
    <td>Max users that will be followed per hour. Default value is <code>8</code></td>
  </tr>
  <tr>
    <td>INSTAFOLLOW::MaxUnfollowsPerHour</td>
    <td>Max users that will be unfollowed per hour. Default value is <code>2</code>. Unfollowing functionality in progress.</td>
  </tr>
  <tr>
    <td>INSTAFOLLOW::UnfollowAfterNoOfDays</td>
    <td>Unfollow users who do not follow you back after that amount of days. <code>6</code> is default</td>
  </tr>
  <tr>
    <td>BLACKLIST::PhotoTagsList</td>
    <td>Specify tags that you would like to avoid. e.g. <code>comma, separated, list, format</code></td>
  </tr>
  <tr>
    <td>BLACKLIST::UserNameBlacklist</td>
    <td>Don't like media posted by user with these names. Don't follow users with these names. Comma separated list e.g. <code>mickey15, hulk12, lover2020</code></td>
  </tr>
  <tr>
    <td>BLACKLIST::UserDescription</td>
    <td>Avoid users whose description contains any of these words. e.g. <code>comma, separated, list, format</code></td>
  </tr>
  <tr>
    <td>LIKEFILTER::MinLikesOnPhoto</td>
    <td>Do not like photos with less likes than specified value, default value is <code>0</code> which is no limit</td>
  </tr>
  <tr>
    <td>LIKEFILTER::MaxLikesOnPhoto</td>
    <td>Do not like photos with more likes than specified value, default value is <code>0</code> which is no limit</td>
  </tr>
</table>

# Starting bot
If you have provided your username and password combination in `default.cfg` file then start with `python main.py` otherwise use `python main.py -u username -p password`.

You can create a new configuration file by copying `default.cfg`, and then you can pass it on startup like that: `python main.py -u username -p password -c filename` - where `filename` is the name of the new configuration file.


# Requirements
- python 3+
- `python -m pip install requests`
- `python -m pip install peewee`

# PythonAnywhere setup

Set up a PythonAnywhere account and start a bash console.
Clone the repository and then move to the directory:
$ git clone https://github.com/mpawlak2/instalike-instagram-bot.git
$ cd instalike-instagram-bot.git
Install requirements **like this**:
$ pip3 install -U requests --user
$ pip3 install -U peewee --user
The installation is now complete. Now, you can edit **default.cfg** file or run the bot using the following command:
$ python3 main.py -u username -p password

# External libs docs
[Peewee documentation](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html)
