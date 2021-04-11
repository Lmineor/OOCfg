# The OOCfg 
![](https://img.shields.io/static/v1?label=整体进度&message=60%&color=blue)
![](https://img.shields.io/static/v1?label=license&message=MIT&color=blue)


![a](https://img.shields.io/static/v1?label=ini&message=support&color=succes)
![a](https://img.shields.io/static/v1?label=yaml&message=support&color=success)
![a](https://img.shields.io/static/v1?label=conf&message=support&color=success)

## 说明

这个模块初步打算用来读取各种配置文件，并可以通过以属性的方式来访问配置项。

属性访问的方式如下：

当按照如下结构注册配置文件时
```ini
[info]
sex: female
name: xiaoming
age: 18
```

代码访问方式为：

```python
cfg.CONF.INFO.name
```

ini配置文件的section名已转换为大写，本例中`info`转换为`INFO`



## 进度

- `.ini` 完成

- `.yaml` 完成90%

- `.conf` 完成90%


## 示例

```python

from oocfg.cfg import cfg
from oocfg.config import options

info_opts = [
    options.StrOpt('name', default='xiao', helper='this is name config'),
    options.IntOpt('age', default=18, helper='this is age config'),
    options.StrOpt('sex', default='female', helper='this is gender config', choices=['female', 'male'])
]

class_opts = [
    options.IntOpt('class', default='6', helper='the class grade'),
    options.StrOpt('school', default='xi wang xiao xue', helper='school name')
]

group = {
    'class': class_opts,
    'info': info_opts
}


file = '/The/path/to/your/config/file/config.ini'
cfg.startup(group, config_file=file)
print(cfg.CONF.CLASS.school)

```

详见测试脚本[test.py](./test.py)

## 参考

[oslo.config](https://github.com/openstack/oslo.config)