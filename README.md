# StealMemes

StealMemes is a python script which scrapes meme images and videos from iFunny.co's top memes of the day page.

Python libraries requests and bs4 are used to find image download links. Selenium webdriver must be used to find video downloads since iFunny.co loads videos dynamically through javascript.

**WARNING** - As the project currently stands, memes will always be saved to a /memes folder with a non-random name. So, running the script more than once will overwrite the files in /memes. To avoid this, you can remedy my code or transfer any memes you want to safeguard to a different directory than /memes.

### Prerequisites

You must have Chromedriver and Selenium Webdriver to use this project. Learn about using Chromedriver and Selenium here:
- https://chromedriver.chromium.org/getting-started
- https://selenium-python.readthedocs.io/installation.html
- https://selenium-python.readthedocs.io/getting-started.html

### Installation

Once selenium is installed properly, you can run this project through:

```
git clone https://github.com/YulkyTulky/StealMemes.git
cd StealMemes
python StealMemes.py
```

## Authors

* **Eamon Tracey** - *Initial work* - [YulkyTulky](https://github.com/YulkyTulky)
