import pickle

def load_pkl_file(file_path):
    """
    解析 .pkl 文件并返回其中的内容。
    
    :param file_path: .pkl 文件的路径
    :return: 反序列化后的 Python 对象
    """
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。")
    except pickle.UnpicklingError:
        print("错误: 无法反序列化该文件。文件可能已损坏。")
    except Exception as e:
        print(f"发生错误: {e}")

def save_data_to_txt(data, dst_file):
    """
    将数据写入文本文件。
    
    :param data: 要写入的 Python 对象
    :param dst_file: 目标文本文件路径
    """
    try:
        with open(dst_file, 'w') as f:
            # 将 data 转换为字符串并写入文件
            f.write(str(data))
        print(f"数据已成功写入文件：{dst_file}")
    except Exception as e:
        print(f"发生错误: {e}")

# 示例：加载 .pkl 文件并将内容写入到 .txt 文件
if __name__ == '__main__':
    pkl_file_path = '/home/zzx/masa/demo/minions_rush_out_outputs_tracking_results.pkl'  # 替换为实际的 .pkl 文件路径
    dst_txt_file = '/home/zzx/masa/demo/dst_txt.txt'  # 替换为目标文本文件路径

    data = load_pkl_file(pkl_file_path)
    
    if data is not None:
        save_data_to_txt(data, dst_txt_file)
