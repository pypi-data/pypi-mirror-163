spapp
=====

介绍
----

使用算盘部署非流计算节点时，可以用 spapp 来获得节点的配置信息，包括

1. user_id, app_id, node_id 等环境变量
2. 右面板的参数配置
3. 模板的 graph 信息

安装
----

.. code-block:: text

    pip install spapp

Usage
-----

获取环境变量

.. code-block:: python

    from spapp import env

    if __name__ == "__main__":
        print('user_id', env.user_id)
        print('app_id', env.app_id)

获取右面板参数，`single_text` 是右面板参数的名字

.. code-block:: python

    from spapp import params

    if __name__ == "__main__":
        print('single_text', params.get('single_text'))

支持
----

如果有使用问题或者有其他微服务方面的需求，欢迎联系 mocheng.lgy@xuelangyun.com
