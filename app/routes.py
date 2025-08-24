from flask import Blueprint, request, jsonify
from .utils import compare_version, is_ip_vietnam, MIN_VERSION

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
      if not is_ip_vietnam(client_ip):
          return jsonify({"allow": False, "reason": "Not from Vietnam"})

      return jsonify({"allow": True})
  except Exception as e:
      return jsonify({"allow": False, "reason": str(e)})