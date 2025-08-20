import discord
from discord.ext import commands
from PIL import Image
import aiohttp
import io
import os
from moviepy.editor import VideoFileClip

intents = discord.Intents.default()
intents.message_content = True  # Enable content reading

bot = commands.Bot(command_prefix='!', intents=intents)

# Supported image formats
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
VIDEO_EXTENSIONS = ['.mp4', '.webm', '.mov', '.avi']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

async def download_attachment(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                return None

@bot.command(name='convert')
async def convert(ctx, target_format: str):
    """
    Convert attached image or video to target format.
    Usage: !convert png
    Supported image formats: jpg, png, bmp, tiff, webp
    Supported video -> gif conversions: input video formats are mp4, webm, mov, avi
    """
    if not ctx.message.attachments:
        await ctx.send("Please attach an image or video file to convert.")
        return

    target_format = target_format.lower()
    if target_format.startswith('.'):
        target_format = target_format[1:]  # strip dot

    attachment = ctx.message.attachments[0]
    filename = attachment.filename.lower()
    file_ext = os.path.splitext(filename)[1]

    # Download file to bytes
    file_bytes = await download_attachment(attachment.url)
    if file_bytes is None:
        await ctx.send("Failed to download the file.")
        return

    # Process Image Conversion
    if file_ext in IMAGE_EXTENSIONS:
        if target_format not in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']:
            await ctx.send(f"Unsupported target image format: {target_format}")
            return
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(file_bytes)).convert("RGBA")

            # Convert PNG/JPG difference: remove alpha channel for JPG
            save_params = {}
            if target_format in ['jpg', 'jpeg'] and image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])  # 3 is alpha channel
                image = background
            else:
                if image.mode == 'P':
                    image = image.convert('RGBA')

            out_bytes = io.BytesIO()
            image.save(out_bytes, format=target_format.upper())
            out_bytes.seek(0)

            await ctx.send(file=discord.File(fp=out_bytes, filename=f'converted.{target_format}'))

        except Exception as e:
            await ctx.send(f"Error converting image: {e}")

    # Process Video to GIF conversion
    elif file_ext in VIDEO_EXTENSIONS:
        if target_format != 'gif':
            await ctx.send("Currently, only conversion from video to GIF is supported for videos.")
            return

        try:
            # Save the video to a temporary file first (moviepy needs a filename)
            temp_vid_path = f"temp_video{file_ext}"
            with open(temp_vid_path, "wb") as f:
                f.write(file_bytes)

            # Load video with moviepy
            clip = VideoFileClip(temp_vid_path)

            # Limit duration for GIF (e.g., max 10 seconds) to avoid huge files
            max_duration = 10
            if clip.duration > max_duration:
                clip = clip.subclip(0, max_duration)

            temp_gif_path = "converted.gif"
            clip.write_gif(temp_gif_path)

            # Send GIF back
            await ctx.send(file=discord.File(temp_gif_path))

            # Clean up
            clip.close()
            os.remove(temp_vid_path)
            os.remove(temp_gif_path)

        except Exception as e:
            await ctx.send(f"Error converting video to GIF: {e}")

    else:
        await ctx.send("Unsupported file type. Please attach an image or a supported video file.")


import os
bot.run(os.getenv('DISCORD_TOKEN'))
