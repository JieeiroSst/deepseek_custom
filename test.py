# test.py
# Script để test các chức năng

from deepseek_client import DeepSeekClient, ScenarioManager
from config import SCENARIOS
import time

def print_header(text):
    """In header đẹp"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_connection():
    """Test kết nối Ollama"""
    print_header("1. KIỂM TRA KẾT NỐI")
    client = DeepSeekClient()
    
    if client.check_connection():
        print("✅ Kết nối Ollama: THÀNH CÔNG")
        
        models = client.list_models()
        if models:
            print(f"✅ Đã tìm thấy {len(models)} models:")
            for model in models:
                print(f"   - {model}")
        else:
            print("⚠️  Chưa có model nào được cài")
            print("   Chạy: ollama pull deepseek-r1:1.5b")
        return True
    else:
        print("❌ Kết nối Ollama: THẤT BẠI")
        print("   Hãy chạy: ollama serve")
        return False

def test_scenarios():
    """Test danh sách kịch bản"""
    print_header("2. KIỂM TRA KỊCH BẢN")
    
    scenarios = ScenarioManager.list_scenarios()
    print(f"✅ Tìm thấy {len(scenarios)} kịch bản:")
    
    for key, info in scenarios.items():
        print(f"\n   📋 {key}")
        print(f"      Tên: {info['name']}")
        print(f"      Temperature: {info['temperature']}")

def test_simple_chat():
    """Test chat đơn giản"""
    print_header("3. TEST CHAT ĐơN GIẢN")
    
    client = DeepSeekClient()
    
    print("\n🤖 Kịch bản: DEFAULT")
    print("👤 Câu hỏi: Xin chào, bạn là ai?")
    print("⏳ Đang chờ phản hồi...")
    
    start_time = time.time()
    response = client.chat("Xin chào, bạn là ai?", scenario="default")
    elapsed = time.time() - start_time
    
    print(f"\n🤖 AI phản hồi ({elapsed:.2f}s):")
    print(f"   {response}")

def test_different_scenarios():
    """Test các kịch bản khác nhau"""
    print_header("4. TEST NHIỀU KỊCH BẢN")
    
    client = DeepSeekClient()
    
    test_cases = [
        ("customer_support", "Làm sao để đổi mật khẩu?"),
        ("teacher", "Giải thích vòng lặp for trong Python"),
        ("technical", "Sự khác biệt giữa list và tuple?"),
    ]
    
    for scenario, question in test_cases:
        scenario_name = SCENARIOS[scenario]['name']
        print(f"\n📋 Kịch bản: {scenario_name}")
        print(f"👤 Câu hỏi: {question}")
        print("⏳ Đang chờ...")
        
        start_time = time.time()
        response = client.chat(question, scenario=scenario)
        elapsed = time.time() - start_time
        
        # Hiển thị 200 ký tự đầu
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"🤖 AI ({elapsed:.2f}s): {preview}\n")

def test_conversation_history():
    """Test lịch sử hội thoại"""
    print_header("5. TEST LỊCH SỬ HỘI THOẠI")
    
    client = DeepSeekClient()
    
    print("\n💬 Cuộc trò chuyện 1:")
    print("👤 Tên tôi là Minh")
    response1 = client.chat("Tên tôi là Minh", use_history=True)
    print(f"🤖 {response1}")
    
    print("\n💬 Cuộc trò chuyện 2:")
    print("👤 Tên tôi là gì?")
    response2 = client.chat("Tên tôi là gì?", use_history=True)
    print(f"🤖 {response2}")
    
    # Kiểm tra xem AI có nhớ không
    if "Minh" in response2 or "minh" in response2.lower():
        print("\n✅ AI nhớ tên người dùng!")
    else:
        print("\n⚠️  AI không nhớ - có thể cần điều chỉnh")

def test_temperature_variations():
    """Test các mức temperature khác nhau"""
    print_header("6. TEST TEMPERATURE")
    
    client = DeepSeekClient()
    question = "Viết một câu về con mèo"
    
    temps = [0.1, 0.5, 0.9]
    
    for temp in temps:
        print(f"\n🌡️  Temperature: {temp}")
        print(f"👤 Câu hỏi: {question}")
        
        response = client.chat(question, temperature=temp)
        print(f"🤖 {response[:150]}...")

def test_export():
    """Test export conversation"""
    print_header("7. TEST EXPORT")
    
    client = DeepSeekClient()
    
    # Tạo vài cuộc hội thoại
    client.chat("Xin chào", use_history=True)
    client.chat("Tên tôi là Test", use_history=True)
    
    # Export
    filename = client.export_conversation("test_conversation.json")
    print(f"✅ Đã export ra file: {filename}")

def run_all_tests():
    """Chạy tất cả tests"""
    print("\n" + "🧪 " * 20)
    print("BẮT ĐẦU KIỂM TRA HỆ THỐNG")
    print("🧪 " * 20)
    
    # Test 1: Kết nối
    if not test_connection():
        print("\n⚠️  Không thể tiếp tục test vì chưa kết nối được Ollama")
        return
    
    # Test 2: Kịch bản
    test_scenarios()
    
    # Hỏi có muốn test chat không
    print("\n" + "="*60)
    print("⚠️  Các test tiếp theo sẽ gọi AI và có thể mất thời gian")
    choice = input("Bạn có muốn tiếp tục? (y/n): ").lower()
    
    if choice != 'y':
        print("\n👋 Đã dừng test. Chạy lại bất cứ lúc nào!")
        return
    
    # Test 3-7: Chat tests
    test_simple_chat()
    test_different_scenarios()
    test_conversation_history()
    test_temperature_variations()
    test_export()
    
    # Kết luận
    print("\n" + "🎉 " * 20)
    print("HOÀN THÀNH TẤT CẢ TESTS!")
    print("🎉 " * 20)
    print("\n✅ Hệ thống hoạt động tốt!")
    print("\n📝 Các bước tiếp theo:")
    print("   1. Chạy CLI: python cli.py")
    print("   2. Chạy Web: python app.py")
    print("   3. Tùy chỉnh kịch bản trong config.py")

if __name__ == "__main__":
    run_all_tests()
