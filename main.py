import asyncio
import time
import feedparser
from astrbot.api.all import *

@register("jinshi_pusher", "Author", "金十数据推送插件", "1.1.0")
class JinshiPusher(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}
        self.target_id = self.config.get("target_id", "123456789")
        self.platform = self.config.get("platform", "aiocqhttp")
        self.interval = self.config.get("interval", 60)
        self.enable_push = self.config.get("enable_push", True)
        
        self.last_time = time.time()
        self.rss_url = "https://rsshub.app/jin10/flash"
        
        if self.enable_push:
            self.task = asyncio.create_task(self.poll_data())
        else:
            self.task = None

    async def poll_data(self):
        while True:
            try:
                # 检查配置是否更新
                self.interval = self.config.get("interval", 60)
                self.target_id = self.config.get("target_id", "123456789")
                self.platform = self.config.get("platform", "aiocqhttp")
                
                feed = await asyncio.to_thread(feedparser.parse, self.rss_url)
                if feed.entries:
                    new_entries = []
                    for entry in feed.entries:
                        entry_time = time.mktime(entry.published_parsed)
                        if entry_time > self.last_time:
                            new_entries.append(entry)
                    
                    # 按时间升序推送
                    for entry in sorted(new_entries, key=lambda x: time.mktime(x.published_parsed)):
                        await self.send_news(entry.title)
                        self.last_time = time.mktime(entry.published_parsed)
            except Exception as e:
                self.context.logger.error(f"金十推送轮询报错: {e}")
            
            await asyncio.sleep(self.interval)

    async def send_news(self, text: str):
        msg_chain = [Plain(f"【金十快讯】\n{text}")]
        await self.context.send_message(self.platform, self.target_id, msg_chain)

    @command("jin10")
    async def get_latest_news(self, event: AstrMessageEvent):
        \"\"\"获取最新的一条金十数据快讯\"\"\"
        try:
            feed = await asyncio.to_thread(feedparser.parse, self.rss_url)
            if feed.entries:
                latest = feed.entries[0]
                yield event.plain_result(f"【金十快讯 - 最新】\n{latest.title}")
            else:
                yield event.plain_result("暂时没有获取到金十快讯。")
        except Exception as e:
            yield event.plain_result(f"获取失败: {e}")

    @command("jin10_push")
    async def toggle_push(self, event: AstrMessageEvent, status: str = None):
        \"\"\"开启或关闭金十推送。参数: on/off\"\"\"
        if status == "on":
            if not self.task or self.task.done():
                self.enable_push = True
                self.task = asyncio.create_task(self.poll_data())
                yield event.plain_result("金十推送已开启。")
            else:
                yield event.plain_result("金十推送已经在运行中。")
        elif status == "off":
            if self.task and not self.task.done():
                self.enable_push = False
                self.task.cancel()
                self.task = None
                yield event.plain_result("金十推送已关闭。")
            else:
                yield event.plain_result("金十推送当前未开启。")
        else:
            current_status = "开启" if (self.task and not self.task.done()) else "关闭"
            yield event.plain_result(f"当前推送状态: {current_status}。使用 /jin10_push on/off 切换。")
