import os
import re
import pandas as pd

# 配置：要处理的ckt文件列表
ckt_files = ["c499.ckt", "c1355.ckt", "c2670.ckt"]

# 定义： "Buffer" 类别
buffer_keywords = ["BUF", "BUFFER"]

# 定义：特殊节点 (不算 Cell)
special_nodes = ["INPUT", "OUTPUT"]

# 结果收集
result_list = []


def parse_ckt_file(filepath, index_start):
    """
    解析单个ckt文件，统计Cell和Buffer数量
    """
    num_cells = 0
    num_buffers = 0

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # 清除注释和空白
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # 提取门的类型，通常是这一行的第一个单词
            tokens = re.split(r'\s+', line)
            if not tokens:
                continue
            gate_type = tokens[0].upper()

            # 忽略输入输出
            if gate_type in special_nodes:
                continue

            # 计数 Cell
            num_cells += 1

            # 如果是Buffer
            if any(buf in gate_type for buf in buffer_keywords):
                num_buffers += 1

        return num_cells, num_buffers

    except FileNotFoundError:
        print(f"[Error] File not found: {filepath}")
        return None, None


def main():
    table_rows = []
    index_start = 1  # 起始索引，比如文献是从1开始
    for idx, ckt_file in enumerate(ckt_files, start=index_start):
        if not os.path.exists(ckt_file):
            print(f"[Warning] File '{ckt_file}' not found. Skipping.")
            continue

        num_cells, num_buffers = parse_ckt_file(ckt_file, idx)
        if num_cells is not None:
            table_rows.append([idx, os.path.splitext(ckt_file)[0], num_cells, num_buffers])

    # 生成DataFrame表格
    df = pd.DataFrame(table_rows, columns=["Index", "Case", "#Cell", "#Buffer"])

    # 打印表格
    print("\nTest cases and detailed information:")
    print(df.to_markdown(index=False))

    # 可以保存成csv或其他格式
    df.to_csv("parsed_results.csv", index=False)
    print("\n[Info] Results saved to 'parsed_results.csv'.")


if __name__ == "__main__":
    main()
