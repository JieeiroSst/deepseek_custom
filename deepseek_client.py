# deepseek_client.py
# Module chính để giao tiếp với DeepSeek AI

import requests
import json
from typing import List, Dict, Optional
from config import OLLAMA_URL, MODEL_NAME, SCENARIOS

class DeepSeekClient:
    """Client để tương tác với DeepSeek AI qua Ollama"""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.ollama_url = OLLAMA_URL
        self.conversation_history = []
        
    def check_connection(self) -> bool:
        """Kiểm tra kết nối với Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def list_models(self) -> List[str]:
        """Lấy danh sách models đã cài"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model['name'] for model in models]
            return []
        except Exception as e:
            print(f"Lỗi khi lấy danh sách models: {e}")
            return []
    
    def chat(
        self, 
        user_message: str, 
        scenario: str = "default",
        use_history: bool = False,
        temperature: Optional[float] = None
    ) -> str:
        """
        Gửi tin nhắn và nhận phản hồi
        
        Args:
            user_message: Câu hỏi của người dùng
            scenario: Kịch bản sử dụng (từ SCENARIOS)
            use_history: Có sử dụng lịch sử chat không
            temperature: Độ sáng tạo (0.0-1.0), None = dùng mặc định
            
        Returns:
            Câu trả lời từ AI
        """
        if scenario not in SCENARIOS:
            scenario = "default"
        
        scenario_config = SCENARIOS[scenario]
        system_prompt = scenario_config["system_prompt"]
        temp = temperature if temperature is not None else scenario_config.get("temperature", 0.7)
        
        # Tạo messages
        messages = []
        
        # Thêm system prompt
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Thêm lịch sử hội thoại nếu cần
        if use_history:
            messages.extend(self.conversation_history)
        
        # Thêm tin nhắn người dùng
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Gửi request
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temp
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['message']['content']
                
                # Lưu vào lịch sử
                if use_history:
                    self.conversation_history.append({
                        "role": "user",
                        "content": user_message
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                
                return ai_response
            else:
                return f"Lỗi: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Lỗi: Timeout - AI mất quá nhiều thời gian để phản hồi"
        except requests.exceptions.ConnectionError:
            return "Lỗi: Không thể kết nối với Ollama. Bạn đã chạy 'ollama serve' chưa?"
        except Exception as e:
            return f"Lỗi: {str(e)}"
    
    def chat_stream(
        self,
        user_message: str,
        scenario: str = "default",
        temperature: Optional[float] = None
    ):
        """
        Chat với streaming response (trả về từng phần)
        """
        if scenario not in SCENARIOS:
            scenario = "default"
        
        scenario_config = SCENARIOS[scenario]
        system_prompt = scenario_config["system_prompt"]
        temp = temperature if temperature is not None else scenario_config.get("temperature", 0.7)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": temp
                }
            }
            
            response = requests.post(
                self.ollama_url, 
                json=payload, 
                stream=True,
                timeout=60
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'message' in data:
                        yield data['message']['content']
                        
        except Exception as e:
            yield f"Lỗi: {str(e)}"
    
    def clear_history(self):
        """Xóa lịch sử hội thoại"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Lấy lịch sử hội thoại"""
        return self.conversation_history
    
    def export_conversation(self, filename: str = "conversation.json"):
        """Xuất hội thoại ra file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        return filename


class ScenarioManager:
    """Quản lý các kịch bản custom"""
    
    @staticmethod
    def list_scenarios() -> Dict:
        """Lấy danh sách tất cả kịch bản"""
        return {
            key: {
                "name": value["name"],
                "temperature": value.get("temperature", 0.7)
            }
            for key, value in SCENARIOS.items()
        }
    
    @staticmethod
    def get_scenario(scenario_name: str) -> Optional[Dict]:
        """Lấy thông tin chi tiết của một kịch bản"""
        return SCENARIOS.get(scenario_name)
    
    @staticmethod
    def add_scenario(
        key: str,
        name: str,
        system_prompt: str,
        temperature: float = 0.7
    ):
        """Thêm kịch bản mới"""
        SCENARIOS[key] = {
            "name": name,
            "system_prompt": system_prompt,
            "temperature": temperature
        }


# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo client
    client = DeepSeekClient()
    
    # Kiểm tra kết nối
    print("🔍 Kiểm tra kết nối Ollama...")
    if client.check_connection():
        print("✅ Kết nối thành công!")
        
        # Liệt kê models
        models = client.list_models()
        print(f"\n📦 Models đã cài: {models}")
    else:
        print("❌ Không thể kết nối. Hãy chạy: ollama serve")
        exit(1)
    
    # Test chat với kịch bản khác nhau
    print("\n" + "="*50)
    print("TEST CHAT VỚI CÁC KỊCH BẢN")
    print("="*50)
    
    # Test 1: Default
    print("\n1️⃣  Kịch bản: DEFAULT")
    response = client.chat("Xin chào, bạn là ai?", scenario="default")
    print(f"AI: {response}")
    
    # Test 2: Customer Support
    print("\n2️⃣  Kịch bản: CUSTOMER SUPPORT")
    response = client.chat("Tôi quên mật khẩu", scenario="customer_support")
    print(f"AI: {response}")
    
    # Test 3: Teacher
    print("\n3️⃣  Kịch bản: TEACHER")
    response = client.chat("Giải thích cho tôi về biến trong Python", scenario="teacher")
    print(f"AI: {response}")
    
    # Test 4: Chat với lịch sử
    print("\n4️⃣  Chat với lịch sử:")
    client.clear_history()
    response1 = client.chat("Tên tôi là Minh", use_history=True)
    print(f"AI: {response1}")
    
    response2 = client.chat("Tên tôi là gì?", use_history=True)
    print(f"AI: {response2}")
