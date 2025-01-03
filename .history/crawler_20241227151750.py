import os
import requests
from bs4 import BeautifulSoup




def get_chapter_links(book_url: str) -> list[str]:
    """
    给定章节列表的页面，返回所有的正文章节url列表
    """
    response = requests.get(book_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    chapter_links = []
    # 章节的href只在<div class=book-list clearfix><ul><li>下
    for li_tag in soup.select("div.book-list.clearfix ul li"):
        for a_tag in li_tag.find_all('a', href=True):
            chapter_url = a_tag['href']
            chapter_links.append(chapter_url)
    # 去掉译序和后记
    chapter_links = chapter_links[3: -3]
    return chapter_links


def get_chapter_content(chapter_link: str)


if __name__ == "__main__":
    book_url = "https://luoxiadushu.com/shuyi/"
    data_dir = "book"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    chapter_links = get_chapter_links(book_url)
    