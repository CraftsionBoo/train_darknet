#ifndef __YOLO_DETECTOR_HPP_
#define __YOLO_DETECTOR_HPP_
#define OPENCV

#include <opencv2/opencv.hpp>
#include "../darknet/include/yolo_v2_class.hpp"
#include <fstream>
#include <string>
#include <vector>

class YoLoDetctor
{
public:
    YoLoDetctor(std::string cfg_filename, std::string weight_filename, std::string classes_file,
                int gpu_id = 0, float thresh = 0.5)
        : detector{cfg_filename, weight_filename, gpu_id},
          classes_file_{classes_file},
          thresh_(thresh)
    {
        std::ifstream ifs(classes_file_.c_str());
        std::string line;
        while (getline(ifs, line))
            classes_v_file.push_back(line);
    }

    void DetectorImage(cv::Mat &img)
    {
        std::shared_ptr<image_t> detImg = detector.mat_to_image_resize(img);
        yolo_outs_ = detector.detect_resized(*detImg, img.cols, img.rows, thresh_);
    }

    void DrawerBoxes(cv::Mat &frame)
    {
        if (yolo_outs_.empty())
        {
            printf("The target boxes was not detected\n");
            return;
        }
        for (size_t i = 0; i < yolo_outs_.size(); i++)
        {
            int left = yolo_outs_[i].x;
            int top = yolo_outs_[i].y;
            int right = yolo_outs_[i].x + yolo_outs_[i].w;
            int bottom = yolo_outs_[i].y + yolo_outs_[i].h;

            cv::rectangle(frame, cv::Point(left, top), cv::Point(right, bottom), cv::Scalar(102, 211, 255), 1);
            std::string label = cv::format("%.2f", yolo_outs_[i].prob);
            if (!classes_v_file.empty())
            {
                CV_Assert(yolo_outs_[i].obj_id < (int)classes_v_file.size());
                label = classes_v_file[yolo_outs_[i].obj_id] + ":" + label;
            }
            int baseline;
            cv::Size labelSize = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseline);
            top = cv::max(top, labelSize.height);
            cv::rectangle(frame, cv::Point(left, top - round(1.5 * labelSize.height)), cv::Point(left + round(1.5 * labelSize.width), top + baseline), cv::Scalar(255, 255, 255), cv::FILLED);
            cv::putText(frame, label, cv::Point(left, top), cv::FONT_HERSHEY_SIMPLEX, 0.75, cv::Scalar(0, 0, 0), 1);
        }
    }
private:
    Detector detector;
    std::vector<std::string> classes_v_file;
    std::vector<bbox_t> yolo_outs_;
    std::string classes_file_;
    float thresh_;
};
#endif
