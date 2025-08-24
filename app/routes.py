from flask import Blueprint, request, jsonify
from .utils import compare_version, get_ip_location, MIN_VERSION

bp = Blueprint("routes", __name__)

@bp.route("/verify-access", methods=["POST"])
def verify_access():
  try:
      data = request.json or {}
      app_version = data.get("appVersion", "0.0.0")
      device_type = data.get("deviceType", "unknown")
      client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

      # 1. check device type
      if device_type.lower() != "physical":
          return jsonify({"allow": False, "reason": "Device not physical"})

      # 2. check ip vietnam
      location = get_ip_location(client_ip)
      if location.get("country") != "VN":
        return jsonify({
            "allow": False,
            "reason": f"Not from Vietnam ({location.get('country')})",
            "location": location
        })

      return jsonify({"allow": True})
  except Exception as e:
      return jsonify({"allow": False, "reason": str(e)})