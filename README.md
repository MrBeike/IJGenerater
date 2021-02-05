# 🧰 IJGenerater

## 简介

金融基础数据采集报表辅助工具，依据《金融基础数据采集规范》对金融机构的金融基础数据报表进行上报前处理，包括身份信息脱敏、特定小数位处理等。

## 申明

本程序仅为方便部分手工制作报文单位使用，使用单位请报送前请检查数据准确性与合规性，本程序不对数据准确性与合规性负责。使用即代表知悉并同意本申明。

## 警告

- 偶然发现身份信息脱敏处理因表格格式不统一而存在 Bug,因为手中验证表格不多而无法确定。
- 最新版 rule 中未加入身份脱敏函数规则(idMask),因为解析报表规范文件存在困难。

## 使用

目前 GUI 还未制作，入口为 _main.py_

1. `python main.py`
2. 当提示输入 Excel 路径时候，将要处理的文件拖入窗口。

## 流程

读取 Excel 文件 >> 根据规则处理数据（_rule.dict_ ,_confighanlder.py_）>> 保存处理好的数据为 dat 文件(_datWriter.py_) >> 根据 dat 文件生成对应的 log 文件（_logWriter.py_） >> 将生成好的文件存入压缩包（_zipFile.py_）

## 进展

### API

- [x] Excel 报表读取
- [ ] 规则处理函数
  - [x] 规则文件写入保存
  - [x] 规则函数编写
  - [ ] 规则列表完善
- [x] 保存 dat 文件
- [x] 生成 log 文件
- [x] 生成压缩包
- [ ] 清理工作空间或设置子空间？

### GUI

- [ ] UI 设计
- [ ] slot 函数定义

## 待解决/计划

- 加入错误提示功能（错误日志？）
- 已知报表中日期格式数据填错时（1900-01-01），获取的数据为 datetime.time 类型（正常为 datetime.date），无法进行 datetime.strftime()处理.
- 合并两个项目，将金数表单融入单个项目.

## 赞赏

如果你觉得这个工具很赞,可以赞赏作者给予鼓励。（下次一定也 OK:joy:）

<img src="resource\\donate.png">

## 红楼一梦

            春梦随云散
            飞花逐水流
            寄言众儿女
            何必觅闲愁

---

Hope you get your own happines,sincerely.

---

Cause I know it's hard, but it worths.

---
