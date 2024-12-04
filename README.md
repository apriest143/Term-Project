# Term-Project
Andrew and Cole's OIM3640 Term Python Project

Big Idea/Goal/Why did we do this?

As busy and often frantic college students we often struggle with keeping up with events and meeting throughout the year. We wanted an easy way to automatically upload events into the a calendar using computer vision and flyers that we frequently get sent to our inboxes or see around campus.

With our program users can upload an image of a flier and GPT will get the details for the event from the image, and allow you to download the event to you calender.


Implementation Information:
There is a large number of packages that need installation before this our project can be ran properly.

# Core Dependencies
- Flask==3.0.0 (Web framework)
- Flask-SQLAlchemy==3.1.1 (Database ORM)
- Pillow==10.1.0 (Image processing)
- pytesseract==0.3.10 (OCR text extraction)
- python-dotenv==1.0.0 (Environment variables)
- openai==1.3.5 (AI text analysis)
- python-dateutil==2.8.2 (Date parsing)
- ics==0.7.2 (Calendar export)
- Werkzeug==3.0.1 (WSGI utilities)

# System Requirement
- Tesseract OCR (System package for OCR)

(IMPORTANT) pytesseract must correctly pathed to the repository during installation or else it will not call correctly

<img width="1018" alt="image" src="https://github.com/user-attachments/assets/7e1b8517-8035-4270-b379-59861cda8491">
<img width="1031" alt="image" src="https://github.com/user-attachments/assets/b8c8b561-a9d1-4696-a432-a27d98cee060">


Our project works quite functionally. The computer vision does struggle to find information depending on the complexity and amount of information shown on the uploaded image. However, it is quite good with dates and getting an overall summary of the event.

We began by creating basic flask routes and HTML pages that would follow the journey of an uploaded image, we needed a homepage, a place to upload and image, a place where uploads could live, and a calendar page where the output would eventually get placed. Once this functional skeleton was built we began researching how to implement the image to text functionality.  After considering using API's from Google and AWS, we found Tesseract which is avalible as a python libary with pytesseract. Next we created the functionality to get the event details from this relitivly unstructured text. We decided to use the OpenAI API as it is able to handle dynamic text responses better that code we could create.  We created a prompt to tell GPT exactly what to look for in the text and how to format the result, so that it can be picked up from the rest of the app. Next we discovered that we needed a way to properly store the event information, so we attempted to implement a SQLite database. At this point after getting the base flask site to work, to optimize the UX flow we used Copilot to help us implement the database and remeber who uploaded what events.  This enabled the calender page to populate with the correct infromation. Next we added in some quality of life changes to the web pages themselves such as a username function, a navagation bar, and general UI improvements. This left us with a decently good looking website that successfuly utilizes computer vision and the OpenAI API to accurately glean inforation from flyers and store the information into an auto updating calendar.


AI was used heavily during this project during the frequent and lengthy troubleshooting processes. It was very helpful for building functionality out of HTML that we did not learn in class, namely in the creation of a calendar, database, session storage. It was also invaluable in explaining the installation processes of many of the packages that we would need to make this project functional. Pushing our project to main while hiding the API key was an incredibly confusing an obtuse process, and without the use of generative AI, I highly doubt we would have been able to figure it out on our own.

Upon completion we hosted it on Pythonanywhere, where it can be found here: https://vampartyslayer.pythonanywhere.com/upload
* Please note that it runs very slow on Pythonanywhere, we recomend forking it to your computer and using your own OpenAi key
