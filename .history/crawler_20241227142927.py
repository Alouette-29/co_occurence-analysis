import os


if __name__ == "__main__":
    book_url = "https://luoxiadushu.com/shuyi/"
    if not os.path.exists(book_url):
        os.makedirs(book_url)