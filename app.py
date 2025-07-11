from flask import Flask, request, send_file, jsonify, after_this_request, render_template
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
CX = os.getenv("CX")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get("query")
    output_format = data.get("format", "txt").lower()

    if not query:
        return jsonify({"error": "Missing query"}), 400

    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
        "num": 10,
        "start": 1
    }

    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    if response.status_code != 200:
        return jsonify({"error": "Google API error", "details": response.text}), 500

    items = response.json().get("items", [])

    if not items:
        return jsonify({"error": "No results found."}), 404

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results_{timestamp}.{output_format}"

    try:
        if output_format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
        elif output_format == "txt":
            with open(filename, "w", encoding="utf-8") as f:
                for item in items:
                    f.write(f"{item['title']}\n")
                    f.write(f"{item['link']}\n")
                    f.write(f"{item.get('snippet', '')}\n")
                    f.write("\n" + "-" * 40 + "\n\n")
        else:
            return jsonify({"error": "Unsupported format"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to write file: {e}"}), 500

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            app.logger.warning(f"File doesn't exist: {e}")
        return response

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=True)
