#### darknet边缘算力平台部署
数据标注选择精灵标注工具进行标注，在以下边缘算力平台测试
- [x] Jetson NX
- [x] Jetson Agx xaiver
#### 环境
- [x] OpenCV3.2.0 
- [x] OpenCV4.4.0
#### 步骤
1. 解压darknet框架
```bash
# From https://github.com/AlexeyAB/darknet
unzip darknet-master.zip
```
2. 安装OpenCV4.4.0步骤
```bash
# 依赖项安装
sudo apt-get update 
sudo apt-get dist-upgrade -y --autoremove 
sudo apt-get install -y build-essential cmake git gfortran libatlas-base-dev libavcodec-dev libavformat-dev libavresample-dev libcanberra-gtk3-module libdc1394-22-dev libeigen3-dev libglew-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer1.0-dev libgtk-3-dev libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev liblapack-dev liblapacke-dev libopenblas-dev libpng-dev libpostproc-dev libswscale-dev libtbb-dev libtbb2 libtesseract-dev libtiff-dev libv4l-dev libxine2-dev libxvidcore-dev libx264-dev pkg-config python-dev python-numpy python3-dev python3-numpy python3-matplotlib qv4l2 v4l-utils v4l2ucp zlib1g-dev
# 安装QT
sudo apt-get install qt5-default qtcreator -y 
# 安装jtop
sudo apt-get install python3-pip
sudo -H pip3 install -U jetson-stats

# cmake 
cmake -DBUILD_EXAMPLES=OFF -DWITH_NVCUVID=ON -DWITH_QT=ON -DBUILD_opencv_python2=ON -D BUILD_opencv_python3=ON -D CMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/home/nvidia/BOG-configuration/build_opencv/opencv-4.4.0/install -D CUDA_ARCH_BIN=7.2 -D CUDA_ARCH_PTX="" -D CUDA_FAST_MATH=ON -D CUDNN_VERSION='8.0'-D EIGEN_INCLUDE_PATH=/usr/include/eigen3 -D ENABLE_NEON=ON -DOPENCV_DNN_CUDA=ON -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=/home/nvidia/BOG-configuration/build_opencv/opencv_contrib-4.4.0/modules -DOPENCV_GENERATE_PKGCONFIG=ON -D WITH_CUBLAS=ON -D WITH_CUDA=ON -D WITH_CUDNN=ON -DWITH_GSTREAMER=ON -D WITH_LIBV4L=ON -D WITH_OPENGL=ON -D BUILD_PERF_TESTS=OFF -D BUILD_TESTS=OFF 

make -j4/j8
sudo make install 
sudo ldconfig

# 修改pkg-config
cd ${path_opencv_install}/pkgconfig/opencv4.pc
sudo cp opencv4.pc /usr/lib/aarch64-linux-gnu/pkgconfig

# ~/.bashrc添加
export CMAKE_PREFIX_PATH=${root_path}/opencv-4.4.0/install/lib/cmake:$CMAKE_PREFIX_PATH
export PKG_CONFIG_PATH=${root_path}/opencv-4.4.0/install/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=${root_path}/opencv-4.4.0/install/lib:$LD_LIBRARY_PATH
```
3. 安装OpenCV3.2.0步骤
```bash
# opencv3.2.0 : https://github.com/opencv/opencv/releases?page=5
# opencv_contrilb : https://github.com/opencv/opencv_contrib/releases/tag/3.2.0
cd && mkdir -p build_opencv/opencv3.2.0 && mv ${刚下载的两个源码文件} 
tar -zxvf opencv-3.2.0.tar.gz (unzip opencv-3.2.0.zip)
tar -zxvf opencv_contrib-3.2.0.tar.gz (unzip opencv_contrib-3.2.0.zip)
cd opencv-3.2.0 
mkdir build && mkdir install && cd build
cmake -D CMAKE_BUILD_TYPE=Release -D OPENCV_GENERATE_PKGCONFIG=OFF \
-D CMAKE_INSTALL_PREFIX=/home/${用户名}/build_opencv/opencv-3.2.0/install \
-D WITH_CUDA=OFF -D WITH_QT=OFF -D WITH_OPENGL=ON -D WITH_OPENMP=ON  \
-D WITH_V4L=ON -D BUILD_opencv_python2=ON -D BUILD_opencv_python3=ON \
-D EIGEN_INCLUDE_PATH=/usr/include/eigen3 -D WITH_VTK=OFF \
-D OPENCV_EXTRA_MODULES_PATH=${opencv_contrib路径}/opencv_contrib-3.2.0/modules ..
make -j8
# 切换到root权限
sudo make install -j4

# 添加环境变量
vim ~/.bashrc
export PKG_CONFIG_PATH=${opencv3.2路径}/install/lib/pkgconfig
export LD_LIBRARY_PATH=${opencv3.2路径}/install/lib
source ~/.bashrc

# 配置opencv.conf 便于pkg-config --modversion opencv查看
cd /etc/ld.so.conf.d
sudo touch opencv.conf
sudo vim opencv.conf
写入 ${opencv3.2路径}/install/lib
sudo ldconfig

# ~/.bashrc添加
export CMAKE_PREFIX_PATH=${root_path}/opencv-3.2.0/install/lib/cmake:$CMAKE_PREFIX_PATH
export PKG_CONFIG_PATH=${root_path}/opencv-3.2.0/install/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=${root_path}/opencv-3.2.0/install/lib:$LD_LIBRARY_PATH
```
#### 修改darknet配置文件
```bash
GPU=1       
CUDNN=1   
CUDNN_HALF=0  # 半精度
OPENCV=1
AVX=0
OPENMP=0
LIBSO=1   # 动态库，后续进行推理使用
ZED_CAMERA=0
ZED_CAMERA_v2_8=0
# 根据nvidia修改
ARCH= -gencode arch=compute_86,code=[sm_86,compute_86]
# opencv版本修改
LDFLAGS+= `pkg-config --libs opencv3 2> /dev/null || pkg-config --libs opencv`
COMMON+= `pkg-config --cflags opencv3 2> /dev/null || pkg-config --cflags opencv`
```
