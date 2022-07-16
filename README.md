# 基于 PaddleDetection 的 SoccerNet 多目标追踪基线
* 中文 | [English](./README_EN.md)

## 1. 介绍
* 一个基于 [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection) 套件和 [SoccerNet Tracking](https://github.com/SoccerNet/sn-tracking) 数据集开发的足球和足球运动员多目标追踪（MOT）的基线

* 包含 DeepSort、ByteTrack、JDE 和 FairMOT 四个经典的多目标追踪模型，模型训练、评估、推理和部署全流程支持

## 2. 演示
* 足球与运动员追踪效果如下：

    ![demo](https://ai-studio-static-online.cdn.bcebos.com/c2e1a47da7c345c4b483367803b1c42c4bfba0984fa046c3ba19630687ac9398)

## 3. 目录
* 本项目目录结构如下：

    * configs -> 模型配置文件

    * dataset -> 数据集下载和预处理脚本

    * tools -> 评估脚本

## 4. 数据
### 4.1 数据简介
* SoccerNet Tracking 追踪数据集由来自主摄像机拍摄的 12 场完整足球比赛组成，包括：

    * 200 个视频剪辑，每段 30 秒，包含跟踪数据

    * 一个完整的半场视频，用跟踪数据标注

    * 12 场比赛的完整视频

### 4.2 数据格式
* 真实值和检测结果存储在逗号分隔的 csv 文件中，共 10 列，如下表格所示：

    |帧 ID（Frame ID）|追踪 ID（Track ID）|包围框左侧坐标（X）|包围框顶部坐标（Y）|包围框宽度（W）|包围框高度（H）|包围框置信度（Score）|未使用（-1）|未使用（-1）|未使用（-1）|
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|

* 数据集符合 MOT20 格式要求，由于某些值未使用，所以被标注为 -1

## 5. 模型
* 模型及其对应的配置文件如下表格所示：

    |模型|论文|配置|
    |:-:|:-:|:-:|
    |DeepSort|[Simple Online and Realtime Tracking with a Deep Association Metric](https://arxiv.org/abs/1703.07402)|[configs](./configs/snmot/deepsort)|
    |ByteTrack|[ByteTrack: Multi-Object Tracking by Associating Every Detection Box](https://arxiv.org/abs/2110.06864)|[configs](./configs/snmot/bytetrack)|
    |JDE|[Towards Real-Time Multi-Object Tracking](https://arxiv.org/abs/1909.12605)|[configs](./configs/snmot/jde)|
    |FairMOT|[FairMOT: On the Fairness of Detection and Re-Identification in Multiple Object Tracking](https://arxiv.org/abs/2004.01888v6)|[configs](./configs/snmot/fairmot)|

## 6. 使用
### 6.1 克隆安装
* 克隆本项目代码：

    ```bash
    $ git clone https://github.com/jm12138/SoccerNet_Tracking_PaddleDetection

    $ cd SoccerNet_Tracking_PaddleDetection

    $ pip install -r requirements.txt
    ```

* 克隆 PaddleDetection 代码：

    ```bash
    $ git clone https://github.com/PaddlePaddle/PaddleDetection
    
    $ cd PaddleDetection

    $ pip install -r requirements.txt
    ```

* 复制文件：

    ```bash
    $ cp -r ../configs ./
    $ cp -r ../dataset ./
    $ cp -r ../tools ./
    ```

### 6.2 数据下载
* 使用下载脚本可以快速下载数据：

    ```bash
    $ cd ./dataset/snmot
    
    $ python download_data.py
    ```

### 6.3 数据解压
* 使用如下命令解压数据：

    ```bash
    $ cd ../../
    $ mkdir ./dataset/snmot/SNMOT/images

    $ unzip -q ./dataset/snmot/SNMOT/tracking/train.zip -d ./dataset/snmot/SNMOT/images
    $ unzip -q ./dataset/snmot/SNMOT/tracking/test.zip -d ./dataset/snmot/SNMOT/images
    $ unzip -q ./dataset/snmot/SNMOT/tracking/challenge.zip -d ./dataset/snmot/SNMOT/images
    ```

### 6.4 数据处理
* 转换数据格式以符合 PaddleDetection 的要求：

    ```bash
    $ cd ./dataset/snmot
    
    $ python gen_labels.py
    $ python gen_image_list.py
    $ python gen_det_coco.py
    $ python gen_det_results.py
    $ python zip_gt.py
    ```

### 6.5 模型训练
* 指定一个模型配置文件，使用如下命令进行模型训练（以 FairMOT 为例）：

    ```bash
    $ cd ../../

    $ python tools/train.py -c ./configs/snmot/fairmot/fairmot_dla34_30e_1088x608.yml 
    ```

### 6.6 模型验证
* 使用如下命令进行模型评估：

    ```bash
    $ python tools/eval_mot.py \
        -c ./configs/snmot/fairmot/fairmot_dla34_30e_1088x608.yml \
        -o weights=./output/fairmot_dla34_30e_1088x608/model_final

    $ cd ./output/mot_results
    
    $ zip soccernet_mot_results.zip *.txt

    $ cd ../../
    
    $ python tools/evaluate_soccernet_v3_tracking.py \
        --BENCHMARK SNMOT \
        --DO_PREPROC False \
        --SEQMAP_FILE tools/SNMOT-test.txt \
        --TRACKERS_TO_EVAL test \
        --SPLIT_TO_EVAL test \
        --OUTPUT_SUB_FOLDER eval_results \
        --TRACKERS_FOLDER_ZIP ./output/mot_results/soccernet_mot_results.zip \
        --GT_FOLDER_ZIP ./dataset/snmot/gt.zip
    ```

### 6.7 模型推理
* 使用如下命令进行模型推理：

    ```bash
    $ python tools/infer_mot.py \
        -c ./configs/snmot/fairmot/fairmot_dla34_30e_1088x608.yml \
        -o weights=./output/fairmot_dla34_30e_1088x608/model_final \
        --image_dir ./dataset/snmot/SNMOT/images/challenge/SNMOT-021/img1 \
        --frame_rate 25 \
        --output_dir ./output \
        --save_videos
    ```

### 6.8 更多详情
* 模型部署和更多使用指南请参考 PaddleDetection 官方文档

## 7. 参考
* 相关链接：

    * [SoccerNet: Soccer Video Understanding Benchmark Suite](https://www.soccer-net.org/home)

    * [SoccerNet Tracking Official Website](https://www.soccer-net.org/tasks/tracking)

    * [SoccerNet Tracking Development Kit](https://github.com/SoccerNet/sn-tracking)

    * [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)

* 论文引用：

    ```BibTeX
    @inproceedings{Wojke2017simple,
        title={Simple Online and Realtime Tracking with a Deep Association Metric},
        author={Wojke, Nicolai and Bewley, Alex and Paulus, Dietrich},
        booktitle={2017 IEEE International Conference on Image Processing (ICIP)},
        year={2017},
        pages={3645--3649},
        organization={IEEE},
        doi={10.1109/ICIP.2017.8296962}
    }

    @article{DBLP:journals/corr/abs-2110-06864,
        title = {ByteTrack: Multi-Object Tracking by Associating Every Detection Box},
        author = {Zhang, Yifu and Sun, Peize and Jiang, Yi and Yu, Dongdong and Weng, Fucheng and Yuan, Zehuan and Luo, Ping and Liu, Wenyu and Wang, Xinggang},
        doi = {10.48550/ARXIV.2110.06864},
        url = {https://arxiv.org/abs/2110.06864},
        publisher = {arXiv},
        year = {2021}
    }

    @article{wang2019towards,
        title={Towards Real-Time Multi-Object Tracking},
        author={Wang, Zhongdao and Zheng, Liang and Liu, Yixuan and Wang, Shengjin},
        journal={arXiv preprint arXiv:1909.12605},
        year={2019}
    }

    @article{zhang2020fair,
        title={FairMOT: On the Fairness of Detection and Re-Identification in Multiple Object Tracking},
        author={Zhang, Yifu and Wang, Chunyu and Wang, Xinggang and Zeng, Wenjun and Liu, Wenyu},
        journal={arXiv preprint arXiv:2004.01888},
        year={2020}
    }
    ```
