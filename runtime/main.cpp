#include "yoloDetector.hpp"
#include <iostream>
#include <unistd.h>
#include <chrono>

#define PRINT_TIME
#define SAVE_VIDEO

int main(int argc, char **argv)
{
    if (argc < 6)
    {
        std::cerr << "User : " << argv[0] << "<main path> <image/video> <cfg> <weights> <classes> <mode>" << std::endl;
        return -1;
    }
    chdir(argv[1]);                                                  // 主目录
    std::string model_cfg = std::string("../config/") + argv[3];     // 模型
    std::string model_weights = std::string("../config/") + argv[4]; // 权重
    std::string class_file = std::string("../config") + argv[5];     // 类别
    std::string image_path = std::string("../") + argv[2];           // 图像或视频
    int mode = std::stoi(argv[6]);                                   // 图像视频标志

    YoLoDetctor *det = new YoLoDetctor(model_cfg, model_weights, class_file, 0, 0.5);
    cv::Mat frame;
    if (mode == 0) // 图像
    {
        frame = cv::imread(image_path);
#ifdef PRINT_TIME
        auto start = std::chrono::high_resolution_clock::now();
#endif
        det->DetectorImage(frame);
#ifdef PRINT_TIME
        auto end = std::chrono::high_resolution_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000.f;
        std::cout << "each frame time(ms): " << elapsed << std::endl;
#endif
        det->DrawerBoxes(frame);
    }
    else if (mode == 1)
    {
        cv::VideoCapture cap;
        cap = cv::VideoCapture(image_path);
#ifdef SAVE_VIDEO
        cv::Size frame_size = cv::Size(cap.get(cv::CAP_PROP_FRAME_WIDTH), cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        double fps = cap.get(cv::CAP_PROP_FPS);
        cv::VideoWriter write("../result.avi", cv::VideoWriter::fourcc('D', 'I', 'V', 'X'), fps, frame_size);
#endif
        while (cap.isOpened())
        {
            cap >> frame;
#ifdef PRINT_TIME
            auto start = std::chrono::high_resolution_clock::now();
#endif
            det->DetectorImage(frame);
#ifdef PRINT_TIME
            auto end = std::chrono::high_resolution_clock::now();
            auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000.f;
            std::cout << "each frame time(ms): " << elapsed << std::endl;
            std::string time_str = "time: " + std::to_string(elapsed);
            std::string fps_str = "fps: " + std::to_string(1000.f / elapsed);
            cv::putText(frame, time_str, cv::Point(50, 50), cv::FONT_HERSHEY_PLAIN, 1.2, cv::Scalar(255, 255, 255), 1);
            cv::putText(frame, fps_str, cv::Point(50, 100), cv::FONT_HERSHEY_PLAIN, 1.2, cv::Scalar(255, 255, 255), 1);
#endif
            det->DrawerBoxes(frame);
#ifdef SAVE_VIDEO
            write.write(frame);
#endif
        }
    }
    delete det;
    return 0;
}
