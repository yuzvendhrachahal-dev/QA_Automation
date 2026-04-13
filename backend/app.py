from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import traceback
from pathlib import Path

from backend.engine.executor import run_test
from backend.engine.model import parse_human_steps

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent.parent
SCREENSHOT_ROOT = BASE_DIR / "storage" / "runs"
SCREENSHOT_ROOT.mkdir(parents=True, exist_ok=True)

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)


# ── Run test ──────────────────────────────────────────────────────────────────
@app.route("/run", methods=["POST"])
def run_test_api():
    try:
        data = request.get_json(force=True)
        structured_steps = parse_human_steps(data["steps"], data["url"])
        return jsonify(run_test(data["url"], structured_steps, data["testName"]))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "FAILED", "error": str(e)})


# ── Screenshot serving ────────────────────────────────────────────────────────

@app.route("/storage/runs/<run_id>/<filename>")
def serve_screenshot(run_id, filename):
    directory = str(SCREENSHOT_ROOT / run_id)
    return send_from_directory(directory, filename)


# ── Health ────────────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)