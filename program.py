from flask import Flask, request, render_template_string, send_file
import os
import webbrowser

app = Flask(__name__)

# 홈 페이지 HTML 
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sleep Quality Enhancer</title>
    <style>
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background-image: url('/static/images/morning_image.jpg');
            background-size: cover;
            background-position: center center;
            color: #4A4A4A;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        h1 {
            font-size: 2.5em;
            color: white;
        }
        form {
            margin-top: 20px;
        }
        button {
            background-color: #ADD8E6; /* 하늘색 */
            color: #4A4A4A;
            border: none;
            padding: 10px 20px;
            font-size: 1.2em;
            cursor: pointer;
            border-radius: 20px;
        }
        button:hover {
            background-color: #87CEFA; /* 조금 더 진한 하늘색 */
        }
    </style>
</head>
<body>
    <h1>Welcome to Sleep Quality Enhancer</h1>
    <form action="/question1" method="GET">
        <button type="submit">Start</button>
    </form>
</body>
</html>
"""

# 질문 1 페이지 HTML 
question1_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How was your day?</title>
    <style>
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background-image: url('/static/images/day_image.jpg');
            background-size: cover;
            background-position: center center;
            color: #4A4A4A;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        h2 {
            font-size: 2em;
            color: white;
            margin-bottom: 30px;
            text-align: center;
        }
        form {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        button {
            background-color: #A5D8D6;
            color: #FFFFFF;
            border: none;
            padding: 15px;
            font-size: 1em;
            cursor: pointer;
            border-radius: 10px;
        }
        button:hover {
            background-color: #82C4C3;
        }
    </style>
</head>
<body>
    <h2>Hi there! How was your day today? Choose the option that best describes your day.</h2>
    <form action="/question2" method="POST">
        <button type="submit" name="day" value="stressful">Stressful</button>
        <button type="submit" name="day" value="productive">Productive</button>
        <button type="submit" name="day" value="relaxing">Relaxing</button>
        <button type="submit" name="day" value="exhausting">Exhausting</button>
    </form>
</body>
</html>
"""

# 질문 2 페이지 HTML 
question2_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Choose a Keyword</title>
    <style>
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background-image: url('{{ url_for("static", filename="images/evening_image.jpg") }}');
            background-size: cover;
            background-position: center center;
            color: #4A4A4A;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        h2 {
            font-size: 2em;
            color: white;
            margin-bottom: 30px;
            text-align: center;
        }
        form {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        button {
            background-color: #FFD1A9;
            color: #FFFFFF;
            border: none;
            padding: 15px;
            font-size: 1em;
            cursor: pointer;
            border-radius: 10px;
        }
        button:hover {
            background-color: #FFB582;
        }
    </style>
</head>
<body>
    <h2>Choose a keyword that will help you relax and sleep better tonight!</h2>
    <form action="/result" method="POST">
        <input type="hidden" name="day" value="{{ day }}">
        <button type="submit" name="keyword" value="calm">Calm</button>
        <button type="submit" name="keyword" value="excitement">Excitement</button>
        <button type="submit" name="keyword" value="leisure">Leisure</button>
        <button type="submit" name="keyword" value="focus">Focus</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return home_page

@app.route("/question1")
def question1():
    return question1_page

@app.route("/question2", methods=["POST"])
def question2():
    day = request.form.get("day")
    return render_template_string(question2_template, day=day)

@app.route("/result", methods=["POST"])
def result():
    day = request.form.get("day")
    keyword = request.form.get("keyword")

    # 16가지 경우의 수에 따른 음악 파일 매핑
    sound_map = {
        ("stressful", "calm"): "stressful_calm.mp3",
        ("stressful", "excitement"): "stressful_excitement.mp3",
        ("stressful", "leisure"): "stressful_leisure.mp3",
        ("stressful", "focus"): "stressful_focus.mp3",
        ("productive", "calm"): "productive_calm.mp3",
        ("productive", "excitement"): "productive_excitement.mp3",
        ("productive", "leisure"): "productive_leisure.mp3",
        ("productive", "focus"): "productive_focus.mp3",
        ("relaxing", "calm"): "relaxing_calm.mp3",
        ("relaxing", "excitement"): "relaxing_excitement.mp3",
        ("relaxing", "leisure"): "relaxing_leisure.mp3",
        ("relaxing", "focus"): "relaxing_focus.mp3",
        ("exhausting", "calm"): "exhausting_calm.mp3",
        ("exhausting", "excitement"): "exhausting_exciteme.mp3",
        ("exhausting", "leisure"): "exhausting_leisure.mp3",
        ("exhausting", "focus"): "exhausting_focus.mp3"
    }
    sound_file = sound_map.get((day, keyword), "default.mp3")

    # 글귀 추가
    quotes = {
        "stressful": "Even on the most stressful days, the night gives you a chance to recharge and renew.",
        "productive": "After a day of great accomplishments, let your body and mind find peace.",
        "relaxing": "A relaxing day deserves an even more peaceful night.",
        "exhausting": "When you’re weary, sleep becomes your sweetest sanctuary."
    }
    quote = quotes.get(day, "Close your eyes and let the gentle rhythm of the night carry you away.")

    result_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sleep Aid Result</title>
        <style>
            body {{
                font-family: 'Comic Sans MS', cursive, sans-serif;
                background-image: url('{{{{ url_for("static", filename="images/night_image.jpg") }}}}');
                background-size: cover;
                background-position: center center;
                color: #4A4A4A;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }}
            .quote {{
                background-color: rgba(255, 255, 255, 0.85);
                color: white;
                border-radius: 20px;
                padding: 20px;
                text-align: center;
                max-width: 70%;
                font-size: 1.5em;
                font-style: italic;
                box-shadow: none;
                margin-bottom: 30px;
            }}
            audio {{
                margin-top: 20px;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                background-color: #DAB6FF;
                color: #FFFFFF;
                padding: 10px 20px;
                font-size: 1.1em;
                border-radius: 20px;
            }}
            a:hover {{
                background-color: #C296FF;
            }}
        </style>
    </head>
    <body>
        <div class="quote">
            <em>"{quote}"</em>
        </div>
        <audio controls autoplay>
            <source src="/static/{sound_file}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(result_page, quote=quote, sound_file=sound_file)

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)  # 이미지 폴더 생성
    port = 8080
    url = f"http://127.0.0.1:{port}"
    print(f"Opening web browser at {url}...")
    webbrowser.open(url)
    app.run(host="0.0.0.0", port=port, debug=True)
