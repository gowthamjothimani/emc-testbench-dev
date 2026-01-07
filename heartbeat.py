import time
import socket
import psutil
from datetime import datetime


def get_ipv4_address():
    """
    Get real LAN IPv4 address (not 127.0.1.1)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No real connection is made
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "0.0.0.0"
    finally:
        s.close()
    return ip


class HeartbeatPublisher:
    def __init__(self, mqtt_client, interval=10, device_id=None):
        """
        :param mqtt_client: Existing MQTTClient instance
        :param interval: Heartbeat interval in seconds
        :param device_id: Optional stable device ID (UUID / PCB serial)
        """
        self.mqtt_client = mqtt_client
        self.interval = interval
        self.hostname = socket.gethostname()
        self.ip_address = get_ipv4_address()
        self.device_id = device_id or self.hostname
        self.start_time = time.time()

    def get_uptime(self):
        return int(time.time() - self.start_time)

    def build_payload(self):
        return {
            "device": "BeagleBoneBlack",
            "device_id": self.device_id,
            "hostname": self.hostname,
            "ip": self.ip_address,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "uptime_sec": self.get_uptime(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "status": "ONLINE"
        }

    def start(self):
        topic = f"emc/testbench/heartbeat/{self.hostname}"
        print(f"💓 Heartbeat started → topic: {topic}")

        while True:
            try:
                payload = self.build_payload()

                # Uses your EXISTING mqtt_client API
                self.mqtt_client.publish_data(
                    payload,
                    topic=topic
                )

                print(f"💓 Heartbeat sent [{self.hostname}]")

            except Exception as e:
                print("❌ Heartbeat publish failed:", e)

            time.sleep(self.interval)