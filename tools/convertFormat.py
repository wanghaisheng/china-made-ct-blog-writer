import os
import pypandoc

def cvt2doc(md_folder_name, output_format):
    # 定义输出文件夹和转换后缀，以便于让md生成docx或pdf

    md_folder = md_folder_name
    output_extension = output_format # 可以根据需要修改为"pdf"

    # 获取输入文件夹中的所有md文件
    md_files = [f for f in os.listdir(md_folder) if f.endswith(".md")]

    for md_file in md_files:
        input_file_path = os.path.join(md_folder, md_file)
        output_file_path = os.path.join(md_folder, md_file.replace(".md", f".{output_extension}"))

        try:
            pypandoc.convert_file(input_file_path, output_extension, outputfile=output_file_path)
            print(f"成功将 {md_file} 转换为 {output_file_path}")
        except Exception as e:
            print(f"转换 {md_file} 时出错: {e}")

