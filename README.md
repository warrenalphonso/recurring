**Recurring** uses Python's [smtplib library](
https://realpython.com/python-send-email/) to send periodic emails with 
dynamic content. I'll [use Heroku to run the Python script periodically](
https://medium.com/analytics-vidhya/schedule-a-python-script-on-heroku-a978b2f91ca8
). I'll create a throwaway GMail account 
because using smtplib requires some changing some setting in GMail which makes 
it less secure. I'll also be storing the email password in Heroku's environment 
config files, and I don't trust myself to not do something stupid which leaks 
the password. 

The original intent is to send me the text of each post in the [original 
LW sequences](https://www.lesswrong.com/tag/original-sequences). I receive 
daily emails of the posts in sequential order via a link to [this website](
https://www.readthesequences.com/). 
