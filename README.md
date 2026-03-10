# Jinshi Pusher Plugin for AstrBot

一个为 AstrBot 设计的金十数据快讯推送插件。

## 功能

- **自动推送**：定时轮询金十数据 RSS，发现新消息自动发送到指定平台和目标 ID。
- **手动查询**：通过指令 `/jin10` 获取最新的一条快讯。
- **开关控制**：通过指令 `/jin10_push on/off` 随时开启或关闭推送服务。
- **灵活配置**：支持在 WebUI 中配置目标 ID、平台、轮询间隔等。

## 安装

1. 将 `jinshi_pusher` 文件夹放入 AstrBot 的 `plugins` 目录下。
2. 安装依赖：`pip install feedparser`
3. 重启 AstrBot。

## 配置项

在 AstrBot 管理面板中可以找到以下配置：

- `target_id`: 接收消息的目标 ID（如 QQ 群号、频道 ID 等）。
- `platform`: 消息平台（如 `aiocqhttp`, `telegram`, `satori` 等）。
- `interval`: 轮询间隔（秒），建议不低于 60 秒。
- `enable_push`: 是否默认开启推送。

## 使用指令

- `/jin10`: 获取最新的一条金十快讯。
- `/jin10_push [on/off]`: 查看或设置推送状态。

## 数据来源

本插件使用 [RSSHub](https://rsshub.app/jin10/flash) 提供的金十数据接口。
