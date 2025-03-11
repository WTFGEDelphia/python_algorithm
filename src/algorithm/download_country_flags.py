import argparse
import json
import os
import requests
from urllib.parse import urljoin

"""
下载国旗图片
通过CDN（HTTP API）在您的网站上嵌入的标志

可用尺寸
16x12
20x15
24x18
28x21
32x24
36x27
40x30
48x36
56x42
60x45
64x48
72x54
80x60
84x63
96x72
108x81
112x84
120x90
128x96
144x108
160x120
192x144
224x168
256x192

插入您的网站
<img
  src="https://flagcdn.com/16x12/ua.png"
  srcset="https://flagcdn.com/32x24/ua.png 2x,
    https://flagcdn.com/48x36/ua.png 3x"
  width="16"
  height="12"
  alt="乌克兰">

编程下载
https://flagcdn.com(服务地址)/16x12(尺寸)/ua(ISO 3166国家代码).png

JSON格式的国家代码列表（国家、美国、欧盟和联合国）
https://flagcdn.com(服务地址)/zh(语言)/codes.json
"""
# 基础配置
BASE_JSON_URL = "https://flagcdn.com/zh/codes.json"
IMAGE_BASE_URL = "https://flagcdn.com/"
AVAILABLE_SIZES = [
    "16x12",
    "20x15",
    "24x18",
    "28x21",
    "32x24",
    "36x27",
    "40x30",
    "48x36",
    "56x42",
    "60x45",
    "64x48",
    "72x54",
    "80x60",
    "84x63",
    "96x72",
    "108x81",
    "112x84",
    "120x90",
    "128x96",
    "144x108",
    "160x120",
    "192x144",
    "224x168",
    "256x192",
]


def download_flags(size: str, output_dir: str):
    """下载指定尺寸的国旗图片"""
    # 创建尺寸子目录
    target_dir = os.path.join(output_dir, size)
    os.makedirs(target_dir, exist_ok=True)

    # 获取国家代码列表
    response = requests.get(BASE_JSON_URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    country_codes = json.loads(response.text)

    # 下载每个国旗
    success = 0
    for code, name in country_codes.items():
        try:
            # 文件名
            filename = os.path.join(target_dir, f"{code}.png")

            # 检查文件是否已经存在
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"✅ 文件已存在 {name} ({code})")
                success += 1
                continue

            # 构建图片URL
            img_url = urljoin(IMAGE_BASE_URL, f"{size}/{code}.png")
            print(f"准备下载 {name} ({code}) img_url: {img_url}")

            # 发送请求
            img_response = requests.get(img_url, stream=True, timeout=15)
            img_response.raise_for_status()

            # 保存文件
            with open(filename, "wb") as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)

            success += 1
            print(f"✅ 已下载 {name} ({code})")
        except Exception as e:
            print(f"❌ 下载失败 {name} ({code}): {str(e)}")

    print(f"\n下载完成！成功 {success}/{len(country_codes)}")


if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="国旗下载工具")
    parser.add_argument(
        "-s",
        "--size",
        required=False,
        default="256x192",
        choices=AVAILABLE_SIZES,
        help="图片尺寸（默认：256x192）",
    )
    parser.add_argument(
        "-o", "--output", default="flags", help="输出目录（默认：flags）"
    )

    args = parser.parse_args()

    # 执行下载
    print(f"开始下载 {args.size} 尺寸的国旗...")
    download_flags(args.size, args.output)
