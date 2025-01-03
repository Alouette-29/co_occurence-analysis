import os
import re


script_dir = os.path.dirname(__file__)
os.chdir(script_dir)


def extract_people(file_path: str) -> list[str]:
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


if __name__ == "__main__":
    file_path = "book/0-人物简介.txt"
    people = extract_people(file_path)
    
