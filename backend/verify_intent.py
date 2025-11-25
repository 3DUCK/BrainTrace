import requests
import json

BASE_URL = "http://localhost:8000"

def test_simple_chat():
    print("\n--- Testing SIMPLE Chat ---")
    payload = {
        "question": "안녕, 너는 누구니?",
        "session_id": 1,
        "brain_id": 1,
        "model": "ollama",
        "model_name": "gemma2:9b",
        "use_deep_search": False
    }
    try:
        response = requests.post(f"{BASE_URL}/brainGraph/answer", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {response.status_code}")
            print(f"Intent: {data.get('intent')}")
            answer = data.get('answer', '')
            print(f"Answer: {answer}")
            
            if data.get('intent') == 'SIMPLE' and answer.startswith("[LLM]"):
                print("✅ SIMPLE Test Passed (Tag: [LLM])")
            else:
                print(f"❌ SIMPLE Test Failed. Intent: {data.get('intent')}, Answer starts with tag: {answer.startswith('[LLM]')}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_agent_chat():
    print("\n--- Testing AGENT Chat ---")
    payload = {
        "question": "광고비를 20% 줄이면 ROI가 어떻게 될까?",
        "session_id": 1,
        "brain_id": 1,
        "model": "ollama",
        "model_name": "gemma2:9b",
        "use_deep_search": False
    }
    try:
        response = requests.post(f"{BASE_URL}/brainGraph/answer", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {response.status_code}")
            print(f"Intent: {data.get('intent')}")
            answer = data.get('answer', '')
            print(f"Answer: {answer}")
            print(f"Agent Data: {data.get('agent_data')}")
            
            if data.get('intent') == 'AGENT' and data.get('agent_data') and answer.startswith("[Agent]"):
                print("✅ AGENT Test Passed (Tag: [Agent])")
            else:
                print(f"❌ AGENT Test Failed. Intent: {data.get('intent')}, Answer starts with tag: {answer.startswith('[Agent]')}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_rag_chat():
    print("\n--- Testing RAG Chat ---")
    payload = {
        "question": "BrainTrace 프로젝트에 대해 설명해줘",
        "session_id": 1,
        "brain_id": 1,
        "model": "ollama",
        "model_name": "gemma2:9b",
        "use_deep_search": False
    }
    try:
        response = requests.post(f"{BASE_URL}/brainGraph/answer", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {response.status_code}")
            intent = data.get('intent', 'RAG') 
            answer = data.get('answer', '')
            print(f"Intent: {intent}")
            print(f"Answer: {answer[:100]}...")
            
            if intent == 'RAG' and answer.startswith("[RAG]"):
                print("✅ RAG Test Passed (Tag: [RAG])")
            else:
                print(f"❌ RAG Test Failed. Intent: {intent}, Answer starts with tag: {answer.startswith('[RAG]')}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple_chat()
    test_agent_chat()
    test_rag_chat()
