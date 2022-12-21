import requests  # send http req
from bs4 import BeautifulSoup  # handel html feature to found it (req)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
html_response = requests.get('https://www.google.com/search?q=news&hl=en', headers=headers)
soup = BeautifulSoup(html_response.content, 'html.parser')
with open("s.html", "w+", encoding="utf-8") as f:
    f.write(soup.prettify())
news = soup.find_all('div', attrs={"class": "mCBkyc tNxQIb ynAwRc nDgy9d"})
news = [i.text.replace("...", "").strip() for i in news]

# test
# from Speaker_Identification import *
# add_known_voice('Y1.wav', "Yousr Ahmed 1")
# add_known_voice('Y2.wav', "Yousr Ahmed 2")
# add_known_voice('N.wav', "NourEldin Osama")
# print(get_unknown_voice("Y2.wav"))
