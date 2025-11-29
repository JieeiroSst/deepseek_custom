# examples.py
# Các ví dụ sử dụng nâng cao

from deepseek_client import DeepSeekClient, ScenarioManager
from config import SCENARIOS
import json

def example_basic_chat():
    """Ví dụ 1: Chat cơ bản"""
    print("="*60)
    print("VÍ DỤ 1: CHAT CƠ BẢN")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Chat đơn giản
    response = client.chat("Xin chào!", scenario="default")
    print(f"AI: {response}\n")


def example_customer_support_bot():
    """Ví dụ 2: Bot hỗ trợ khách hàng"""
    print("="*60)
    print("VÍ DỤ 2: BOT HỖ TRỢ KHÁCH HÀNG")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Kịch bản: Khách hàng gặp vấn đề
    questions = [
        "Tôi không thể đăng nhập vào tài khoản",
        "Tôi đã thử quên mật khẩu nhưng không nhận được email",
        "Email của tôi là user@example.com",
    ]
    
    for q in questions:
        print(f"\n👤 Khách: {q}")
        response = client.chat(
            q, 
            scenario="customer_support",
            use_history=True  # Nhớ ngữ cảnh
        )
        print(f"🤖 Support: {response}")


def example_teaching_assistant():
    """Ví dụ 3: Trợ lý giảng dạy"""
    print("\n" + "="*60)
    print("VÍ DỤ 3: TRỢ LÝ GIẢNG DẠY PYTHON")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Dạy về Python
    lesson_flow = [
        "Giải thích biến trong Python là gì",
        "Đưa ví dụ về biến",
        "Tôi có thể đặt tên biến là 123abc được không?"
    ]
    
    for question in lesson_flow:
        print(f"\n👨‍🎓 Học viên: {question}")
        response = client.chat(
            question,
            scenario="teacher",
            use_history=True
        )
        print(f"👨‍🏫 Giáo viên: {response}")


def example_sales_conversation():
    """Ví dụ 4: Cuộc trò chuyện bán hàng"""
    print("\n" + "="*60)
    print("VÍ DỤ 4: TƯ VẤN BÁN HÀNG")
    print("="*60)
    
    client = DeepSeekClient()
    
    conversation = [
        "Tôi muốn mua laptop",
        "Ngân sách khoảng 20 triệu",
        "Dùng cho lập trình và thiết kế đồ họa",
    ]
    
    for msg in conversation:
        print(f"\n👤 Khách: {msg}")
        response = client.chat(
            msg,
            scenario="sales",
            use_history=True
        )
        print(f"💼 Sales: {response}")


def example_technical_support():
    """Ví dụ 5: Hỗ trợ kỹ thuật"""
    print("\n" + "="*60)
    print("VÍ DỤ 5: HỖ TRỢ KỸ THUẬT LẬP TRÌNH")
    print("="*60)
    
    client = DeepSeekClient()
    
    technical_questions = [
        "Làm sao để đọc file JSON trong Python?",
        "Code của bạn bị lỗi 'FileNotFoundError'",
        "File của tôi nằm ở thư mục khác"
    ]
    
    for q in technical_questions:
        print(f"\n👨‍💻 Dev: {q}")
        response = client.chat(
            q,
            scenario="technical",
            use_history=True
        )
        print(f"🔧 Expert: {response}")


def example_creative_writing():
    """Ví dụ 6: Sáng tạo nội dung"""
    print("\n" + "="*60)
    print("VÍ DỤ 6: SÁNG TẠO NỘI DUNG")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Viết content với temperature cao = sáng tạo hơn
    prompts = [
        "Viết một đoạn mở đầu cho blog về du lịch Đà Lạt",
        "Thêm chi tiết về ẩm thực",
    ]
    
    for prompt in prompts:
        print(f"\n✍️  Yêu cầu: {prompt}")
        response = client.chat(
            prompt,
            scenario="creative",
            use_history=True,
            temperature=0.9  # Sáng tạo cao
        )
        print(f"🎨 Content: {response}")


def example_custom_scenario():
    """Ví dụ 7: Tạo kịch bản riêng"""
    print("\n" + "="*60)
    print("VÍ DỤ 7: TẠO KỊCH BẢN TÙY CHỈNH")
    print("="*60)
    
    # Thêm kịch bản mới: Fitness Coach
    ScenarioManager.add_scenario(
        key="fitness_coach",
        name="Huấn luyện viên Fitness",
        system_prompt="""Bạn là huấn luyện viên fitness chuyên nghiệp.
        
        Nhiệm vụ:
        - Tư vấn chế độ tập luyện
        - Hướng dẫn dinh dưỡng
        - Động viên và khích lệ
        - An toàn là ưu tiên hàng đầu
        
        Phong cách: Nhiệt tình, chuyên nghiệp, khích lệ""",
        temperature=0.7
    )
    
    client = DeepSeekClient()
    
    questions = [
        "Tôi muốn tăng cơ",
        "Tôi nặng 70kg, cao 1m75",
    ]
    
    for q in questions:
        print(f"\n💪 Học viên: {q}")
        response = client.chat(
            q,
            scenario="fitness_coach",
            use_history=True
        )
        print(f"🏋️ Coach: {response}")


def example_temperature_comparison():
    """Ví dụ 8: So sánh temperature"""
    print("\n" + "="*60)
    print("VÍ DỤ 8: SO SÁNH TEMPERATURE")
    print("="*60)
    
    client = DeepSeekClient()
    question = "Viết một câu mô tả bầu trời"
    
    temps = [
        (0.1, "Rất chính xác"),
        (0.5, "Cân bằng"),
        (0.9, "Rất sáng tạo")
    ]
    
    for temp, description in temps:
        print(f"\n🌡️  Temperature {temp} ({description}):")
        print(f"❓ Câu hỏi: {question}")
        
        response = client.chat(
            question,
            scenario="creative",
            temperature=temp
        )
        print(f"💬 Phản hồi: {response}")


def example_conversation_export():
    """Ví dụ 9: Export cuộc hội thoại"""
    print("\n" + "="*60)
    print("VÍ DỤ 9: EXPORT CUỘC HỘI THOẠI")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Tạo cuộc hội thoại
    messages = [
        "Xin chào",
        "Tôi cần học Python",
        "Bắt đầu từ đâu?"
    ]
    
    for msg in messages:
        print(f"👤 {msg}")
        response = client.chat(msg, use_history=True)
        print(f"🤖 {response}\n")
    
    # Export
    filename = "conversation_export.json"
    client.export_conversation(filename)
    print(f"✅ Đã lưu cuộc hội thoại vào: {filename}")
    
    # Đọc và hiển thị
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"\n📄 Nội dung file ({len(data)} tin nhắn):")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")


def example_batch_processing():
    """Ví dụ 10: Xử lý hàng loạt câu hỏi"""
    print("\n" + "="*60)
    print("VÍ DỤ 10: XỬ LÝ HÀNG LOẠT")
    print("="*60)
    
    client = DeepSeekClient()
    
    # Danh sách câu hỏi FAQ
    faqs = [
        "Giờ làm việc của bạn?",
        "Địa chỉ cửa hàng?",
        "Chính sách đổi trả?"
    ]
    
    print("Đang xử lý {} câu hỏi...\n".format(len(faqs)))
    
    results = []
    for i, question in enumerate(faqs, 1):
        print(f"[{i}/{len(faqs)}] {question}")
        answer = client.chat(question, scenario="customer_support")
        results.append({
            "question": question,
            "answer": answer
        })
        # Hiển thị preview
        preview = answer[:100] + "..." if len(answer) > 100 else answer
        print(f"    → {preview}\n")
    
    # Lưu kết quả
    with open("faq_answers.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("✅ Đã lưu kết quả vào: faq_answers.json")


def run_all_examples():
    """Chạy tất cả ví dụ"""
    print("\n" + "🚀 " * 20)
    print("CHẠY TẤT CẢ VÍ DỤ")
    print("🚀 " * 20)
    
    examples = [
        ("Chat cơ bản", example_basic_chat),
        ("Bot hỗ trợ khách hàng", example_customer_support_bot),
        ("Trợ lý giảng dạy", example_teaching_assistant),
        ("Tư vấn bán hàng", example_sales_conversation),
        ("Hỗ trợ kỹ thuật", example_technical_support),
        ("Sáng tạo nội dung", example_creative_writing),
        ("Tạo kịch bản tùy chỉnh", example_custom_scenario),
        ("So sánh temperature", example_temperature_comparison),
        ("Export hội thoại", example_conversation_export),
        ("Xử lý hàng loạt", example_batch_processing),
    ]
    
    print("\nChọn ví dụ để chạy:")
    print("0. Chạy tất cả")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    choice = input("\nNhập số (0-10): ").strip()
    
    if choice == "0":
        for name, func in examples:
            try:
                func()
                input("\nNhấn Enter để tiếp tục...")
            except Exception as e:
                print(f"❌ Lỗi: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        examples[idx][1]()
    else:
        print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    run_all_examples()
