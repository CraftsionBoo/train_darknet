# Darknet
To train darknet and Inference using the darknet model

### USE
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
# 找到日志输出 train_cmd 复制到终端即可
```
