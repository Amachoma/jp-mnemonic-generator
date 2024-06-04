import os
from dotenv import load_dotenv
import requests
from time import time
import re
import json

from stream_parser.constants import TASK_SUMMARY, TASK_SUMMARY_ANSWER

load_dotenv()


class ChatBot:

    def __init__(self, task_summary=TASK_SUMMARY):
        self.task_summary = task_summary
        self.url = os.getenv('API_URL')
        self.headers = {"Authorization": f"Bearer {os.getenv('ID_TOKEN')}"}
        self.payload_base = {"chat_mode": 1, "genre_id": 102, "gpt_type": 102, "is_enabled_rag": False,
                             'old_conversation_context_summary': "", "thread_id": None}

    def send_message(self, message, message_history=None):
        if message_history is None:
            message_history = []

        payload = {**self.payload_base, **{
            "input_question": message,
            "previous_messages": [self.task_summary, TASK_SUMMARY_ANSWER] + message_history,
        }}

        start_time = time()
        response = requests.post(self.url, headers=self.headers, json=payload, stream=True)

        if response.status_code == 200:
            final_message = ""
            for line in response.iter_lines():
                pattern = r'\{(.+?)\}'
                if line:
                    try:
                        result = re.search(pattern, line.decode('utf-8'))
                        stream_obj = json.loads(result.group(0))
                        final_message += stream_obj["part_of_final_answer_text"]
                    except:
                        print(f"Cannot process following string, skipping: {line}")

            elapsed = time() - start_time
            return [final_message, elapsed]

        elif response.status_code == 401:
            token_input = input("Token expired, provide updated token: ").strip()
            if token_input != "":
                self.headers = {"Authorization": f"Bearer {token_input}"}
                return self.send_message(message, message_history)
            else:
                raise ValueError("Token expired")

        else:
            raise Exception(response.content)
