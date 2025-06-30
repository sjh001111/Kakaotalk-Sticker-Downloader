# Kakaotalk-Sticker-Downloader

A Discord bot that downloads and converts KakaoTalk emoticons, supporting both WebP and GIF formats with automatic decryption.

## ✨ Features

- 🎨 **Download KakaoTalk emoticons** directly to Discord
- ⚡ **Fast WebP download** (~10 seconds)
- 🎬 **WebP to GIF conversion** (~10 minutes) using automated web conversion
- 🔓 **Automatic decryption** of encrypted emoticon files
- 📦 **ZIP packaging** for easy distribution
- 🧹 **Automatic cleanup** of temporary files

## 🛠️ Tech Stack

- **Python** - Core programming language
- **discord.py** - Discord bot framework
- **requests** - HTTP requests for KakaoTalk emoticon downloads
- **Selenium** - Web automation for WebP to GIF conversion
- **zipfile** - Archive creation and extraction
- **Custom encryption module** - Decrypt KakaoTalk's protected files

## 🚀 Commands

```
!readme                    # Show usage instructions
!webp <emoticon_url>      # Download as WebP format (~10 sec)
!gif <emoticon_url>       # Download and convert to GIF (~10 min)
```

## 📋 Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Kakaotalk-Sticker-Downloader.git
cd Kakaotalk-Sticker-Downloader
```

2. **Install dependencies**
```bash
pip install discord.py requests selenium webdriver-manager
```

3. **Set up environment variables**
```bash
export TOKEN=your_discord_bot_token
```

4. **Run the bot**
```bash
python bot.py
```

## 🔧 How it Works

1. **URL Processing**: Parses KakaoTalk store URLs to extract emoticon ID and name using HTML scraping
2. **Download**: Fetches encrypted emoticon pack ZIP from KakaoTalk CDN servers
3. **Decryption**: Uses custom LFSR-based XOR algorithm to decrypt .gif/.webp files (PNG files are unencrypted)
4. **Conversion** (GIF mode): Automates ezgif.com using Selenium with WebDriverWait for reliable WebP→GIF conversion
5. **Packaging**: Creates separate ZIP archives for WebP and GIF formats
6. **Cleanup**: Automatically removes temporary directories and files after upload

## 📁 Project Structure

```
├── main.py          # Standalone downloader script
├── bot.py           # Discord bot implementation
├── decrypt.py       # LFSR-based emoticon decryption
├── util.py          # URL parsing and KakaoTalk CDN utilities
├── webp2gif.py      # Selenium-based WebP to GIF converter
└── README.md
```

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue for any bugs or feature requests.
