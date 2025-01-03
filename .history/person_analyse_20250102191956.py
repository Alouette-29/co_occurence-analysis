import os
import re
from typing import Literal
from collections import Counter


script_dir = os.path.dirname(__file__)
os.chdir(script_dir)


def extract_people(file_path: str) -> list[str]:
    """
    从人物简介中抽取人物列表
    """
    people = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        match = re.match(r'(.*?)：', line)
        if match:
            person = match.group(1).strip()
            people.append(person)
        else:
            print("人名匹配出错")
    return people


def load_book_section(data_dir: str, index: Literal[1, 2, 3, 4, 5]) -> list[str]:
    """
    加载第index部的全文，总共五部
    原本的格式就是天然的chunk，不进行拼接
    """
    index_span = [1, 10, 22, 24, 34, 39]  # 第几个文件到第几个文件是哪一部
    start, end = index_span[index - 1], index_span[index]
    file_names = os.listdir(data_dir)[start: end]
    
    contents = []
    for file_name in file_names:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            contents.append(content)

    return contents


def count_name_frequency(people: list[str], context: str) -> dict:
    """
    给定上下文和人名列表，统计人物出现次数
    由于外国的人名用 "·" 隔开，所以全名、姓、名都要统计然后累加
    假设所有人的姓名都没有重叠
    """
    names_dict = {}
    for name in people:
        assert "·" in name
        first_name, last_name = name.split("·")
        names_dict[name] = [name, first_name, last_name]
    
    count_dict = {}
    for name in names_dict:
        full_name, first_name, last_name = names_dict[name]
        count = context.count(full_name) + context.count(first_name) + context.count(last_name)
        count_dict[name] = count

    return count_dict


def 


if __name__ == "__main__":
    file_path = "book/00-人物简介.txt"
    people = extract_people(file_path)
    