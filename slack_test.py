from flask import Flask, request, jsonify
import asyncio
import time
import threading
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = WebClient(token='xoxb-6042236359541-6059253691345-ByHni4DixNeXKphWuwMNje3l')

async def test_1():
    logging.info("Функция test_1 была вызвана!")
    await asyncio.sleep(5)
    return "Результат test_1"

async def test_2():
    logging.info("Функция test_2 была вызвана!")
    return "Результат test_2"

async def test_3():
    logging.info("Функция test_3 была вызвана!")
    return "Результат test_3"

blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello again, @user! You've triggered the production smoke test run and here's the results:"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*PA Notifications - :white_check_mark:*\n Regular - :white_check_mark:\n Pop_up - :white_check_mark:\n Survey -  :white_check_mark:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Pushy (MOBILE_PUSH) Notifications - :x:*"
			}
		}
]

def background_task(task_functions, channel_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    results = loop.run_until_complete(asyncio.gather(*[func() for func in task_functions]))
    loop.close()

    result_text = ', '.join(results)

    logging.info('going forward!!')

    # Отправка результата обратно в Slack
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=blocks
        )
    except SlackApiError as e:
        logging.error(f"Error posting message: {e}")

@app.route("/slack", methods=["POST"])
def slack_endpoint():
    text = request.form.get('text', '')
    user_id = request.form.get('user_id', '')
    # channel_id = request.form.get('channel_id', '')  # ID канала Slack для отправки результата
    channel_id = 'C061B4S9VJN'

    task_functions = {
        '1': test_1,
        '2': test_2,
        '3': test_3,
        'ALL': [test_1, test_2, test_3]
    }

    if text.upper() in task_functions:
        tasks = task_functions[text.upper()]
        if isinstance(tasks, list):
            # Запускаем все задачи
            threading.Thread(target=background_task, args=(tasks, channel_id)).start()
        else:
            # Запускаем одну задачу
            threading.Thread(target=background_task, args=([tasks], channel_id)).start()

    return jsonify({"response_type": "in_channel", "text": f"Привет <@{user_id}>! Задачи запущены, результаты появятся позже."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45000)
