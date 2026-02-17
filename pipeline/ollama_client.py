import requests
import json


def list_models(port=11434):
    url = f"http://localhost:{port}/api/tags"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    models = resp.json().get("models", [])
    return [m["name"] for m in models]


def stream_generate(model, prompt, port=11434, temperature=0.7, callback=None, cancel_check=None):
    url = f"http://localhost:{port}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {"temperature": temperature},
    }
    full_response = ""
    with requests.post(url, json=payload, stream=True, timeout=300) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if cancel_check and cancel_check():
                resp.close()
                break
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                full_response += token
                if callback:
                    callback(token)
                if data.get("done", False):
                    break
    return full_response
