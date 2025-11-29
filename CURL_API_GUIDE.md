# CURL API TEST GUIDE
# Tài liệu đầy đủ các lệnh curl để test API

## Khởi động API Server
```bash
python api_server.py
```
Server sẽ chạy tại: http://localhost:8000

---

## 1. HEALTH CHECK

### Kiểm tra trạng thái API
```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "ollama_connected": true,
  "active_sessions": 0
}
```

---

## 2. SCENARIOS (Kịch bản)

### 2.1. Lấy danh sách tất cả kịch bản
```bash
curl -X GET http://localhost:8000/api/scenarios
```

**Response:**
```json
{
  "success": true,
  "count": 6,
  "scenarios": {
    "default": {
      "name": "Trợ lý thông minh",
      "temperature": 0.7
    },
    "customer_support": {
      "name": "Hỗ trợ khách hàng",
      "temperature": 0.5
    }
  }
}
```

### 2.2. Lấy chi tiết một kịch bản
```bash
curl -X GET http://localhost:8000/api/scenarios/teacher
```

**Response:**
```json
{
  "success": true,
  "scenario_id": "teacher",
  "scenario": {
    "name": "Giáo viên",
    "system_prompt": "Bạn là một giáo viên...",
    "temperature": 0.6
  }
}
```

---

## 3. CHAT

### 3.1. Chat đơn giản (không lưu lịch sử)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Xin chào, bạn là ai?"
  }'
```

**Response:**
```json
{
  "success": true,
  "session_id": "abc123...",
  "response": "Xin chào! Tôi là trợ lý AI...",
  "scenario": "default",
  "elapsed_time": 1.23,
  "timestamp": 1234567890.123
}
```

### 3.2. Chat với kịch bản cụ thể
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tôi quên mật khẩu",
    "scenario": "customer_support"
  }'
```

### 3.3. Chat với lịch sử (nhớ ngữ cảnh)
```bash
# Tin nhắn 1
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tên tôi là Minh",
    "session_id": "my_session_123",
    "use_history": true
  }'

# Tin nhắn 2 - AI sẽ nhớ tên
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tên tôi là gì?",
    "session_id": "my_session_123",
    "use_history": true
  }'
```

### 3.4. Chat với temperature tùy chỉnh
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Viết một câu về bầu trời",
    "scenario": "creative",
    "temperature": 0.9
  }'
```

### 3.5. Chat streaming (nhận từng phần)
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Kể một câu chuyện ngắn",
    "scenario": "creative"
  }'
```

---

## 4. SESSION MANAGEMENT

### 4.1. Tạo session mới
```bash
curl -X POST http://localhost:8000/api/session
```

**Response:**
```json
{
  "success": true,
  "session_id": "abc123def456...",
  "created_at": 1234567890.123
}
```

### 4.2. Lấy thông tin session
```bash
curl -X GET http://localhost:8000/api/session/abc123def456
```

**Response:**
```json
{
  "success": true,
  "session_id": "abc123def456",
  "created_at": 1234567890.123,
  "last_active": 1234567900.456,
  "message_count": 4,
  "history": [
    {
      "role": "user",
      "content": "Xin chào"
    },
    {
      "role": "assistant",
      "content": "Xin chào! Tôi có thể giúp gì..."
    }
  ]
}
```

### 4.3. Xóa lịch sử chat của session
```bash
curl -X DELETE http://localhost:8000/api/session/abc123def456/history
```

**Response:**
```json
{
  "success": true,
  "message": "History cleared"
}
```

### 4.4. Xóa session hoàn toàn
```bash
curl -X DELETE http://localhost:8000/api/session/abc123def456
```

**Response:**
```json
{
  "success": true,
  "message": "Session deleted"
}
```

---

## 5. MODELS

### Lấy danh sách models đã cài
```bash
curl -X GET http://localhost:8000/api/models
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "models": [
    "deepseek-r1:1.5b",
    "deepseek-r1:7b"
  ],
  "current_model": "deepseek-r1:1.5b"
}
```

---

## 6. BATCH PROCESSING

### Xử lý nhiều câu hỏi cùng lúc
```bash
curl -X POST http://localhost:8000/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "Xin chào",
      "Python là gì?",
      "2 + 2 bằng mấy?"
    ],
    "scenario": "default",
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "success": true,
  "total_messages": 3,
  "successful": 3,
  "failed": 0,
  "total_time": 5.67,
  "results": [
    {
      "index": 0,
      "message": "Xin chào",
      "response": "Xin chào! Tôi có thể...",
      "success": true
    },
    {
      "index": 1,
      "message": "Python là gì?",
      "response": "Python là ngôn ngữ...",
      "success": true
    },
    {
      "index": 2,
      "message": "2 + 2 bằng mấy?",
      "response": "2 + 2 = 4",
      "success": true
    }
  ]
}
```

---

## 7. CÁC VÍ DỤ THỰC TẾ

### 7.1. Bot hỗ trợ khách hàng
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Làm sao để đổi mật khẩu?",
    "scenario": "customer_support"
  }'
```

### 7.2. Trợ lý giảng dạy
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Giải thích vòng lặp for trong Python",
    "scenario": "teacher"
  }'
```

### 7.3. Tư vấn bán hàng
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tôi muốn mua laptop cho lập trình",
    "scenario": "sales"
  }'
```

### 7.4. Chuyên gia kỹ thuật
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Sự khác biệt giữa GET và POST?",
    "scenario": "technical"
  }'
```

### 7.5. Sáng tạo nội dung
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Viết một đoạn mở đầu blog về du lịch",
    "scenario": "creative",
    "temperature": 0.9
  }'
```

---

## 8. CUỘC HỘI THOẠI NHIỀU LƯỢT

```bash
# Lượt 1: Tạo session
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/session | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
echo "Session ID: $SESSION_ID"

# Lượt 2: Giới thiệu
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Tên tôi là Minh, tôi đang học Python\",
    \"session_id\": \"$SESSION_ID\",
    \"use_history\": true,
    \"scenario\": \"teacher\"
  }"

# Lượt 3: AI sẽ nhớ tên và ngữ cảnh
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Tôi nên bắt đầu học từ đâu?\",
    \"session_id\": \"$SESSION_ID\",
    \"use_history\": true,
    \"scenario\": \"teacher\"
  }"

# Lượt 4: Kiểm tra lịch sử
curl -X GET http://localhost:8000/api/session/$SESSION_ID
```

---

## 9. BASH SCRIPT TỰ ĐỘNG

### Tạo file `test_api.sh`:
```bash
#!/bin/bash

API_URL="http://localhost:8000"

echo "=== TESTING DEEPSEEK API ==="

# Test 1: Health Check
echo -e "\n1. Health Check..."
curl -s -X GET $API_URL/health | jq '.'

# Test 2: Scenarios
echo -e "\n2. List Scenarios..."
curl -s -X GET $API_URL/api/scenarios | jq '.scenarios | keys'

# Test 3: Simple Chat
echo -e "\n3. Simple Chat..."
curl -s -X POST $API_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' | jq '.response'

# Test 4: Batch
echo -e "\n4. Batch Processing..."
curl -s -X POST $API_URL/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["Hi", "2+2=?", "Bye"],
    "scenario": "default"
  }' | jq '.results[].response'

echo -e "\n=== TESTS COMPLETED ==="
```

**Chạy:**
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 10. PYTHON CLIENT

### Tạo file `api_client.py`:
```python
import requests

API_URL = "http://localhost:8000"

def chat(message, scenario="default", session_id=None, use_history=False):
    """Chat với API"""
    response = requests.post(
        f"{API_URL}/api/chat",
        json={
            "message": message,
            "scenario": scenario,
            "session_id": session_id,
            "use_history": use_history
        }
    )
    return response.json()

# Sử dụng
result = chat("Xin chào!", scenario="default")
print(result['response'])
```

---

## 11. POSTMAN COLLECTION

### Import vào Postman:
```json
{
  "info": {
    "name": "DeepSeek API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/health"
      }
    },
    {
      "name": "Chat",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/chat",
        "body": {
          "mode": "raw",
          "raw": "{\"message\": \"Hello\"}"
        },
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ]
      }
    }
  ]
}
```

---

## 12. ERROR HANDLING

### Lỗi: Message trống
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```
**Response:** `400 Bad Request`

### Lỗi: Session không tồn tại
```bash
curl -X GET http://localhost:8000/api/session/invalid_id
```
**Response:** `404 Not Found`

### Lỗi: Endpoint không tồn tại
```bash
curl -X GET http://localhost:8000/api/invalid
```
**Response:** `404 Not Found`

---

## 13. TIPS & TRICKS

### Lưu response vào file
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' > response.json
```

### Chỉ lấy response text
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' | jq -r '.response'
```

### Đo thời gian phản hồi
```bash
time curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Pretty print JSON
```bash
curl -s -X GET http://localhost:8000/api/scenarios | jq '.'
```

---

## 14. MONITORING & DEBUGGING

### Xem logs của API server
API server sẽ in logs ra console khi chạy `python api_server.py`

### Test với verbose mode
```bash
curl -v -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Kiểm tra headers
```bash
curl -I http://localhost:8000/health
```

---

## KẾT LUẬN

Bạn đã có đầy đủ các lệnh curl để test API! 🎉

**Bắt đầu:**
1. Chạy: `python api_server.py`
2. Test health: `curl http://localhost:8000/health`
3. Chat: `curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "Hello"}'`

**Tài liệu đầy đủ:** README.md
