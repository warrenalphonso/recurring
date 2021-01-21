# Recurring 

Recurring uses [SendGrid's Python API](
https://github.com/sendgrid/sendgrid-python) to send reminder emails to myself. 
I'll [use Heroku to run the Python script periodically](
https://medium.com/analytics-vidhya/schedule-a-python-script-on-heroku-a978b2f91ca8
). The idea is to slowly and consistently consume large collections of important 
material. For example, the first project sends me the text of each post in 
the [original LW sequences](https://www.lesswrong.com/tag/original-sequences). 
I receive daily emails of the posts in sequential order via a link to 
[this website](https://www.readthesequences.com/). 

`main.py` is where the magic happens. The rest of the files are code to curate 
the material in an appropriate form. 
