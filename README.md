# 巡展主题触达与无障碍导览重排

所有记录都是本地合成数据。CSV 为 UTF-8 且有首行字段名；JSON 空值表示未报告。

## 补充来源说明

- `venues.json`：展馆分工作日开放的通行图。moves 的各项依次为起点、终点、步行分钟、是否无障碍、每 15 分钟最大通过人数。open、close、counter_ticks 各项以实际时段分钟编号；班团的 group 是方位观测采用的对象。
- `observations.json`：visit 是点位观测号而非队伍号。group 若缺失，candidate 是可连接的上一个点位；计数为分方向经过人数，可含回访。selected 表示入口抽样已入样，prob 是队伍抽中概率；seen_area 不是抽样区域以外的推断。
- `booking_and_readback.json`：预约和场馆导视交接。已售队伍有固定集合时段，必须停靠 stops；open-plan 只是布置确认，之后当天实况的 installed 才可用于归因。
- `zone_rollout.json`：入口导视（`entrance_sign`）和厅内陈列（`hall_install`）分开回传。布置已接单的记录不证明展品已移；同区域同一时段以当时已知的较晚实况为准，局部实况优先于整馆报送。`window` 为活动相对分钟、左闭右开，`at`/`known_at` 是场馆收到证件的班次标记。`staging_occupancy` 是该布局搬展期间实际扣减的定向通行位（每 15 分钟），与观众本身的通行占位共账。

## 本地检查

使用 Python 3.11 标准库。当前可运行的是来源契约检查：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
