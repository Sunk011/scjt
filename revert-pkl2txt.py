# import pickle


# def format_data(data, indent=0):
#     """
#     将数据格式化为适合写入文本文件的字符串，处理嵌套结构。
#     """
#     if isinstance(data, dict):
#         items = []
#         for key, value in data.items():
#             formatted_value = format_data(value, indent + 4)
#             items.append(f'{" " * indent}{key}: {formatted_value}')
#         return "{\n" + ",\n".join(items) + "\n" + " " * indent + "}"
#     elif isinstance(data, list):
#         items = [format_data(item, indent + 4) for item in data]
#         return "[\n" + ",\n".join(items) + "\n" + " " * indent + "]"
#     else:
#         return str(data)


# def pkl_to_txt(pkl_file_path, txt_file_path):
#     try:
#         with open(pkl_file_path, 'rb') as pkl_file:
#             data = pickle.load(pkl_file)
#             formatted_data = format_data(data)
#             with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
#                 txt_file.write(formatted_data)
#     except FileNotFoundError:
#         print(f"文件 {pkl_file_path} 不存在，请检查路径是否正确。")
#     except pickle.UnpicklingError:
#         print(f"读取 {pkl_file_path} 文件时反序列化失败，请确保文件内容格式正确。")
#     except Exception as e:
#         print(f"出现其他错误: {e}")


# if __name__ == "__main__":
#     pkl_file_path = "D:\Workspace\scjt\car_outputs_tracking_results.pkl"  # 替换为实际的.pkl文件路径
#     txt_file_path = "D:\Workspace\scjt\car_outputs_tracking_results.TXT"  # 替换为实际要输出的.txt文件路径
#     pkl_to_txt(pkl_file_path, txt_file_path)
    



# import pickle

# def pkl_to_txt(pkl_file_path, txt_file_path):
#     try:
#         # 读取pkl文件
#         with open(pkl_file_path, 'rb') as pkl_file:
#             data = pickle.load(pkl_file)
        
#         # 将数据写入txt文件
#         with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
#             # 如果数据是列表或字典，每个元素单独一行
#             if isinstance(data, (list, dict)):
#                 for item in data:
#                     txt_file.write(str(item) + '\n')
#             else:
#                 txt_file.write(str(data))
                
#         print(f"转换成功！文件已保存为: {txt_file_path}")
        
#     except Exception as e:
#         print(f"转换过程中出现错误: {str(e)}")

# # 使用示例
# if __name__ == "__main__":
#     pkl_file_path = "D:\Workspace\scjt\car_outputs_tracking_results.pkl"  # 输入pkl文件路径
#     txt_file_path = "D:\Workspace\scjt\car_outputs_tracking_results.txt"  # 输出txt文件路径
    
#     pkl_to_txt(pkl_file_path, txt_file_path)





# import pickle
# import numpy as np

# def load_tracking_results(pkl_file_path):
#     try:
#         # 读取pkl文件
#         with open(pkl_file_path, 'rb') as f:
#             instances_list = pickle.load(f)
        
#         print(f"成功加载文件: {pkl_file_path}")
#         print(f"数据类型: {type(instances_list)}")
#         print(f"列表长度: {len(instances_list)}")  # 通常是视频帧数
        
#         # 解析第一帧数据来查看结构
#         if len(instances_list) > 0:
#             print("\n第一帧数据结构:")
#             first_frame = instances_list[0]
#             for key in first_frame:
#                 print(f"{key}: {type(first_frame[key])}, 形状: {first_frame[key].shape if hasattr(first_frame[key], 'shape') else len(first_frame[key])}")
        
#         return instances_list
        
#     except Exception as e:
#         print(f"加载文件时出错: {str(e)}")
#         return None

# def save_to_txt(instances_list, txt_file_path):
#     try:
#         with open(txt_file_path, 'w', encoding='utf-8') as f:
#             # 遍历每一帧
#             for frame_idx, frame_data in enumerate(instances_list):
#                 f.write(f"帧 {frame_idx}:\n")
#                 # 写入每个键值对的信息
#                 for key, value in frame_data.items():
#                     f.write(f"{key}: {value}\n")
#                 f.write("\n")  # 帧之间添加空行
#         print(f"已将结果保存到: {txt_file_path}")
        
#     except Exception as e:
#         print(f"保存文件时出错: {str(e)}")

# if __name__ == "__main__":
#     # 设置文件路径
#     pkl_file_path = "D:\Workspace\scjt\car_outputs_tracking_results.pkl"  # 替换为你的pkl文件路径
#     txt_file_path = pkl_file_path.replace('.pkl', '_parsed.txt')
    
#     # 加载并解析数据
#     tracking_results = load_tracking_results(pkl_file_path)
    
#     if tracking_results is not None:
#         # 保存解析结果到txt文件
#         save_to_txt(tracking_results, txt_file_path)




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

# 示例：加载 .pkl 文件并打印其内容
if __name__ == '__main__':
    file_path = 'D:\Workspace\scjt\code\car_outputs_tracking_results.pkl'  # 替换为实际的 .pkl 文件路径
    data = load_pkl_file(file_path)
    
    if data is not None:
        print("文件内容：")
        print(data)
