from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)

async def test_1():
    print("Функция test_1 была вызвана!")
    return "Результат test_1"

async def test_2():
    print("Функция test_2 была вызвана!")
    return "Результат test_2"

async def test_3():
    print("Функция test_3 была вызвана!")
    return "Результат test_3"

@app.route("/slack", methods=["POST"])
def slack_endpoint():
    text = request.form.get('text', '')
    user_id = request.form.get('user_id', '')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    response_text = f"Привет <@{user_id}>! Вы сказали: {text}\n"

    try:
        if text == '1':
            result = asyncio.run(test_1())
            response_text += result
        elif text == '2':
            result = asyncio.run(test_2())
            response_text += result
        elif text == '3':
            result = asyncio.run(test_3())
            response_text += result
        elif text.upper() == 'ALL':
            # Запуск всех функций асинхронно и сбор результатов
            tasks = [test_1(), test_2(), test_3()]
            results = loop.run_until_complete(asyncio.gather(*tasks))
            response_text += ', '.join(results)
    finally:
        loop.close()

    # Ответ в Slack
    return jsonify({
        "response_type": "in_channel",
        "text": response_text
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45000)
