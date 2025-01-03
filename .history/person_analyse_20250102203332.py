import os
import re
import json
import numpy as np
from typing import Literal
import matplotlib.pyplot as plt


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
                    co_matrix[i][i + j + 1] += 1
                    co_matrix[i + j + 1][i] += 1
                    freq = min(count_dict[person1], count_dict[person2])
                    freq_matrix[i][i + j + 1] += freq
                    freq_matrix[i + j + 1][i] += freq
    
    return co_matrix, freq_matrix


def draw_heatmap(co_matrix: np.ndarray, freq_matrix: np.ndarray, people: list[str]):
    


    # 创建两个示例矩阵（你可以替换为自己的实际矩阵数据）
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])

    # 设置自定义的横轴和纵轴标签（可根据实际情况修改）
    x_labels = ['col1', 'col2']
    y_labels = ['row1', 'row2']

    # 创建包含两个子图的图形，一行两列布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # 绘制第一个热力图
    im1 = ax1.imshow(matrix1, cmap='viridis')
    # 设置纵轴标签
    ax1.set_yticks(np.arange(len(y_labels)))
    ax1.set_yticklabels(y_labels)
    # 设置横轴标签
    ax1.set_xticks(np.arange(len(x_labels)))
    ax1.set_xticklabels(x_labels)
    ax1.set_title("Matrix 1 Heatmap")

    # 绘制第二个热力图
    im2 = ax2.imshow(matrix2, cmap='viridis')
    # 设置纵轴标签
    ax2.set_yticks(np.arange(len(y_labels)))
    ax2.set_yticklabels(y_labels)
    # 设置横轴标签
    ax2.set_xticks(np.arange(len(x_labels)))
    ax2.set_xticklabels(x_labels)
    ax2.set_title("Matrix 2 Heatmap")

    # 添加颜色条
    fig.colorbar(im1, ax=ax1)
    fig.colorbar(im2, ax=ax2)

    # 调整子图之间的间距等布局设置
    plt.tight_layout()

    # 显示图形
    plt.show()


if __name__ == "__main__":
    file_path = "book/00-人物简介.txt"
    people = extract_people(file_path)
    co_list = []
    for i in range(5):
        contexts = load_book_section("book", i + 1)
        co_matrix, freq_matrix = co_occurence(people, contexts)



        co_dict = {"idx": f"section {i + 1}"}
        co_dict["co_matrix"] = co_matrix.tolist()
        co_dict["freq_matrix"] = freq_matrix.tolist()
        co_list.append(co_dict)
    
    if not os.path.exists("output"):
        os.makedirs("output")
    
    with open("output/co_occurence.json", "w") as f:
        json.dump(co_list, f, indent=4)
