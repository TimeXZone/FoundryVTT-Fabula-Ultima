import json
import os
import re

def is_chinese(text):
    # 判断字符串是否包含中文
    return bool(re.search(r'[\u4e00-\u9fff]', str(text)))

def find_non_chinese_keys(data, path=""):
    non_chinese = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                non_chinese.extend(find_non_chinese_keys(value, current_path))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    item_path = f"{current_path}[{i}]"
                    if isinstance(item, dict):
                        non_chinese.extend(find_non_chinese_keys(item, item_path))
                    elif not is_chinese(item):
                        non_chinese.append(item_path)
            else:
                if not is_chinese(value):
                    non_chinese.append(current_path)
    return non_chinese

def main():
    final_path = os.path.join('final_version', 'cn.json')

    with open(final_path, 'r', encoding='utf-8') as f:
        final_json = json.load(f)

    non_chinese_keys = find_non_chinese_keys(final_json)

    print("Keys without Chinese characters:")
    for key in non_chinese_keys:
        print(key)

if __name__ == '__main__':
    main()