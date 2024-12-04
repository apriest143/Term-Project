# Term-Project
Andrew and Cole's OIM3640 Term Python Project

Big Idea/Goal/Why did we do this?

As busy and often frantic college students we often struggle with keeping up with events and meeting throughout the year. We wanted an easy way to automatically upload events into the a calendar using computer vision and flyers that we frequently get sent to our inboxes or see around campus.



Provide guidance to users regarding downloading, installation, and initial use of your software. Here is a collection of incredible READMEs that can help you get started. 
Implementation Information:
There is a large number of packages that need installation before this our project can be ran properly.

for models.py:
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

for main.py:
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
from dateutil import parser

(IMPORTANT) pytesseract must correctly pathed to the repository during installation or else it will not call correctly

for flyer_app.py: 
from flask import Flask, request, render_template, redirect, url_for, session, g, current_app
import datetime
import os
from main import image_upload, analyze_text_with_ai
from werkzeug.utils import secure_filename
from models import db, User, Event, Image
from functools import wraps
from dotenv import load_dotenv
import logging
from ics import Calendar, Event as ICSEvent
from flask import send_file
import io



Although each project will have unique details, showcasing your software's capabilities is essential! Screenshots and video can be especially useful. Include graphs and data, if appropriate.

COLE ADD SOME GOOD SCREENSHOTS HERE

Our project works quite functionally. The computer vision does struggle to find information depending on the complexity and amount of information shown on the uploaded image. However, it is quite good with dates and getting an overall summary of the event.

We began by creating basic flask routes and HTML pages that would follow the journey of an uploaded image, we needed a homepage, a place to upload and image, a place where uploads could live, and a calendar page where the output would eventually get placed. Once this functional skeleton was built we began implementing the API aspect so that it could glean information from the images that were uploaded. While troubleshooting this API we added in some quality of life changes to the web pages themselves such as a username function, a home banner, and general UI improvements. This led us with a decently good looking website with a functional computer vision API that could pretty accurately glean inforation from flyers and store the information into an auto updating calendar.



AI was used heavily during this project during the frequent and lengthy troubleshooting processes. It was very helpful for building functionality out of HTML that we did not learn in class, namely in the creation of a calendar. It was also invaluable in explaining the installation processes of many of the packages that we would need to make this project functional. Pushing our project to main while hiding the API key was an incredibly confusing an obtuse process, and without the use of generative AI, I highly doubt we would have been able to figure it out on our own.
