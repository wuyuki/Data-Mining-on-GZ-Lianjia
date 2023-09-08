## 项目简介

本项目于2023年5月至7月每月初爬取链家网广州（https://gz.lianjia.com/ershoufang） 二手房数据作为本项目数据集，尝试对广州市二手房价格进行建模，并通过建立的模型预测广州市二手房价格。

## 项目目录

```
base
│  main.py                  // 主程序入口
│  requirements.txt
│ 
├─data
│      data.sqlite          // 原始数据库
│      backup.csv           // 数据库备份文件
│      res.csv              // 预处理得到的数据文件
│      spider.py            // 爬虫文件
│      
├─pretreatment
│  │  building.py           // 处理属性building
│  │  direction.py          // 处理属性direction
│  │  encoding.py           // 处理特征编码
│  │  floor.py              // 处理属性floor
│  │  model.py              // 处理属性model（包括rooms 和living_rooms）
│  │  overview.py           // 浏览原始数据的相关信息
│  │  pretreat.py           // 预处理函数入口
│  │  
│  └─__pycache__
│          
├─train
│  │  train.py              // 训练函数入口
│  │  
│  └─__pycache__
│            
└─report
   │ report.md              // 项目报告
   │  
   └─ img                    // 报告静态图片
```

## 启动方法

安装 requirements 后，运行 main.py 文件即可启动