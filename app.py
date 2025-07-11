from flask import Flask, request, send_file, jsonify, after_this_request
import requests
import os
from dotenv import load_dotenv
from flask import render_template
from datetime import datetime


load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
CX = os.getenv("CX")

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
  data = request.get_json()
  query = data.get("query")

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
    return jsonify( {
        "error": "Google API error",
        "details": response.text 
        }), 500

  data = response.json()
  items = data.get("items", [])

  if not items:
    return jsonify({"error": "No results found."}), 404
  
  timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

  filename = f"results_{timestamp}"
  txt_filename = f"{filename}.txt"

  with open(txt_filename, "w", encoding="utf-8") as f:
    for item in items:
      f.write(f"{item['title']}\n")
      f.write(f"{item['link']}\n")
      f.write(f"{item.get('snippet', '')}\n")
      f.write("\n" + "-" * 40 + "\n\n")

  @after_this_request
  def remove_file(response):
        try:
            os.remove(txt_filename)
        except Exception as e:
            app.logger.warning(f"File doesn't exist: {e}")
        return response

  return send_file(txt_filename, as_attachment=True)

if __name__ == '__main__':
  app.run(debug=True)
