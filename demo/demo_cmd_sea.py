import gradio as gr
import requests
import json
from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer
import torch
import argparse

from elasticsearch import Elasticsearch
from config import es as esconf


def json_send(url, data=None, method="POST"):
    headers = {"Content-type": "application/json",
               "Accept": "text/plain", "charset": "UTF-8"}
    if method == "POST":
        if data != None:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        else:
            response = requests.post(url=url, headers=headers)
    elif method == "GET":
        response = requests.get(url=url, headers=headers)
    return json.loads(response.text)


def json_send_sea(es, prompt):
    resp = es.search(
        index=esconf['index'],
        size=60,
        query={
            "function_score": {
                "query": {
                    "bool": {
                        "must": {
                            "combined_fields": {
                                "query": prompt,
                                # "fields": ["from", "to"] # relation使用的keyword
                                "fields": ["from", "relation", "to"] # relation使用的keyword
                            }
                        }
                    }
                },
                "min_score": 8
            }
        },
        filter_path=[
            'hits.hits._score',
            'hits.hits._source.from',
            'hits.hits._source.relation',
            'hits.hits._source.to',
        ]
    )

    if not 'hits' in resp.keys():
        return []
    if not 'hits' in resp['hits'].keys():
        return []
    return [hit['_source']['from'] + hit['_source']['relation'] + hit['_source']['to'] for hit in resp['hits']['hits']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--classifier_url", type=str, default="")
    parser.add_argument("--load_in_8bit", action="store_true")
    parser.add_argument("--use_chat_mode", action="store_true")
    args = parser.parse_args()
    checkpoint = args.checkpoint
    classifier_url = args.classifier_url

    es = Elasticsearch(
        esconf['host'],
        basic_auth=(esconf['username'], esconf['password'])
    )

    print("Loading model...")
    tokenizer = LlamaTokenizer.from_pretrained(checkpoint)
    if args.load_in_8bit:
        model = LlamaForCausalLM.from_pretrained(checkpoint, device_map="auto", load_in_8bit=True)
    else:
        model = LlamaForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.float16)
    print("Model loaded.")

    if args.use_chat_mode:
        print("Chat mode enabled.")
        print("If you want to start a new chat, enter 'clear' please")
        chat_history = []

    while True:
        current_user_input = input("[Human] >>> ")
        current_user_input = current_user_input.strip()
        if len(current_user_input) == 0:
            continue

        if args.use_chat_mode and current_user_input == "clear":
            chat_history = []
            print("Chat history cleared.")
            continue

        if args.use_chat_mode:
            history_user_input = [x[0] for x in chat_history]
            input_to_classifier = " ".join(history_user_input) + " " + current_user_input
        else:
            input_to_classifier = current_user_input
        data = {"input": input_to_classifier}
        retrieve_output = json_send_sea(es, input_to_classifier)

        # 构造输入
        if len(retrieve_output) == 0:
            input_text = "你是人工智能法律助手“Lawyer LLaMA”，能够回答与中国海洋法律相关的问题。\n"
            for history_pair in chat_history[:-1]:
                input_text += f"### Human: {history_pair[0]}\n### Assistant: {history_pair[1]}\n"
            input_text += f"### Human: {current_user_input}\n### Assistant: "
        else:
            input_text = f"你是人工智能法律助手“Lawyer LLaMA”，能够回答与中国海洋法律相关的问题。请参考给出的\"参考知识\"，回复用户的咨询问题。\"参考知识\"中可能存在与咨询无关的知识，请回复时不要引用这些无关的知识。\n"
            for history_pair in chat_history[:-1]:
                input_text += f"### Human: {history_pair[0]}\n### Assistant: {history_pair[1]}\n"

            input_text += f"### Human: {current_user_input}\n### 参考知识: "
            for output_item in retrieve_output:
                input_text += f"{output_item}\n"
            input_text += f"### Assistant: "

        # print(input_text)
        # print()

        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        outputs = model.generate(input_ids, max_new_tokens=400, do_sample=False, repetition_penalty=1.1)
        output_text = str(tokenizer.decode(outputs[0], skip_special_tokens=True))
        # skip prompt
        output_text = output_text[len(input_text):]

        print("[AI] >>> " + output_text)

        if args.use_chat_mode:
            chat_history.append((current_user_input, output_text))

