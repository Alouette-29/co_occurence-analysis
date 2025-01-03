import os
import requests
from bs4 import BeautifulSoup




def crawl(book_url: str):
    pass


if __name__ == "__main__":
    book_url = "https://luoxiadushu.com/shuyi/"
    data_dir = "book"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


    response = requests.get(book_url)
    response.encoding = 'utf-8'  # 根据网页实际编码设置
    soup = BeautifulSoup(response.text, 'lxml')

    chapter_links = []
    for li_tag in soup.select("div.book-list.clearfix ul li"):
        for a_tag in li_tag.find_all('a', href=True):  # 假设所有含href属性的a标签都是章节链接
            chapter_url = a_tag['href']
            chapter_links.append(chapter_url)
    
    print(chapter_links)