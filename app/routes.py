from flask import Blueprint, request, jsonify
from .utils import get_ip_location

bp = Blueprint("routes", __name__)

@bp.route("/verify-access", methods=["POST"])
def verify_access():
  try:
      data = request.json or {}
      app_version = data.get("appVersion", "0.0.0")
      is_physical_device = data.get("isPhysicalDevice", False)
      client_public_ip = request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist("X-Forwarded-For") else request.remote_addr
 

      # # 1. check device type
      # if is_physical_device is not True:
      #     return jsonify({"allow": False, "reason": "Device not physical"})

      # 2. check ip vietnam
      client_location = get_ip_location(client_public_ip)
      if client_location.get("country") != "VN":
        return jsonify({
            "allow": False,
            "reason": f"Not from Vietnam ({client_location.get('country')})",
            "client_location": client_location
        })

      return jsonify({"allow": True})
  except Exception as e:
      return jsonify({"allow": False, "reason": str(e)})