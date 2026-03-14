import discord
import os
import asyncio
import datetime
import pytz
from discord.ext import commands, tasks

# --- ดึงค่าความปลอดภัยจากระบบ (ใส่ใน Variables ของ Railway) ---
# ชื่อใน Railway ต้องตั้งว่า DISCORD_TOKEN และ CHANNEL_ID
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

class GoldBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.daily_report.start()
        print("✅ ระบบส่งรายงานอัตโนมัติ (จันทร์-ศุกร์ 09:00 น.) พร้อมทำงาน!")

    async def on_ready(self):
        print(f'🚀 บอท {self.user.name} ออนไลน์และกำลังรอส่งรายงาน...')

    def format_report(self, data, dt):
        """ รูปแบบข้อความ: หัวข้ออยู่บนสุด ตามด้วยวันที่และเวลา """
        # แปลงชื่อวันเป็นภาษาไทย
        days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        day_name = days[dt.weekday()]
        date_str = dt.strftime("%d/%m/%Y")
        time_str = dt.strftime("%H:%M")

        return (
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "   📊 **GOLD MARKET REPORT** 📊\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 **วัน{day_name}ที่ {date_str}**\n"
            f"⏰ **เวลา: {time_str} น.**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 **Price**\n{data['price']} USD\n\n"
            f"📈 **Market Trend**\n{data['trend']}\n\n"
            f"🟢 **Support**\n{data['support']}\n\n"
            f"🔴 **Resistance**\n{data['resistance']}\n\n"
            f"💡 **Market Insight**\n{data['insight']}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ **Note**\n"
            "การวิเคราะห์นี้เป็นเพียงข้อมูล\n"
            "ไม่ใช่คำแนะนำในการลงทุน\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    @tasks.loop(minutes=1)
    async def daily_report(self):
        # ตั้งค่าโซนเวลาไทย
        tz = pytz.timezone('Asia/Bangkok')
        now = datetime.datetime.now(tz)

        # ตรวจสอบ: จันทร์-ศุกร์ (0-4) และ เวลา 09:00 น.
        if now.weekday() < 5 and now.hour == 9 and now.minute == 0:
            channel = self.get_channel(int(CHANNEL_ID))
            if channel:
                # แก้ไขข้อมูลตัวเลขตรงนี้ก่อนอัปโหลดขึ้น GitHub ทุกครั้ง
                data = {
                    "price": "5023.10",
                    "trend": "Downtrend",
                    "support": "5014.10",
                    "resistance": "5132.40",
                    "insight": "แรงขายยังคงกดดันตลาด แนวโน้มยังอ่อนตัว"
                }
                await channel.send(self.format_report(data, now))
                print(f"✅ ส่งรายงานสำเร็จเมื่อเวลา {now.strftime('%H:%M:%S')}")
                # รอ 60 วินาทีเพื่อป้องกันการส่งซ้ำในนาทีเดียวกัน
                await asyncio.sleep(60)

if __name__ == "__main__":
    if TOKEN and CHANNEL_ID:
        bot = GoldBot()
        bot.run(TOKEN)
    else:
        print("❌ ERROR: กรุณาตั้งค่า DISCORD_TOKEN และ CHANNEL_ID ในหน้า Variables ของ Railway")