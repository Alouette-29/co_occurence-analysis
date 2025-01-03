import os
import re
import numpy as np
from typing import Literal


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
        if "·" in name:
            first_name, last_name = name.split("·")
            names_dict[name] = [name, first_name, last_name]
        else:
            names_dict[name] = [name]
    
    count_dict = {}
    for name in names_dict:
        aliases = names_dict[name]
        count = 0
        for alias in aliases:
            count += context.count(alias)
        count_dict[name] = count

    return count_dict


def co_occurence(people: list[str], contexts: list[str]) -> tuple[np.ndarray]:
    """
    给定某一部的所有内容（以chunk列表形式呈现）
    返回人物之间的共现关系矩阵
    `co_matrix`按照每次在chunk共现就加一计数
    `freq_matrix`按照在chunk中共现时出现较少的那一方的频次计数
    """
    n_people = len(people)
    co_matrix = np.zeros((n_people, n_people))
    freq_matrix = np.zeros((n_people, n_people))
    for context in contexts:
        count_dict = count_name_frequency(people, context)
        for i, person1 in enumerate(people):
            for j, person2 in enumerate(people[i + 1:]):
                if count_dict[person1] > 0 and count_dict[person2] > 0:
                    co_matrix[i][j] += 1
                    co_matrix[j][i] += 1
                    freq = min(count_dict[person1], count_dict[person2])
                    freq_matrix[i][j] += freq
                    freq_matrix[j][i] += freq
    
    return co_matrix, freq_matrix


if __name__ == "__main__":
    file_path = "book/00-人物简介.txt"
    people = extract_people(file_path)
    co_matrices, freq_matrices = [], []
    for i in range(5):
        contexts = load_book_section("book", i + 1)
        co_matrix, freq_matrix = co_occurence(people, contexts)
        co_matrices.append(co_matrix)
        freq_matrices.append(freq_matrix)
    
    if not os.path.exists("output"):
        os.makedirs("output")
    
    with open("output/co_matrices.txt", "w", encoding="utf-8") as f:
        f.write(co_matrices)
    with open("output/freq_matrices.txt", "w", encoding="utf-8") as f:
        f.write(freq_matrices)
    