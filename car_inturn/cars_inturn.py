# import numpy as np
# import cv2
# # 定义检测线段

# # 读取txt文件并解析
# def read_annotations(file_path):
#     data = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             frame_id, target_id, x, y, w, h = map(int, line.strip().split(',')[:-4])
#             if frame_id not in data:
#                 data[frame_id] = []
#             # 计算目标中心点
#             center_x = x + w // 2
#             center_y = y + h // 2
#             data[frame_id].append({"traget": target_id, "center": (center_x, center_y)})
#     return data

# # 判断线段相交逻辑
# def line_intersection(p1, p2, q1, q2):
#     def cross_product(a, b):
#         return a[0] * b[1] - a[1] * b[0]
    
#     def subtract_points(a, b):
#         return (a[0] - b[0], a[1] - b[1])
    
#     r = subtract_points(p2, p1)
#     s = subtract_points(q2, q1)
#     denom = cross_product(r, s)
    
#     if denom == 0:
#         return None  # 平行或共线
    
#     t = cross_product(subtract_points(q1, p1), s) / denom
#     u = cross_product(subtract_points(q1, p1), r) / denom
    
#     if 0 <= t <= 1 and 0 <= u <= 1:
#         # 计算交点坐标
#         intersection = (p1[0] + t * r[0], p1[1] + t * r[1])
#         return intersection
#     return None

# # 检查目标是否经过线段并记录交点和顺序
# def check_crossing(data, line_start, line_end):
#     crossings = []
#     crossed_targets = set()  # 用于记录已相交的目标 ID
#     for target_id, trajectory in data.items():
#         if target_id in crossed_targets:
#             continue  # 如果目标已经相交，跳过后续检测
#         for i in range(1, len(trajectory)):
#             p1 = trajectory[i - 1]["center"]
#             p2 = trajectory[i]["center"]
#             intersection = line_intersection(line_start, line_end, p1, p2)
#             if intersection:
#                 crossings.append({
#                     "target_id": target_id,
#                     "frame": trajectory[i]["frame"],
#                     "intersection": intersection
#                 })
#                 crossed_targets.add(target_id)  # 记录目标已相交
#                 break  # 找到第一次相交后直接跳出当前目标的检测
#     # 按帧号排序
#     crossings.sort(key=lambda x: x["frame"])
#     return crossings

# if __name__ == "__main__":
#     id_right=set()
#     line_start = (285, 800)
#     line_end = (570, 800)

#     # 主逻辑
#     file_path = "E:/a_lab_show/mot测试视频/car_inturn_res.txt"  # 替换为你的文件路径
#     annotations = read_annotations(file_path)
#     crossings = check_crossing(annotations, line_start, line_end)
#     mp4_path = "E:/a_lab_show/mot测试视频/video1.avi"  # 替换为你的视频路径
#     video = cv2.VideoCapture(mp4_path)
#     idx = 0
#     while video.isOpened():
        
#         ret, frame = video.read()
#         if not ret:
#             break
#         idx = idx+1
#         if idx in annotations:
#             for target in annotations[idx]:
#                 target_id = target["traget"]
#                 center = target["center"]
#                 if target_id in crossings:
#                     cv2.circle(frame, center, 5, (0, 0, 255), -1)
#         # 在这里处理每一帧，例如显示帧
#         cv2.rectangle(frame, (line_start[0], line_start[1]), (line_end[0], line_end[1]), (255, 0, 0), 2)
#         cv2.imshow('Frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     # 输出结果
#     print("Crossing Information:")
#     for crossing in crossings:
#         print(f"Target ID: {crossing['target_id']}, Frame: {crossing['frame']}, Intersection: {crossing['intersection']}")
        





# 读取标注信息

# def read_annotations(file_path):
#     data = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             frame_id, target_id, x, y, w, h = map(int, line.strip().split(',')[:-4])
#             if frame_id not in data:
#                 data[frame_id] = []
#             # 添加目标信息
#             data[frame_id].append({
#                 "target_id": target_id,
#                 "center": (x + w // 2, y + h // 2),
#                 "bbox": (x, y, w, h)
#             })
#     return data

# # 判断线段相交逻辑
# def line_intersection(p1, p2, q1, q2):
#     def cross_product(a, b):
#         return a[0] * b[1] - a[1] * b[0]
    
#     def subtract_points(a, b):
#         return (a[0] - b[0], a[1] - b[1])
    
#     r = subtract_points(p2, p1)
#     s = subtract_points(q2, q1)
#     denom = cross_product(r, s)
    
#     if denom == 0:
#         return None  # 平行或共线
    
#     t = cross_product(subtract_points(q1, p1), s) / denom
#     u = cross_product(subtract_points(q1, p1), r) / denom
    
#     if 0 <= t <= 1 and 0 <= u <= 1:
#         return True  # 相交
#     return False

# # 主处理逻辑
# def display_video(video_path, annotations_path):
#     # 读取标注信息
#     annotations = read_annotations(annotations_path)

#     # 打开视频文件
#     cap = cv2.VideoCapture(video_path)

#     # 记录经过线段的目标 ID
#     crossed_targets = set()

#     frame_index = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # 获取当前帧的标注
#         current_annotations = annotations.get(frame_index, [])
        
#         for i, obj in enumerate(current_annotations):
#             target_id = obj["target_id"]
#             center = obj["center"]

#             # 如果目标已经跨过线段，则跳过
#             if target_id in crossed_targets:
#                 continue

#             # 检查目标是否跨过线段
#             if i > 0:
#                 prev_center = current_annotations[i - 1]["center"]
#                 if line_intersection(prev_center, center, line_start, line_end):
#                     crossed_targets.add(target_id)

#             # 绘制目标的边界框和 ID
#             x, y, w, h = obj["bbox"]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(frame, f"ID: {target_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#         # 显示经过线段的所有目标 ID
#         cv2.putText(frame, f"Crossed Targets: {', '.join(map(str, crossed_targets))}", (50, 50), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
#         # 绘制检测线段
#         cv2.line(frame, line_start, line_end, (0, 0, 255), 2)
#         cv2.line(frame, (373,136), (457, 490), (0, 0, 255), 2)

#         # 实时显示当前帧
#         cv2.imshow("Processed Video", frame)
#         frame_index += 1

#         # 按 'q' 键退出
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # 释放资源
#     cap.release()
#     cv2.destroyAllWindows()



# line_start = (285, 800)
# line_end = (570, 800)
# # 输入路径
# video_path = "E:/a_lab_show/mot测试视频/video1.avi"  # 输入视频文件
# annotations_path = "E:/a_lab_show/mot测试视频/car_inturn_res.txt"  # 标注信息文件

# # 运行处理
# display_video(video_path, annotations_path)




import cv2
import numpy as np

# 定义检测线段
line_start = (285, 600)
line_end = (570, 600)

# 定义两个车辆 ID 集合
group_a = {1, 2 , 7,11,10, 20}  # 集合 A
group_b = {5, 4, 9,22}  # 集合 B
last_group = None
# 记录通过线段的车辆顺序和状态
crossed_order = []  # 按顺序记录通过线段的车辆 ID
crossed_targets = set()  # 记录已经通过的车辆 ID
vehicle_status = {}  # 记录每辆车的状态

# 判断是否交替通行
def is_alternating(target_id, group_a, group_b):
    # last_group = None
    global last_group
    if target_id in group_a:
        if last_group == "A":  # 连续两个 A，违规
            # last_group = "A"
            return False
        last_group = "A"
    elif target_id in group_b:
        if last_group == "B":  # 连续两个 B，违规
            # last_group = "B"
            return False
        last_group = "B"
    return True

# 判断线段相交逻辑
def line_intersection(p1, p2, q1, q2):
    def cross_product(a, b):
        return a[0] * b[1] - a[1] * b[0]
    
    def subtract_points(a, b):
        return (a[0] - b[0], a[1] - b[1])
    
    r = subtract_points(p2, p1)
    s = subtract_points(q2, q1)
    denom = cross_product(r, s)
    
    if denom == 0:
        return None  # 平行或共线
    
    t = cross_product(subtract_points(q1, p1), s) / denom
    u = cross_product(subtract_points(q1, p1), r) / denom
    
    if 0 <= t <= 1 and 0 <= u <= 1:
        # 计算交点坐标
        intersection = (p1[0] + t * r[0], p1[1] + t * r[1])
        return intersection
    return None

# 读取标注文件
def read_annotations(file_path):
    annotations = {}
    with open(file_path, 'r') as file:
        for line in file:
            frame_id, target_id, x, y, w, h = map(int, line.strip().split(',')[:-4])
            if frame_id not in annotations:
                annotations[frame_id] = []
            annotations[frame_id].append({"id": target_id, "x": x, "y": y, "w": w, "h": h})
    return annotations

# 主函数
def process_video(video_path, annotation_path):
    # 读取标注数据
    global last_group
    annotations = read_annotations(annotation_path)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # 绘制检测线
        cv2.line(frame, line_start, line_end, (0, 255, 0), 2)

        # 检查当前帧是否有标注数据
        if frame_id in annotations:
            for obj in annotations[frame_id]:
                target_id = obj["id"]
                x, y, w, h = obj["x"], obj["y"], obj["w"], obj["h"]
                center = (x + w // 2, y + h // 2)

                # 绘制目标矩形和中心点
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # 如果目标已经通过，不再检测
                if target_id in crossed_targets:
                    continue

                # 检测是否与线段相交
                for prev_obj in annotations.get(frame_id - 1, []):
                    if prev_obj["id"] == target_id:
                        prev_center = (prev_obj["x"] + prev_obj["w"] // 2, prev_obj["y"] + prev_obj["h"] // 2)
                        intersection = line_intersection(prev_center, center, line_start, line_end)
                        if intersection:
                            crossed_targets.add(target_id)
                            crossed_order.append(target_id)
                            # 判断车辆是否违规
                            if is_alternating(target_id, group_a, group_b):
                                vehicle_status[target_id] = "normal"
                                
                            else:
                                vehicle_status[target_id] = "abnormal"
                            # print(last_group)
                            break

        # 在每辆车上显示状态
        for obj in annotations[frame_id]:
            target_id = obj["id"]
            if target_id in vehicle_status:
                status = vehicle_status[target_id]
                status_color = (0, 255, 0) if status == "normal" else (0, 0, 255)
                cv2.putText(frame, "  "+f" {status}", (obj["x"], obj["y"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

        # 显示视频帧
        cv2.imshow("Traffic Monitoring", frame)
        cv2.imwrite("D:/桌面/File/实验室/四川交投/code/car_inturn/"+str(frame_id)+".jpg", frame)
        if cv2.waitKey(1000 // fps) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


import cv2
import math

# 配置参数
diagonal_length_real = 5.0  # 车辆对角线实际长度（米）
fps = 30  # 视频帧率

# 读取标注数据
def read_annotations(file_path):
    annotations = {}
    with open(file_path, 'r') as f:
        for line in f:
            frame_id, obj_id, x, y, w, h = map(int, line.strip().split(',')[:-4])
            frame_id, obj_id = int(frame_id), int(obj_id)
            if frame_id not in annotations:
                annotations[frame_id] = []
            annotations[frame_id].append((obj_id, x, y, w, h))
    return annotations

# 计算速度
def calculate_speed(annotations):
    speeds = {}  # 存储每个目标在每一帧的速度
    prev_positions = {}  # 上一帧的中点位置

    for frame_id, objects in annotations.items():
        speeds[frame_id] = []
        for obj_id, x, y, w, h in objects:
            center_x, center_y = x + w / 2, y + h / 2
            diagonal_length_pixels = math.sqrt(w**2 + h**2)

            if obj_id in prev_positions:
                prev_x, prev_y = prev_positions[obj_id]
                pixel_distance = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
                real_distance = (pixel_distance / diagonal_length_pixels) * diagonal_length_real
                speed = real_distance * fps  # 米每秒
            else:
                speed = 0  # 初始帧速度为0

            speeds[frame_id].append((obj_id, speed))
            prev_positions[obj_id] = (center_x, center_y)
    return speeds

# 在图像上绘制标注框和速度
def draw_annotations(image, annotations, speeds, frame_id):
    if frame_id in annotations:
        for (obj_id, x, y, w, h), (_, speed) in zip(annotations[frame_id], speeds[frame_id]):
            x, y, w, h = int(x), int(y), int(w), int(h)
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            text = f"{speed*3.6:.2f} km/h"
            if obj_id==38:
                text = f"{speed*1.8:.2f} km/h"
            cv2.putText(image, text, (x, y -30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (204, 51, 51),2)

# 主程序
def main(video_path, annotations_path, output_path):
    annotations = read_annotations(annotations_path)
    speeds = calculate_speed(annotations)

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 26, (int(cap.get(3)), int(cap.get(4))))

    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id in annotations:
            draw_annotations(frame, annotations, speeds, frame_id)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()

# 调用主程序
# video_path = "E:/a_lab_show/mot测试视频/car_inturn_normal.mp4" # 输入视频路径
# annotations_path = "E:/a_lab_show/mot测试视频/car_inturn_res.txt"   # 标注数据路径
# output_path = "E:/a_lab_show/mot测试视频/speed_video.avi"  # 输出视频路径


video_path = "D:/桌面/File/实验室/四川交投/code/car_inturn/car_inturn_normal.mp4" # 输入视频路径
annotations_path = "D:/桌面/File/实验室/四川交投/code/car_inturn/car_inturn_res.txt"   # 标注数据路径
output_path = "D:/桌面/File/实验室/四川交投/code/car_inturn/speed_video.avi"  # 输出视频路径

main(video_path, annotations_path, output_path)
 
# 调用主函数
# video_path = "E:/a_lab_show/mot测试视频/car_inturn_normal.mp4"  # 输入视频文件
# annotation_path = "E:/a_lab_show/mot测试视频/car_inturn_res.txt"  # 标注信息文件
# process_video(video_path, annotation_path)



# import cv2
# import numpy as np

# line_start = (285, 600)
# line_end = (570, 600)
# group_a = {1, 2 , 7,11,10, 20}  # 集合 A
# group_b = {5, 4, 9,22}  # 集合 B
# # 记录通过线段的车辆顺序和状态
# crossed_order = []  # 按顺序记录通过线段的车辆 ID
# crossed_targets = set()  # 记录已经通过的车辆 ID
# processed_targets = set()  # 记录已经判断状态的车辆 ID
# vehicle_status = {}  # 记录每辆车的状态

# # 判断是否交替通行
# def is_alternating(crossed_order, group_a, group_b):
#     last_group = None
#     for target_id in crossed_order:
#         if target_id in group_a:
#             if last_group == "A":  # 连续两个 A，违规
#                 return False
#             last_group = "A"
#         elif target_id in group_b:
#             if last_group == "B":  # 连续两个 B，违规
#                 return False
#             last_group = "B"
#     return True

# # 判断线段相交逻辑
# def line_intersection(p1, p2, q1, q2):
#     def cross_product(a, b):
#         return a[0] * b[1] - a[1] * b[0]
    
#     def subtract_points(a, b):
#         return (a[0] - b[0], a[1] - b[1])
    
#     r = subtract_points(p2, p1)
#     s = subtract_points(q2, q1)
#     denom = cross_product(r, s)
    
#     if denom == 0:
#         return None  # 平行或共线
    
#     t = cross_product(subtract_points(q1, p1), s) / denom
#     u = cross_product(subtract_points(q1, p1), r) / denom
    
#     if 0 <= t <= 1 and 0 <= u <= 1:
#         # 计算交点坐标
#         intersection = (p1[0] + t * r[0], p1[1] + t * r[1])
#         return intersection
#     return None

# # 读取标注文件
# def read_annotations(file_path):
#     annotations = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             frame_id, target_id, x, y, w, h = map(int, line.strip().split(',')[:-4])
#             if frame_id not in annotations:
#                 annotations[frame_id] = []
#             annotations[frame_id].append({"id": target_id, "x": x, "y": y, "w": w, "h": h})
#     return annotations

# # 主函数
# def process_video(video_path, annotation_path):
#     # 读取标注数据
#     annotations = read_annotations(annotation_path)

#     # 打开视频
#     cap = cv2.VideoCapture(video_path)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

#         # 绘制检测线
#         cv2.line(frame, line_start, line_end, (0, 255, 0), 2)

#         # 检查当前帧是否有标注数据
#         if frame_id in annotations:
#             for obj in annotations[frame_id]:
#                 target_id = obj["id"]
#                 x, y, w, h = obj["x"], obj["y"], obj["w"], obj["h"]
#                 center = (x + w // 2, y + h // 2)

#                 # 绘制目标矩形和中心点
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                 cv2.circle(frame, center, 5, (0, 0, 255), -1)

#                 # 如果目标已经通过且已经处理过，不再检测
#                 if target_id in processed_targets:
#                     continue

#                 # 检测是否与线段相交
#                 for prev_obj in annotations.get(frame_id - 1, []):
#                     if prev_obj["id"] == target_id:
#                         prev_center = (prev_obj["x"] + prev_obj["w"] // 2, prev_obj["y"] + prev_obj["h"] // 2)
#                         intersection = line_intersection(prev_center, center, line_start, line_end)
#                         if intersection:
#                             crossed_targets.add(target_id)
#                             crossed_order.append(target_id)
#                             # 判断车辆是否违规
#                             if is_alternating(crossed_order, group_a, group_b):
#                                 vehicle_status[target_id] = "normal"
#                             else:
#                                 vehicle_status[target_id] = "abnormal"
#                             # 将目标标记为已处理
#                             processed_targets.add(target_id)
#                             break

#         # 在每辆车上显示状态
#         for obj in annotations[frame_id]:
#             target_id = obj["id"]
#             if target_id in vehicle_status:
#                 status = vehicle_status[target_id]
#                 status_color = (0, 255, 0) if status == "normal" else (0, 0, 255)
#                 cv2.putText(frame, "  "+f"{status}", (obj["x"], obj["y"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

#         # 显示视频帧
#         cv2.imshow("Traffic Monitoring", frame)
#         if cv2.waitKey(1000 // fps) & 0xFF == ord("q"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # 调用主函数
# video_path = "E:/a_lab_show/mot测试视频/video1.avi"  # 输入视频文件
# annotation_path = "E:/a_lab_show/mot测试视频/car_inturn_res.txt"  # 标注信息文件
# process_video(video_path, annotation_path)
