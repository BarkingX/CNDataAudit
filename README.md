# CNDataAudit
信息资源管理与大数据管理课程作业

**文件目录说明：**

​	CNDataAudit: scrapy项目，爬取数据集，自编元数据目录

​	aduitor.ipynb: 数据集质量分析，理论上继承specific_province_data_spider稍加修改，可以实现对辽宁，山东，四川，宁夏，广西五省的数据集爬取，但除四川外，要么受限于javascript动态加载，要么数据集数量太少。

​	vocabulary.ipynb: 可视化分析各省级行政区主题词汇表

​	vocabulary_generator.ipynb: 手动录入词汇表信息，json格式保存


使用数据源：[四川公共数据开放网](https://www.scdata.net.cn/)

中华人民共和国.geojson文件来自: [阿里云数据可视化平台 DataV.GeoAtlas](https://datav.aliyun.com/portal/school/atlas/area_selector)
