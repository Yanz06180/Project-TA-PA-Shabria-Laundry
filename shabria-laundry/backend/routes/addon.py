from flask import Blueprint, jsonify
from db import query

addon_bp = Blueprint("addon", __name__)

@addon_bp.route("/", methods=["GET"])
def get_all():
    return jsonify(query("SELECT * FROM add_on WHERE aktif=1 ORDER BY id_add_on"))
