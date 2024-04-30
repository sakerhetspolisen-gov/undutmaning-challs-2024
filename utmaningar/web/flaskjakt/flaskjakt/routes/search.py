# routes/main_route.py
from flask import render_template, request
from flaskjakt import app
import re
import html
import os

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results_with_snippets = []
    error_messages = []

    if query:
        file_path = 'harald_notes.txt'
        cmd = f"/usr/bin/grep -i -n -- {query} {file_path} 2>&1"

        try:
            print(f"Executing command: {cmd}")
            output = os.popen(cmd).read()
            print(f"Command output: {output}")
            if output:
                for line in output.split('\n'):
                    if line:
                        if "grep:" in line or "No such file or directory" in line:
                            error_messages.append(html.escape(line))
                        else:
                            escaped_line = html.escape(line)
                            highlighted_line = escaped_line.replace(query, f'<span style="color:red;">{query}</span>')
                            results_with_snippets.append(highlighted_line)
            else:
                error_messages.append("No matches found.")
        except Exception as e:
            error_messages.append(f"An error occurred while running the search: {e}")

    return render_template('search_results.html', query=query, error_messages=error_messages, results=results_with_snippets)

@app.route('/search-results')
def search_results():
    keyword = request.args.get('keyword')
    results = session.get('results')
    if results:
        return render_template('search_results.html', query=keyword, results=results)
    else:
        return render_template('search_results.html', query=keyword, results=[])

