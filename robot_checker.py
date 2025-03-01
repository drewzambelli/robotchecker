from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

def check_robot_txt(url):
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        return "Invalid URL"
    robots_url = parsed_url.scheme + "://" + parsed_url.netloc + "/robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return f"robots.txt found at {robots_url}:\n{response.text}"
        else:
            return f"No robots.txt found at {robots_url}."
    except requests.exceptions.RequestException as e:
        return f"Error checking robots.txt: {e}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        result = check_robot_txt(url)
        return render_template('index.html', result=result, url=url)
    return render_template('index.html', result=None)

if __name__ == "__main__":
    app.run(debug=True)
