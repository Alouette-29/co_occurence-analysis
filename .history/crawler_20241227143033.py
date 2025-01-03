import os


def crawl(book_url: str):
    pass


if __name__ == "__main__":
    book_url = "https://luoxiadushu.com/shuyi/"
    data_dir = "book"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)