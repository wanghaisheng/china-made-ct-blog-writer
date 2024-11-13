import os
import shutil


def clear_cache():
    # 清除output文件夹中的md文件和docx文件
    output_folder = "./output"
    if os.path.exists(output_folder):
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                if file.endswith(".md") or file.endswith(".docx"):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

    # 清除tools和generation文件夹下的__pychache__
    folders_to_clear = ["feishu_api", "tools", "generation"]
    for folder in folders_to_clear:
        pychache_folder = os.path.join(folder, "__pycache__")
        if os.path.exists(pychache_folder):
            shutil.rmtree(pychache_folder)


if __name__ == "__main__":
    clear_cache()