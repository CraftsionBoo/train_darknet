# Darknet
训练darknet模型和推理

#### USE
1. 构建darknet框架训练格式
```bash
cd utils
# default
python export.py --data_path ../datasets/custom_data --cfg yolov3.cfg --weights darknet53.conv.74
# 选择存储路径 日志路径
python export.py --data_path ../datasets/custom_data --cfg yolov3.cfg --weights darknet53.conv.74 --save_path ${配置文件路径} --logdir ${日志保存路径}
```
2. 输入训练命令
```bash
# 日志输出train_cmd复制
cd .. 
.darknet/darknet detector train ../logs/train.data ../assets/yolov3.cfg ../assets/darknet53.conv.74 -dont_show
```
3. 推理
```bash
cd ..
cmake -S . -B build
cmake --build build
./bin/detector <image_path> ./assets/yolov3.cfg ./logs/yolov3_best.weights ./logs/train.names 0
./bin/detector <video_path> ./assets/yolov3.cfg ./logs/yolov3_best.weights ./logs/train.names 1
```
