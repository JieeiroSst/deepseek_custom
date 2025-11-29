# 🤖 DeepSeek AI - Custom Scenarios

Hệ thống chat AI tùy chỉnh sử dụng DeepSeek chạy local với các kịch bản theo ý muốn.

## 📋 Mục Lục
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Tùy chỉnh kịch bản](#tùy-chỉnh-kịch-bản)
- [API Reference](#api-reference)

## ✨ Tính Năng

- ✅ **Chat với AI Local** - Chạy 100% trên máy của bạn, không cần internet
- 🎭 **Nhiều kịch bản** - Hỗ trợ khách hàng, giáo viên, sales, kỹ thuật...
- 🧠 **Lịch sử hội thoại** - AI nhớ ngữ cảnh cuộc trò chuyện
- 🎨 **Giao diện CLI & Web** - Sử dụng qua terminal hoặc trình duyệt
- ⚙️ **Tùy chỉnh dễ dàng** - Thêm kịch bản mới chỉ với vài dòng code
- 💾 **Export hội thoại** - Lưu cuộc trò chuyện ra file JSON

## 💻 Yêu Cầu Hệ Thống

### Phần cứng tối thiểu:
- **RAM**: 8GB+ (16GB khuyến nghị)
- **CPU**: 4 cores+
- **Disk**: 10GB trống

### Phần mềm:
- **Python**: 3.8+
- **Ollama**: Latest version

## 🚀 Cài Đặt

### Bước 1: Cài Ollama

#### Linux/Mac:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
Tải từ: https://ollama.com/download

### Bước 2: Tải Model DeepSeek

```bash
# Model nhỏ (1.5B) - Nhanh, ít RAM
ollama pull deepseek-r1:1.5b

# Model lớn (7B) - Thông minh hơn, cần RAM nhiều
ollama pull deepseek-r1:7b
```

### Bước 3: Clone Project

```bash
git clone <repo-url>
cd deepseek_custom
```

### Bước 4: Cài Dependencies

```bash
pip install -r requirements.txt
```

### Bước 5: Chạy Ollama Server

Mở terminal mới và chạy:
```bash
ollama serve
```

Để terminal này chạy trong suốt quá trình sử dụng.

## 📖 Sử Dụng

### Option 1: CLI (Terminal)

```bash
python cli.py
```

**Các lệnh trong CLI:**
- `chat` - Bắt đầu chat
- `scenarios` - Xem danh sách kịch bản
- `switch` - Đổi kịch bản
- `history on/off` - Bật/tắt lịch sử
- `clear` - Xóa lịch sử
- `export` - Xuất hội thoại
- `models` - Xem models đã cài
- `quit` - Thoát

### Option 2: Web Interface

```bash
python app.py
```

Mở trình duyệt: http://localhost:5000

### Option 3: Sử dụng Python Code

```python
from deepseek_client import DeepSeekClient

# Khởi tạo
client = DeepSeekClient()

# Chat đơn giản
response = client.chat("Xin chào!", scenario="default")
print(response)

# Chat với kịch bản customer support
response = client.chat(
    "Tôi quên mật khẩu", 
    scenario="customer_support"
)
print(response)

# Chat có lịch sử
client.chat("Tên tôi là Minh", use_history=True)
response = client.chat("Tên tôi là gì?", use_history=True)
print(response)  # AI sẽ nhớ tên bạn
```

## 🎭 Tùy Chỉnh Kịch Bản

### Cách 1: Sửa file config.py

Mở file `config.py` và thêm kịch bản mới:

```python
SCENARIOS = {
    # Kịch bản có sẵn...
    
    # Thêm kịch bản mới
    "doctor": {
        "name": "Bác sĩ tư vấn",
        "system_prompt": """Bạn là bác sĩ chuyên khoa.
        Nhiệm vụ:
        - Tư vấn sức khỏe cơ bản
        - Đưa ra lời khuyên y tế
        - Khuyến nghị đi khám khi cần
        
        Lưu ý: Luôn nhắc người dùng đến gặp bác sĩ thật nếu vấn đề nghiêm trọng.""",
        "temperature": 0.3  # Thấp = Chính xác hơn
    }
}
```

### Cách 2: Thêm qua Code

```python
from deepseek_client import ScenarioManager

ScenarioManager.add_scenario(
    key="chef",
    name="Đầu bếp chuyên nghiệp",
    system_prompt="Bạn là đầu bếp 5 sao...",
    temperature=0.8
)
```

### Tham Số Temperature

- **0.0 - 0.3**: Câu trả lời chính xác, ít sáng tạo (phù hợp: kỹ thuật, y tế)
- **0.4 - 0.6**: Cân bằng (phù hợp: giáo dục, hỗ trợ)
- **0.7 - 1.0**: Sáng tạo, đa dạng (phù hợp: nội dung, brainstorm)

## 🔌 API Reference

### DeepSeekClient

#### `__init__(model_name: str)`
Khởi tạo client.

```python
client = DeepSeekClient(model_name="deepseek-r1:7b")
```

#### `chat(user_message, scenario, use_history, temperature)`
Chat với AI.

**Parameters:**
- `user_message` (str): Câu hỏi
- `scenario` (str): Tên kịch bản (default: "default")
- `use_history` (bool): Dùng lịch sử không (default: False)
- `temperature` (float): Độ sáng tạo (default: từ scenario)

**Returns:** str - Câu trả lời

```python
response = client.chat(
    "Giải thích Python",
    scenario="teacher",
    use_history=True,
    temperature=0.6
)
```

#### `chat_stream(user_message, scenario, temperature)`
Chat với streaming response.

```python
for chunk in client.chat_stream("Viết story", scenario="creative"):
    print(chunk, end='', flush=True)
```

#### `clear_history()`
Xóa lịch sử hội thoại.

#### `get_history()`
Lấy lịch sử hội thoại.

#### `export_conversation(filename)`
Xuất hội thoại ra file.

### ScenarioManager

#### `list_scenarios()`
Lấy danh sách kịch bản.

```python
scenarios = ScenarioManager.list_scenarios()
for key, info in scenarios.items():
    print(f"{key}: {info['name']}")
```

#### `get_scenario(scenario_name)`
Lấy chi tiết kịch bản.

#### `add_scenario(key, name, system_prompt, temperature)`
Thêm kịch bản mới.

## 📁 Cấu Trúc Project

```
deepseek_custom/
├── config.py              # Cấu hình kịch bản
├── deepseek_client.py     # Core client
├── cli.py                 # CLI interface
├── app.py                 # Web server
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html        # Web UI
└── README.md             # Documentation
```

## 🐛 Troubleshooting

### Lỗi "Connection refused"
**Nguyên nhân:** Ollama chưa chạy
**Giải pháp:**
```bash
ollama serve
```

### Lỗi "Model not found"
**Nguyên nhân:** Chưa tải model
**Giải pháp:**
```bash
ollama pull deepseek-r1:1.5b
```

### AI phản hồi chậm
**Nguyên nhân:** Model quá lớn cho RAM
**Giải pháp:** Dùng model nhỏ hơn (1.5b thay vì 7b)

### Lỗi "Port 5000 already in use"
**Giải pháp:** Đổi port trong `app.py`:
```python
app.run(debug=True, port=5001)  # Đổi thành 5001
```

## 💡 Tips & Tricks

### 1. Tối ưu hiệu suất
```python
# Giảm temperature cho câu trả lời nhanh hơn
client.chat("Hello", temperature=0.1)
```

### 2. Tạo chatbot chuyên dụng
```python
# Bot hỗ trợ kỹ thuật
tech_bot = DeepSeekClient()
response = tech_bot.chat(
    "Code Python bị lỗi",
    scenario="technical",
    use_history=True
)
```

### 3. Batch processing
```python
questions = ["Q1", "Q2", "Q3"]
answers = [client.chat(q) for q in questions]
```

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy:
1. Fork repo
2. Tạo branch mới
3. Commit changes
4. Tạo Pull Request

## 📝 License

MIT License - Tự do sử dụng cho mọi mục đích.

## 🙏 Credits

- DeepSeek AI Team
- Ollama Project
- Flask Framework

## 📞 Hỗ Trợ

- Issues: Tạo issue trên GitHub
- Discussions: Thảo luận trong Discussions tab
- Email: your-email@example.com

---

**Chúc bạn thành công! 🚀**
