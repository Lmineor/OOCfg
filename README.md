# The OOCfg 
![](https://img.shields.io/static/v1?label=整体进度&message=50%&color=blue)

![a](https://img.shields.io/static/v1?label=ini&message=support&color=succes)
![a](https://img.shields.io/static/v1?label=yaml&message=support&color=success)
![a](https://img.shields.io/static/v1?label=conf&message=support&color=success)

## 说明

这个模块初步打算用来读取各种配置文件，并可以通过以属性的方式来访问配置项

## 进度

- `.ini` 完成90%

- `.yaml` 完成0%

- `.conf` 完成0%


## 使用说明

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


cfg.set_default_config(group)

print(cfg.CONF.CLASS.school)
# xi wang xiao xue

```

## 参考

[oslo.config](https://github.com/openstack/oslo.config)