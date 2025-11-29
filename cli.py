# cli.py
# Giao diện dòng lệnh để chat với DeepSeek

import sys
from deepseek_client import DeepSeekClient, ScenarioManager
from config import SCENARIOS

class ChatCLI:
    """Giao diện CLI để chat"""
    
    def __init__(self):
        self.client = DeepSeekClient()
        self.current_scenario = "default"
        self.use_history = False
        
    def print_menu(self):
        """In menu chính"""
        print("\n" + "="*60)
        print("🤖 DEEPSEEK AI - CUSTOM SCENARIOS")
        print("="*60)
        print("\nCÁC LỆNH:")
        print("  chat        - Bắt đầu chat")
        print("  scenarios   - Xem danh sách kịch bản")
        print("  switch      - Đổi kịch bản")
        print("  history on  - Bật lịch sử hội thoại")
        print("  history off - Tắt lịch sử hội thoại")
        print("  clear       - Xóa lịch sử")
        print("  export      - Xuất hội thoại ra file")
        print("  models      - Xem models đã cài")
        print("  quit        - Thoát")
        print("="*60)
        
    def show_scenarios(self):
        """Hiển thị danh sách kịch bản"""
        scenarios = ScenarioManager.list_scenarios()
        print("\n📋 DANH SÁCH KỊCH BẢN:")
        print("-" * 60)
        for key, info in scenarios.items():
            current = "👉 " if key == self.current_scenario else "   "
            print(f"{current}{key:20s} - {info['name']}")
            print(f"      Temperature: {info['temperature']}")
        print("-" * 60)
        
    def switch_scenario(self):
        """Đổi kịch bản"""
        self.show_scenarios()
        print("\nNhập tên kịch bản (hoặc Enter để hủy): ", end="")
        scenario_key = input().strip()
        
        if scenario_key and scenario_key in SCENARIOS:
            self.current_scenario = scenario_key
            print(f"✅ Đã chuyển sang kịch bản: {SCENARIOS[scenario_key]['name']}")
            # Xóa lịch sử khi đổi kịch bản
            self.client.clear_history()
            print("📝 Lịch sử hội thoại đã được xóa")
        elif scenario_key:
            print("❌ Kịch bản không tồn tại!")
            
    def chat_mode(self):
        """Chế độ chat"""
        scenario_name = SCENARIOS[self.current_scenario]['name']
        history_status = "BẬT" if self.use_history else "TẮT"
        
        print(f"\n💬 CHẾ ĐỘ CHAT")
        print(f"Kịch bản: {scenario_name}")
        print(f"Lịch sử: {history_status}")
        print("Gõ 'exit' để quay lại menu")
        print("-" * 60)
        
        while True:
            print("\n👤 Bạn: ", end="")
            user_input = input().strip()
            
            if user_input.lower() == 'exit':
                break
                
            if not user_input:
                continue
            
            print("🤖 AI đang suy nghĩ...")
            response = self.client.chat(
                user_input,
                scenario=self.current_scenario,
                use_history=self.use_history
            )
            print(f"\n🤖 AI: {response}")
            
    def toggle_history(self, status: str):
        """Bật/tắt lịch sử"""
        if status == "on":
            self.use_history = True
            print("✅ Đã BẬT lịch sử hội thoại")
        elif status == "off":
            self.use_history = False
            print("✅ Đã TẮT lịch sử hội thoại")
            
    def show_models(self):
        """Hiển thị models đã cài"""
        print("\n🔍 Đang kiểm tra models...")
        models = self.client.list_models()
        if models:
            print("\n📦 MODELS ĐÃ CÀI:")
            for model in models:
                current = "👉 " if model == self.client.model_name else "   "
                print(f"{current}{model}")
        else:
            print("❌ Không tìm thấy model nào hoặc Ollama chưa chạy")
            
    def run(self):
        """Chạy CLI"""
        # Kiểm tra kết nối
        print("🔍 Kiểm tra kết nối Ollama...")
        if not self.client.check_connection():
            print("❌ Không thể kết nối với Ollama!")
            print("\n💡 Hướng dẫn:")
            print("1. Cài Ollama: curl -fsSL https://ollama.com/install.sh | sh")
            print("2. Chạy Ollama: ollama serve")
            print("3. Tải model: ollama pull deepseek-r1:1.5b")
            return
        
        print("✅ Kết nối thành công!\n")
        
        while True:
            self.print_menu()
            print(f"\nKịch bản hiện tại: {SCENARIOS[self.current_scenario]['name']}")
            print("Nhập lệnh: ", end="")
            
            command = input().strip().lower()
            
            if command == "quit" or command == "exit":
                print("\n👋 Tạm biệt!")
                break
            elif command == "chat":
                self.chat_mode()
            elif command == "scenarios":
                self.show_scenarios()
            elif command == "switch":
                self.switch_scenario()
            elif command.startswith("history "):
                status = command.split()[1]
                self.toggle_history(status)
            elif command == "clear":
                self.client.clear_history()
                print("✅ Đã xóa lịch sử hội thoại")
            elif command == "export":
                filename = self.client.export_conversation()
                print(f"✅ Đã xuất hội thoại ra file: {filename}")
            elif command == "models":
                self.show_models()
            else:
                print("❌ Lệnh không hợp lệ!")


if __name__ == "__main__":
    cli = ChatCLI()
    cli.run()
