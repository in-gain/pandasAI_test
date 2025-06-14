from flask import Flask, request, jsonify, render_template_string

from app import query_llm

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang=\"ja\">
<head>
    <meta charset=\"UTF-8\">
    <title>顧客データチャットボット</title>
    <script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        #chat { margin-bottom: 1em; }
        .message { margin: 0.5em 0; }
        .user { font-weight: bold; }
        .response { color: blue; }
    </style>
</head>
<body>
    <h1>顧客データチャットボット</h1>
    <div id=\"chat\"></div>
    <form id=\"chat-form\">
        <input type=\"text\" id=\"question\" placeholder=\"質問を入力\" autocomplete=\"off\" size=\"50\">
        <button type=\"submit\">送信</button>
    </form>
    <script>
        $('#chat-form').on('submit', function(e) {
            e.preventDefault();
            var question = $('#question').val();
            if(!question) return;
            $('#chat').append('<div class="message user">ユーザー: ' + question + '</div>');
            $('#question').val('');
            $.post('/ask', {question: question}, function(data) {
                if(data.answer) {
                    $('#chat').append('<div class="message response">ボット: ' + data.answer + '</div>');
                } else if(data.error) {
                    $('#chat').append('<div class="message response">エラー: ' + data.error + '</div>');
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "")
    if not question:
        return jsonify({"error": "質問が入力されていません"}), 400
    try:
        answer = query_llm(question)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
