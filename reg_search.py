import re
import json
from datetime import datetime

def is_date_format(value):
    """
    检查字符串是否是日期格式（如 YYYY 年 MM 月 DD 日）。
    """
    try:
        datetime.strptime(value.replace(' ', '').replace('\n', '').replace('年', '-').replace('月', '-').replace('日', ''), '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_date(value):
    """
    格式化日期字符串为 YYYY-MM-DD。
    """
    clean_value = value.replace(' ', '').replace('\n', '').replace('年', '-').replace('月', '-').replace('日', '')
    return datetime.strptime(clean_value, '%Y-%m-%d').strftime('%Y-%m-%d')


def reg_search(text, regex_list):
    """
    自定义正则匹配函数
    :param text: str, 需要正则匹配的文本内容
    :param regex_list: list of dict, 正则表达式列表，每个字典的键为名称，值为正则表达式
    :return: list of dict, 每个正则匹配项的结果
    """
    results = []
    
    for regex_group in regex_list:
        result = {}
        
        for key, pattern in regex_group.items():
            matches = re.findall(pattern, text, re.DOTALL)  # 匹配结果列表，支持跨行匹配
            matches = [match if isinstance(match, str) else "".join(match) for match in matches]  # 展平元组
            
            if all(is_date_format(match) for match in matches):  # 如果全部是日期格式
                result[key] = [format_date(match) for match in matches]
            elif len(matches) == 1:  # 单个匹配结果
                result[key] = matches[0]
            elif len(matches) > 1:  # 多个匹配结果存为列表
                result[key] = matches
        
        results.append(result)
    
    return results


# 测试示例
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''

# 正则表达式列表
regex_list = [{
    '标的证券': r'股票代码：([A-Z0-9.]+)',
    '换股期限': r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)'  # 捕获日期
}]

# 调用函数并打印结果
result = reg_search(text, regex_list)
print(json.dumps(result, ensure_ascii=False, indent=4))
