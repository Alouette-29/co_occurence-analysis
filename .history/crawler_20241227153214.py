import os
import re
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


def get_chapter_content(chapter_url: str) -> str:
    """
    给定章节url，返回该章节的内容
    """
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, 'lxml')
    chapter_div = soup.find('div', id='nr1')
    if not chapter_div:
        return "章节内容未找到"
    
    content = ""
    for p_tag in chapter_div.find_all("p"):
        passage = p_tag.get_text()
        if re.search("落", passage) and re.search("霞", passage) and re.search("读", passage) and re.search("书", passage):
            continue
        content += passage + "\n"

    print(content)
    return content.strip()


if __name__ == "__main__":
    book_url = "https://luoxiadushu.com/shuyi/"
    data_dir = "book"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    chapter_links = get_chapter_links(book_url)
    