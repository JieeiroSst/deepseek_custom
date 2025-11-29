# 🚀 QUICK START - API TESTING

Hướng dẫn nhanh để bắt đầu test API trong 5 phút!

---

## 📋 CHUẨN BỊ

### Bước 1: Khởi động API Server
```bash
python api_server.py
```

Server chạy tại: **http://localhost:8000**

### Bước 2: Kiểm tra kết nối
```bash
curl http://localhost:8000/health
```

Nếu thấy `"status": "healthy"` → OK! ✅

---

## 💬 5 LỆNH CURL CƠ BẢN

### 1️⃣ Chat đơn giản
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Xin chào!"}'
```

### 2️⃣ Chat với kịch bản khác
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tôi quên mật khẩu", "scenario": "customer_support"}'
```

### 3️⃣ Xem danh sách kịch bản
```bash
curl http://localhost:8000/api/scenarios
```

### 4️⃣ Chat có nhớ ngữ cảnh
```bash
# Tin nhắn 1
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tên tôi là Minh", "session_id": "test123", "use_history": true}'

# Tin nhắn 2 - AI sẽ nhớ tên
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tên tôi là gì?", "session_id": "test123", "use_history": true}'
```

### 5️⃣ Xử lý nhiều câu hỏi
```bash
curl -X POST http://localhost:8000/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["Xin chào", "Python là gì?", "2+2=?"],
    "scenario": "default"
  }'
```

---

## 🎯 CÁC KỊCH BẢN CÓ SẴN

| Kịch bản | Key | Mô tả |
|----------|-----|-------|
| Mặc định | `default` | Trợ lý AI thông minh |
| Hỗ trợ KH | `customer_support` | Nhân viên support |
| Giáo viên | `teacher` | Giảng dạy và giải thích |
| Bán hàng | `sales` | Tư vấn bán hàng |
| Kỹ thuật | `technical` | Chuyên gia IT |
| Sáng tạo | `creative` | Viết content |

**Sử dụng:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "câu hỏi", "scenario": "teacher"}'
```

---

## 🔧 TEST TỰ ĐỘNG

### Chạy script test
```bash
chmod +x test_curl.sh
./test_curl.sh
```

Script sẽ tự động test tất cả endpoints!

---

## 📱 TEST VỚI POSTMAN

### Import collection
1. Mở Postman
2. Click **Import**
3. Chọn file: `postman_collection.json`
4. Bắt đầu test!

### Hoặc sử dụng Postman API:
```bash
curl --location 'http://localhost:8000/api/chat' \
--header 'Content-Type: application/json' \
--data '{"message": "Hello"}'
```

---

## 🐍 TEST VỚI PYTHON

### Tạo file `quick_test.py`:
```python
import requests

API = "http://localhost:8000"

# Test 1: Simple chat
response = requests.post(f"{API}/api/chat", json={
    "message": "Xin chào!"
})
print(response.json()['response'])

# Test 2: With scenario
response = requests.post(f"{API}/api/chat", json={
    "message": "Giải thích Python",
    "scenario": "teacher"
})
print(response.json()['response'])

# Test 3: List scenarios
response = requests.get(f"{API}/api/scenarios")
print(response.json()['scenarios'].keys())
```

**Chạy:**
```bash
python quick_test.py
```

---

## 📊 XEM KẾT QUẢ ĐẸP HƠN

### Cài jq (JSON formatter)
```bash
# Linux
sudo apt-get install jq

# Mac
brew install jq
```

### Sử dụng với curl
```bash
curl -s http://localhost:8000/api/scenarios | jq '.'
```

### Chỉ lấy response
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' | jq -r '.response'
```

---

## 🎨 VÍ DỤ NÂNG CAO

### 1. Chat với Temperature cao (sáng tạo)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Viết một câu thơ về bầu trời",
    "scenario": "creative",
    "temperature": 0.9
  }'
```

### 2. Conversation flow (nhiều lượt)
```bash
# Tạo session
SESSION=$(curl -s -X POST http://localhost:8000/api/session | jq -r '.session_id')

# Chat lượt 1
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Tôi muốn học lập trình\",
    \"session_id\": \"$SESSION\",
    \"use_history\": true
  }" | jq -r '.response'

# Chat lượt 2
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Bắt đầu từ đâu?\",
    \"session_id\": \"$SESSION\",
    \"use_history\": true
  }" | jq -r '.response'

# Xem lịch sử
curl -s http://localhost:8000/api/session/$SESSION | jq '.history'
```

### 3. Batch processing FAQ
```bash
curl -X POST http://localhost:8000/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "Giờ làm việc?",
      "Địa chỉ shop?",
      "Chính sách đổi trả?",
      "Ship COD không?"
    ],
    "scenario": "customer_support"
  }' | jq '.results[].response'
```

---

## ⚡ TROUBLESHOOTING

### Lỗi: Connection refused
→ API server chưa chạy
```bash
python api_server.py
```

### Lỗi: "ollama_connected": false
→ Ollama chưa chạy
```bash
ollama serve
```

### Lỗi: Model not found
→ Chưa tải model
```bash
ollama pull deepseek-r1:1.5b
```

### Response chậm?
→ Dùng model nhỏ hơn hoặc giảm temperature

---

## 📚 TÀI LIỆU CHI TIẾT

- **API đầy đủ:** `CURL_API_GUIDE.md`
- **Hướng dẫn setup:** `README.md`
- **Code examples:** `examples.py`

---

## ✨ TIPS

### Lưu response vào file
```bash
curl ... > response.json
```

### Chạy trong background
```bash
python api_server.py > api.log 2>&1 &
```

### Kill process nếu bị treo
```bash
pkill -f api_server.py
```

### Đo thời gian response
```bash
time curl -X POST http://localhost:8000/api/chat ...
```

---

**🎉 Bắt đầu ngay! Copy một lệnh curl ở trên và paste vào terminal!**
