from flask import Flask, request, jsonify
import requests  # Импортируем библиотеку requests

app = Flask(__name__)

def test():
    print("Функция test была вызвана!")

@app.route("/slack", methods=["POST"])
def slack_endpoint():
    text = request.form.get('text', '')
    user_id = request.form.get('user_id', '')
    test()

    # Отправка POST-запроса
    post_url = "https://test.com/test"
    payload = {"key": "value"}  # Пример тела запроса. Замените на нужное.
    headers = {"Content-Type": "application/json"}  # Заголовок запроса. Используется при отправке JSON данных.
    response = requests.post(post_url, json=payload, headers=headers)  # Отправка POST-запроса с JSON-данными

    # Можно обработать ответ от POST-запроса, если это необходимо
    if response.status_code == 200:
        post_response_text = "POST-запрос успешно отправлен!"
    else:
        post_response_text = f"Ошибка при отправке POST-запроса: {response.status_code}"

    # Ответ в Slack
    return jsonify({
        "response_type": "in_channel",
        "text": (
            f"Привет <@{user_id}>! Вы сказали: {text}\n"
            f"{post_response_text}"
        ),
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45000)
