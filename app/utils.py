import ipaddress
import requests

def get_ip_location(ip):
    try:
        ipaddress.ip_address(ip)  # validate IP
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": data.get("ip", ip),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
            }
    except Exception:
        pass
    return {"ip": ip, "country": "UNKNOWN"}