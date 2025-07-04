from flask import Flask, request, jsonify
import requests, string, time

app = Flask(__name__)

def get_suggestions(q):
    resp = requests.get('https://suggestqueries.google.com/complete/search', params={'client':'firefox','ds':'yt','q': q})
    return resp.json()[1]

@app.route('/autocomplete')
def autocomplete():
    kw = request.args.get('keyword','').strip()
    alphabet = request.args.get('alphabet','false').lower() == 'true'
    if not kw:
        return jsonify({'error':'keyword required'}), 400

    suggestions = set(get_suggestions(kw))
    if alphabet:
        for letter in string.ascii_lowercase:
            time.sleep(0.2)
            suggestions.update(get_suggestions(f"{kw} {letter}"))
    return jsonify({'keywords': sorted(suggestions), 'count': len(suggestions)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
