# dictbox

#### 介绍
最新移步：https://pypi.org/project/lazysdk/

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install dictbox
```
2.  pip安装（使用阿里镜像加速）
```shell script
pip install dictbox -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import dictbox
test_dict = {
    'aaa': 'aaa',
    'bbb': 'bbb',
    'ccc': {
        'aa': 'aa'
    }
}
test_res = dictbox.dict_tiler(test_dict)
```
