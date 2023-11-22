# skland-checkin-python

利用 GitHub Action 自动完成森空岛签到. 基于[Maojuan-lang](https://github.com/Maojuan-lang/SenKongDao)的实现包装, 修改自[Yanstory](https://github.com/Yanstory/skland-checkin-ghaction)和[xxyz30](https://gitee.com/FancyCabbage/skyland-auto-sign).

## How to do

1. fork 本仓库.
2. 点击顶部 Settings 选项卡进入仓库设置.
3. 左侧栏找到 Security 一节，点击展开 Secrets and variables，点击 Actions.
4. 在右侧点击 New repository secret 按钮，新建一个名为``UID``的 secret, 内容为你游戏账号的UID, 在游戏界面的ID下方有一串8位数字(也许是8位).
5. 同样的新建一个名为``TOKEN``的 secret, 内容为你的Hypergryph账号登录凭证 (可通过登录网页端森空岛后，进入[TOKEN获取网页](https://web-api.skland.com/account/info/hg), ``content`` 字段内容即为 ``TOKEN`` ).
6. 点击顶部Action, 开启 Workflow功能<br>默认每日北京时间4:00启动, 可自行修改workflow触发时间, 注意 Action 使用的是 UTC +0 时区, 需要自行转换为东八区时间(东八区时间-8h).
7. (Option)添加钉钉机器人通知, 添加名为``DINGTALKTOKEN``的 secret, 内容为钉钉机器人的webhook的token, 安全选项选择关键字, 添加``森空岛``作为关键词.
8. 注意: 手机端重新登录和清除会话信息会导致``TOKEN``失效(似乎).
