import os
import tkinter as tk
from tkinter import filedialog


def extract_lines(input_file):
    output_map = {}
    letters_to_extract = {'C', 'E', 'G', 'R', 'J'}
    header_lines = []
    output_lines = []
    found_end_of_header = False
    current_letter = None
    flag = False

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # 不去除空格，直接保留原始行内容
        if "END OF HEADER" in line:
            found_end_of_header = True
            header_lines.append(line)
        elif not found_end_of_header:
            header_lines.append(line)
        else:
            first_char = line[0]
            if first_char in letters_to_extract:
                if current_letter != first_char:
                    if current_letter and output_lines:
                        # 添加header到输出文件中
                        output_lines = header_lines + output_lines
                        output_map[current_letter] = output_lines
                        output_lines = []
                    current_letter = first_char
                    flag = False
                output_lines.append(line)
            elif first_char.isalpha() and first_char not in letters_to_extract:
                flag = True
            elif not flag:
                output_lines.append(line)

    # 保存输出
    if current_letter and output_lines:
        output_lines = header_lines + output_lines
        output_map[current_letter] = output_lines

    # 获取输入文件的文件名和扩展名
    file_name, file_ext = os.path.splitext(os.path.basename(input_file))
    # 获取输入文件所在的目录
    input_dir = os.path.dirname(input_file)

    # 将输出写入文件（保留原始格式）
    for key, value in output_map.items():
        # 根据字母替换 MN 为对应的 EN、CN、GN、RN、JN
        new_file_name = file_name.replace("MN", f"{key}N") + file_ext
        output_file = os.path.join(input_dir, new_file_name)
        with open(output_file, 'w', encoding='utf-8') as f:
            # 保留原格式，不做任何处理，直接写入
            f.writelines(value)
        print(f"提取完成，结果保存在 {output_file}")


def select_file():
    # 使用tkinter打开文件选择对话框
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口

    file_path = filedialog.askopenfilename(
        title="选择输入文件",
        filetypes=(("RNX Files", "*.rnx"),
                   ("Text Files", "*.txt"),
                   ("All Files", "*.*"))
    )

    if file_path:
        extract_lines(file_path)
    else:
        print("未选择文件！")


# 使用文件选择界面来选择文件
select_file()
