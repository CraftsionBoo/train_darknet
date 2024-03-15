import os 
class Logger(object):
    def __init__(self):
        self._logger = None
    
    def init(self, logdir, name="log"):
        if self._logger == None:
            import logging
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            log_file = os.path.join(logdir, name)
            if os.path.exists(log_file):
                os.remove(log_file)
            self._logger = logging.getLogger()
            self._logger.setLevel("INFO")
            fh = logging.FileHandler(log_file)  # 文件保存
            sh = logging.StreamHandler()        # 终端显示
            self._logger.addHandler(fh)
            self._logger.addHandler(sh)
    
    def info(self, str_info):
        self.init("../logs", "darknet.log")
        self._logger.info(str_info)
logger = Logger()
print = logger.info

import xml.etree.ElementTree as ET 
# 坐标归一化
def convert(size , box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)

# 解析xml  path: xml路径 labels: 全局变量存储类别
def single_xml_analysis(path, label_path, labels):
    tree = ET.parse(path)
    root = tree.getroot()

    labeled = root.find("labeled").text
    if(labeled == "true"):
        size = root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)

        # 图像名
        name_image_path = root.find("path").text
        name_image_info = name_image_path.split("\\")[-1]  # 需要修改位置
        name_image_cut = name_image_info.split(".")
        if(len(name_image_cut) == 2):
            name_image = name_image_cut[0]
        elif(len(name_image_cut) > 2):
            name_image_cut.pop(-1)
            name_image = ".".join(name_image_cut)

        # 图像目录下生成txt
        txt_name_image = name_image + ".txt"
        labelFiles = open(os.path.join(label_path, txt_name_image), "w", encoding="utf-8")

        # 跳过未标注数据
        x_outputs = root.find("outputs")
        x_object = x_outputs.find("object")
        if(x_object.find("item") == None):
            labelFiles.close()
            return None
        
        # 处理bdnbox
        for item in x_object.iter("item"):
            x_name = item.find("name").text
            # 若name不在标签就添加
            if x_name not in labels:
                labels.append(x_name)
            
            x_idx = labels.index(x_name)
            x_bndbox = item.find("bndbox")
            x_b = (
                float(x_bndbox.find("xmin").text),
                float(x_bndbox.find("xmax").text),
                float(x_bndbox.find("ymin").text),
                float(x_bndbox.find("ymax").text)
            )
            x_bb = convert((w, h), x_b)
            labelFiles.write(str(x_idx) + " " + " ".join([str(x_a) for x_a in x_bb]) + "\n")
        labelFiles.close()
        return name_image_info
    else:
        return None
