import gradio as gr
import requests
import json
from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer
import torch
import argparse

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--classifier_url", type=str, default="")
    parser.add_argument("--load_in_8bit", action="store_true")
    parser.add_argument("--use_chat_mode", action="store_true")
    args = parser.parse_args()
    checkpoint = args.checkpoint
    classifier_url = args.classifier_url

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
        # chat_history 是一个 list，每一个 list 包括两个项：0 是某一轮的用户输入，1 是对应轮次的回答。
        # TODO：考虑限制这个列表的长度。
        chat_history = []

    while True:
        # [Human] >>> 会输出到命令行提示用户输入，读取的用户输入内容不包含这部分内容；
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

        # 这里 input_to_classifier 在 chat mode 下是一长串历史输入内容拼在一起的，新的在后面；
        data = {"input": input_to_classifier}

        # 请求法条检索服务
        result = json_send(classifier_url, data, method="POST")
        retrieve_output = result['output']
            
        # 构造输入
        if len(retrieve_output) == 0:
            input_text = "你是人工智能法律助手“Lawyer LLaMA”，能够回答与中国法律相关的问题。\n"
            for history_pair in chat_history[:-1]:
                input_text += f"### Human: {history_pair[0]}\n### Assistant: {history_pair[1]}\n"
            input_text += f"### Human: {current_user_input}\n### Assistant: "
        else:
            input_text = f"你是人工智能法律助手“Lawyer LLaMA”，能够回答与中国法律相关的问题。请参考给出的\"参考法条\"，回复用户的咨询问题。\"参考法条\"中可能存在与咨询无关的法条，请回复时不要引用这些无关的法条。\n"
            for history_pair in chat_history[:-1]:
                input_text += f"### Human: {history_pair[0]}\n### Assistant: {history_pair[1]}\n"
            input_text += f"### Human: {current_user_input}\n### 参考法条: {retrieve_output[0]['text']}\n{retrieve_output[1]['text']}\n{retrieve_output[2]['text']}\n### Assistant: "

        # 这是进行编码，是返回 embedding 还是其它格式？tokenize 应该不到 embedding 这步。
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        # 执行生成。看来可以通过 max_new_tokens 参数来单独限制生成内容的长度。
        outputs = model.generate(input_ids, max_new_tokens=400, do_sample=False, repetition_penalty=1.1)
        # outputs 并不是 text，而是某种编码，需要使用 tokenizer 进行 decode 才能得到 text。
        output_text = str(tokenizer.decode(outputs[0], skip_special_tokens=True))
        # skip prompt。 原输出文本还包括输入，要把输入部分截去。
        output_text = output_text[len(input_text):]

        print("[AI] >>> " + output_text)

        if args.use_chat_mode:
            chat_history.append((current_user_input, output_text))

