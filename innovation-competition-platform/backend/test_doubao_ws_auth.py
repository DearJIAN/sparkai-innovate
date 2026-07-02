import os
import sys
import inspect
import asyncio
from pathlib import Path

# Load dotenv safely
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    env_loaded = True
except ImportError:
    env_loaded = False

import websockets

def mask_key(k):
    if not k: return "<EMPTY>"
    if len(k) <= 10: return "***"
    return k[:6] + "***" + k[-4:]

def check_env():
    print("=== 一、确认当前进程实际读取到的环境变量 ===")
    print(f"python version: {sys.version.split()[0]}")
    print(f"websockets version: {getattr(websockets, '__version__', 'unknown')}")
    print(f"Env Loaded via dotenv: {env_loaded}")
    print(f"Current Working Directory: {os.getcwd()}")
    try:
        print(f".env Path: {env_path.absolute()}")
    except:
        pass
    
    tts_provider = os.environ.get("TTS_PROVIDER", "")
    api_key = os.environ.get("DOUBAO_TTS_API_KEY", "").strip()
    resource_id = os.environ.get("DOUBAO_TTS_RESOURCE_ID", "").strip()
    endpoint = os.environ.get("DOUBAO_TTS_WS_ENDPOINT", "").strip()
    speaker = os.environ.get("DOUBAO_TTS_SPEAKER", "").strip()
    
    print(f"TTS_PROVIDER: {tts_provider}")
    print(f"DOUBAO_TTS_API_KEY EXISTS: {bool(api_key)}")
    print(f"DOUBAO_TTS_API_KEY LENGTH: {len(api_key)}")
    print(f"DOUBAO_TTS_API_KEY MASKED: {mask_key(api_key)}")
    print(f"DOUBAO_TTS_RESOURCE_ID: {resource_id}")
    print(f"DOUBAO_TTS_WS_ENDPOINT: {endpoint}")
    print(f"DOUBAO_TTS_SPEAKER: {speaker}")
    
    if api_key.startswith("apikey-"):
        print("【警告】当前填入的是 API Key 管理资源 ID，不是真正的 API Key。")
    elif api_key.startswith("ark-"):
        print("【注意】当前 Key 以 ark- 开头，等待握手测试验证有效性。")
        
    print("\n=== 八、检查代理和网络层 ===")
    for k in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy"]:
        if k in os.environ:
            print(f"Proxy Env found - {k}: {os.environ[k]}")
    print("Proxy check complete.")
    
    return api_key, resource_id, endpoint

def check_websockets_signature():
    print("\n=== 四、检查 websockets 版本兼容 ===")
    sig = inspect.signature(websockets.connect)
    has_additional = "additional_headers" in sig.parameters
    has_extra = "extra_headers" in sig.parameters
    
    header_kwarg = "additional_headers" if has_additional else ("extra_headers" if has_extra else None)
    print(f"Has additional_headers: {has_additional}")
    print(f"Has extra_headers: {has_extra}")
    print(f"Selected header kwarg: {header_kwarg}")
    return header_kwarg

async def min_handshake(api_key, resource_id, endpoint, header_kwarg):
    print("\n=== 五、编写独立最小握手测试 ===")
    import uuid
    headers = {
        "X-Api-Key": api_key,
        "X-Api-Resource-Id": resource_id,
        "X-Api-Connect-Id": str(uuid.uuid4()),
        "X-Control-Require-Usage-Tokens-Return": "*"
    }
    
    print("Attempting connection to:", endpoint)
    print("Headers sent keys:", list(headers.keys()))
    
    kwargs = {}
    if header_kwarg:
        kwargs[header_kwarg] = headers
        
    try:
        async with websockets.connect(endpoint, **kwargs) as ws:
            print("HTTP 握手成功")
            # We don't easily get response headers from high-level websockets.connect without accessing private attrs,
            # but usually it's in ws.response_headers
            if hasattr(ws, "response_headers"):
                print("Response Headers:")
                for k, v in ws.response_headers.items():
                    print(f"  {k}: {v}")
                    if k.lower() == "x-tt-logid":
                        print(f"x-tt-logid: {v}")
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Connection Failed with Status Code: {e.status_code}")
        print("Response Headers:")
        logid = None
        for k, v in e.headers.items():
            print(f"  {k}: {v}")
            if k.lower() == "x-tt-logid":
                logid = v
        if logid:
            print(f"x-tt-logid: {logid}")
        else:
            print("x-tt-logid not found in response headers.")
    except Exception as e:
        print(f"Exception Type: {type(e)}")
        print(f"Exception Details: {e}")

def main():
    api_key, resource_id, endpoint = check_env()
    if not endpoint:
        endpoint = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"
    if not resource_id:
        resource_id = "seed-tts-2.0"
        
    header_kwarg = check_websockets_signature()
    
    if not api_key:
        print("No API Key found, aborting handshake.")
        return
        
    asyncio.run(min_handshake(api_key, resource_id, endpoint, header_kwarg))

if __name__ == "__main__":
    main()
