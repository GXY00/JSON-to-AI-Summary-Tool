import json
import os
from google import genai
from google.genai import types

def validate_file_path(file_path, file_type="JSON"):
    """验证文件路径有效性"""
    # 检查路径是否为空
    if not file_path:
        return False, f"{file_type}文件路径不能为空"
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, f"{file_type}文件 '{file_path}' 不存在"
    
    # 检查是否是文件
    if not os.path.isfile(file_path):
        return False, f"'{file_path}' 不是一个有效的文件"
    
    # 检查文件扩展名
    expected_ext = f".{file_type.lower()}"
    if not file_path.lower().endswith(expected_ext):
        return False, f"文件 '{file_path}' 不是{file_type}格式（应为{expected_ext}）"
    
    return True, "路径有效"

def json_to_txt(json_file_path):
    """
    读取JSON文件，提取所有content字段，用逗号连接后保存为同名TXT文件
    """
    try:
        # 验证文件路径
        valid, message = validate_file_path(json_file_path, "JSON")
        if not valid:
            print(f"错误: {message}")
            return None

        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 检查数据是否为列表
        if not isinstance(data, list):
            print("错误: JSON文件内容不是一个列表")
            return

        # 提取所有content字段
        contents = []
        for item in data:
            if isinstance(item, dict) and 'content' in item:
                contents.append(str(item['content']))
            else:
                print(f"警告: 跳过无效条目 {item}")

        # 用逗号连接所有内容
        combined_text = ', '.join(contents)

        # 生成TXT文件名（与JSON文件同名）
        txt_file_path = os.path.splitext(json_file_path)[0] + '.txt'

        # 保存到TXT文件
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(combined_text)

        print(f"成功生成TXT文件: {txt_file_path}")

        return '用一段话总结后面这段话：'+combined_text

    except json.JSONDecodeError:
        print(f"错误: 文件 '{json_file_path}' 不是有效的JSON格式")
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")

def aiSummary(words):
    """
    调用Gemini API总结字幕内容
    Call the Gemini API to summarize the subtitle content
    :param words: 文件内容 File content
    :return: 打印总结内容，同时生成txt文件 Print the summary content and generate a txt file at the same time
    """
    if not words:
        print("错误: 没有可总结的内容")
        return None

    #如果已将密钥配置在环境变量中
    #If the key has been configured in the environment variables
    client = genai.Client()
    #代码中配置密钥
    #Configure the secret key in the code
    #client = genai.Client(api_key='your key')

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=words,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # 取消思考，加快反应速度
        ),
    )

    # 检查响应是否有效
    if not response.candidates:
        print(f"未返回有效结果")
        return None

    if not response.candidates[0].content or not response.candidates[0].content.parts:
        print(f"返回内容格式不正确")
        return None

    summary_text = response.candidates[0].content.parts[0].text
    if summary_text:
        print('\n以下为视频内容总结：')
        print(summary_text)
        return summary_text

    print(f"空内容")

if __name__ == "__main__":
    # 使用input()函数获取文件路径
    print("请输入JSON文件的路径（例如：C:\\字幕\\文件.json 或 /home/user/文件.json）：")
    json_file_path = input().strip()

    # 处理可能的引号（如果用户输入时加了引号）
    if (json_file_path.startswith('"') and json_file_path.endswith('"')) or \
            (json_file_path.startswith("'") and json_file_path.endswith("'")):
        json_file_path = json_file_path[1:-1]

    # 调用转换函数
    content = json_to_txt(json_file_path)
    aiSummary(content)
    input("\n按回车键退出...")
