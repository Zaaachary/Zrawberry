#! -*- encoding:utf-8 -*-
"""
@File    :   migrate.py
@Author  :   Zachary Li
@Contact :   li_zaaachary@163.com
@Dscpt   :   django migrations
"""


import os

apps = ['account', 'image', 'navigation', 'article']

os.chdir('Zrawberry2020/')

for app in apps:
    os.system(f"python manage.py makemigrations --empty {app}")

cmds = ["makemigrations", "migrate", "createsuperuser"]
for cmd in cmds:
    os.system(f"python manage.py {cmd}")
