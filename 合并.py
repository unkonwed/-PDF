import os
import re
from PyPDF2 import PdfMerger, PdfReader


def merge_pdfs():
    # 获取当前目录下所有PDF文件
    files = [f for f in os.listdir('.') if f.endswith('.pdf')]

    # 提取章节数字并排序
    chapter_files = []
    for f in files:
        match = re.match(r'第(\d+)章\.pdf', f)
        if match:
            chapter_num = int(match.group(1))
            chapter_files.append((chapter_num, f))

    # 按章节数字排序
    chapter_files.sort(key=lambda x: x[0])

    if not chapter_files:
        print("未找到符合'第X章.pdf'格式的PDF文件")
        return

    # 创建PDF合并器
    merger = PdfMerger()
    success_count = 0

    print(f"发现 {len(chapter_files)} 个章节文件，开始合并...")

    for idx, (num, filename) in enumerate(chapter_files, 1):
        try:
            with open(filename, 'rb') as f:
                # 验证PDF有效性
                PdfReader(f)
                f.seek(0)
                merger.append(f)
                success_count += 1
                print(f"已合并第 {num} 章 ({idx}/{len(chapter_files)})")
        except Exception as e:
            print(f"跳过 {filename} (错误: {str(e)})")

    # 生成合并后的文件
    if success_count > 0:
        output_name = "完整版.pdf"
        with open(output_name, 'wb') as f:
            merger.write(f)
        print(f"\n合并完成！共成功合并 {success_count} 个章节")
        print(f"输出文件: {os.path.abspath(output_name)}")
    else:
        print("没有有效PDF文件可合并")

    merger.close()


if __name__ == "__main__":
    merge_pdfs()
