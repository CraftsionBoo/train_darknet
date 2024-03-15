#### darknet边缘算力平台部署
- [x] Jetson NX
- [x] Jetson Agx xaiver
#### 部署环境
OpenCV3.2.0/OpenCV4.4.0测试完成
#### cmd
1. 解压darknet框架
```bash
# From https://github.com/AlexeyAB/darknet
unzip darknet-master.zip
```
2. 安装OpenCV3.2.0/OpenCV4.4.0
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
```
