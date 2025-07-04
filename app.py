rom flask import Flask, request, jsonify
import requests, string

app = Flask(__name__)

def get_suggestions(q):
    r = requests.get('https://suggestqueries.google.com/complete/search', params={'client': 'firefox', 'ds': 'yt', 'q': q})
    return r.json()[1]

@app.route('/autocomplete')
def autocomplete():
    kw = request.args.get('keyword', '').strip()
    alpha = request.args.get('alphabet', 'false').lower() == 'true'
    if not kw:
        return jsonify({'error': 'keyword required'}), 400

    suggestions = set(get_suggestions(kw))
    if alpha:
        for letter in string.ascii_lowercase:
            suggestions.update(get_suggestions(f"{kw} {letter}"))
    return jsonify({'keywords': sorted(suggestions), 'count': len(suggestions)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
