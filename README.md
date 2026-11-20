# 跨时区活动机会账与补偿场次

合作校按班确认每周双语交流机会。时区为 IANA 标识；本地预约的 offset 是已核对的 UTC 偏移，缺省表示来源未作消歧。 数据均为合成。

CSV 使用 UTF-8、首行字段名，`-` 表示来源未填；JSON 使用原生布尔、字符串及数字。没有另行给定时，`seq` 只用于还原各条来件的先后，不是业务日期。

## 来源说明

- `groups.csv`：available.csv 的教学周从当地周一开始；人数是全班保留名额，不可拆班充抵一次。加号分隔的所有语种均需由场次提供。
- `sessions.csv`：start_local 用 host_tz 解释，duration 是实逝分钟。正常场次和补场都只有 hosts 声明的共享容量。
- `invites.csv`：declined 为学校主动谢绝；confirmed 为实际确认；offered 只表收到但未占用名额。更正消息影响当期事实，不隐式撤销历史 confirmed。

## 数据清单

- `groups.csv`：`group`, `school`, `timezone`, `students`, `languages`。
- `available.csv`：`rule`, `group`, `from`, `through`, `weekday`, `start_local`, `end_local`。
- `sessions.csv`：`id`, `host_tz`, `start_local`, `offset`, `duration`, `languages`, `hosts`。
- `invites.csv`：`seq`, `group`, `session`, `kind`, `state`。
- `changes.json`：记录数组。
- `contract.json`：配置对象。

## 本地检查

使用 Python 3.11 标准库，无需安装第三方依赖。构建检查和来源契约测试：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
