from flask import Flask, render_template, request, make_response
import requests
from urllib.parse import urlparse
import csv
import io

app = Flask(__name__)

def parse_robots_txt(robots_txt):
    """
    Parses the robots.txt file content into a readable format.
    """
    user_agents = {}
    current_user_agent = None
    
    # Split the robots.txt content into lines
    lines = robots_txt.splitlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines or comments
        if not line or line.startswith('#'):
            continue
        
        # Detect the user-agent line
        if line.lower().startswith('user-agent'):
            current_user_agent = line.split(':')[1].strip()
            user_agents[current_user_agent] = {"Disallow": [], "Allow": []}
        
        # Handle disallow rules
        elif line.lower().startswith('disallow'):
            if current_user_agent:
                path = line.split(':')[1].strip()
                user_agents[current_user_agent]["Disallow"].append(path)
        
        # Handle allow rules
        elif line.lower().startswith('allow'):
            if current_user_agent:
                path = line.split(':')[1].strip()
                user_agents[current_user_agent]["Allow"].append(path)
    
    return user_agents

def check_robot_txt(url):
    # If the URL does not start with http:// or https://, prepend http://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    
    parsed_url = urlparse(url)
    
    if not parsed_url.netloc:
        return "Invalid URL"
    robots_url = parsed_url.scheme + "://" + parsed_url.netloc + "/robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            # Parse robots.txt and return formatted output
            user_agents = parse_robots_txt(response.text)
            formatted_result = ""
            for agent, rules in user_agents.items():
                formatted_result += f"User-agent: {agent}\n"
                formatted_result += f"Disallowed paths: {', '.join(rules['Disallow']) if rules['Disallow'] else 'None'}\n"
                formatted_result += f"Allowed paths: {', '.join(rules['Allow']) if rules['Allow'] else 'None'}\n\n"
            return formatted_result
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

@app.route('/export', methods=['POST'])
def export():
    url = request.form['url']
    result = request.form['result']
    
    # Create an in-memory text stream
    output = io.StringIO()
    writer = csv.writer(output)

    # Write CSV headers and data
    writer.writerow(['Website URL', 'Robots.txt Content'])
    writer.writerow([url, result])

    # Get the CSV content
    output.seek(0)
    response = make_response(output.getvalue())

    # Set headers to trigger file download
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=robots.txt_export.csv'

    return response


if __name__ == "__main__":
    app.run(debug=True)
