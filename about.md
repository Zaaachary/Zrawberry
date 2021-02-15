# 补充说明

注意事项

## 部署

1. 解压静态文件

2. 配置 setting.py 区分linux windows

3. 迁移数据库
    - 每个 app 下要有 migrations 文件夹，且里面有 __init__.py
    - 可以使用命令 `python manage.py makemigrations --empty [appname]` 来代替
    - `createsuperuser`
