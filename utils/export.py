import argparse
import os
import tqdm
import utils

# cmd : python3 export.py --data_path ${精灵标注数据文件夹} --cfg ${yolov3 v4 v4-tiny等模型参数} --weights ${预训练权重}
parser = argparse.ArgumentParser(description="darknet datasets")
parser.add_argument("--model_path", default='../assets', help="darknet model cfg path")
parser.add_argument("--data_path", default=None, help="datasets path")
parser.add_argument("--save_path", default='../logs', help="weights save path")
parser.add_argument("--cfg", default=None, help="darknet model config[yolov3.cfg]")
parser.add_argument("--weights", default=None, help="darknet model config[yolov3.cfg]")
parser.add_argument('--logdir', default='../logs', help='folder to save to the log')
parser.add_argument("--folder", default=None, help='Separate folders store the existing data')
args = parser.parse_args()

# logger
if not os.path.exists(args.logdir):
    print("Creating new folder {}".format(args.logdir))
    os.makedirs(args.logdir)
print = utils.logger.info

print("------------- start export labels and configs-------------")
### 生成配置文件  
"""
    ------${model_path}           模型以及预训练权重
            ---- yolo.cfg
            ---- yolo.weights
    ------${data_path}
            ---- output           xml路径
            ---- image.png ...
            ---- image.txt ...    归一化坐标位置和类别
    ------${save_path}
            ---- backup           权重保存
                ---- yolo_1000.weights
                ---- yolo_2000.weights
                ...
            ---- train.txt        图像路径目录
            ---- train.data       模型训练加载配置文件，包含类别，路径等
            ---- train.names      识别类别
"""
if not os.path.exists(args.save_path):
    print("Creating new folder {}".format(args.save_path))
    os.makedirs(args.save_path)

file_train_txt = os.path.join(args.save_path, "train.txt")
file_train_data = os.path.join(args.save_path, "train.data")
file_train_names = os.path.join(args.save_path, "train.names")
# 权重
weights_save_path = os.path.join(args.save_path, "backup") 
if not os.path.exists(weights_save_path):
    os.mkdir(weights_save_path)
# xml路径
output_xml_dir = os.path.join(args.data_path, "outputs")

# train.txt 
lables = []
with open(file_train_txt, "w", encoding="utf-8") as f:
    for xml_name in tqdm.tqdm(os.listdir(output_xml_dir), desc="train"):
        xml_path = os.path.join(output_xml_dir, xml_name)
        name_image = utils.single_xml_analysis(xml_path, args.data_path, lables) 
        if (name_image == None):
            continue
        else:
            image_path = os.path.join(args.data_path, name_image)  
            f.write(image_path + "\n")
print("Data generation completed. All classes : {}\n".format(lables))

# train.names
with open(file_train_names, "w", encoding="utf-8") as f:
    for label in lables:
        f.write(label + "\n")
        
# train.data 
with open(file_train_data, "w", encoding="utf-8") as f:
    f.write("classes=" + str(len(lables)) + "\n")
    f.write("train = " + file_train_txt + "\n")
    f.write("names = " + file_train_names + "\n")
    f.write("backup = " + weights_save_path + "\n")
    
print("----------------- Generate output command -----------------")
cfg_path = os.path.join(args.model_path, args.cfg)
weights_path = os.path.join(args.model_path, args.weights)
train_cmd = "./darknet detector train " + file_train_data + " " + cfg_path + " " + weights_path + " -dont_show"
print(train_cmd)

# 单独文件夹存储
if args.folder is not None:
    import shutil
    new_train_txt = os.path.join(project_dir,"train.txt")
    new_train_names = os.path.join(project_dir, "train.names")
    shutil.copyfile(file_train_txt, new_train_txt)
    shutil.copyfile(file_train_names, new_train_names)
    if not os.path.exists(os.path.join(project_dir, "backup")):
        os.mkdir(os.path.join(project_dir , "backup"))
    with open(os.path.join(project_dir, "train.data"), "w", encoding="utf-8") as f:
        f.write("classes=" + str(len(lables)) + "\n")
        f.write("train = " + new_train_txt + "\n")
        f.write("names = " + new_train_names + "\n")
        f.write("backup = " + os.path.join(project_dir , "backup") + "\n")
    train_cmd = "../darknet/darknet detector train " + os.path.join(project_dir, "train.data") + " " + cfg_path + " " + weights_path + "-dont_show"
    print(train_cmd)
