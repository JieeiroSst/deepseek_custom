#!/bin/bash
# test_curl.sh - Script test API với curl

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

echo -e "${BLUE}"
echo "=========================================="
echo "  DEEPSEEK API - CURL TEST SUITE"
echo "=========================================="
echo -e "${NC}"

# Hàm test
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -e "\n${YELLOW}Testing: $name${NC}"
    echo "Endpoint: $method $endpoint"
    
    if [ -z "$data" ]; then
        response=$(curl -s -X $method "$API_URL$endpoint")
    else
        response=$(curl -s -X $method "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    # Kiểm tra response
    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        success=$(echo "$response" | jq -r '.success')
        if [ "$success" = "true" ]; then
            echo -e "${GREEN}✅ PASSED${NC}"
        else
            echo -e "${RED}❌ FAILED${NC}"
            echo "Error: $(echo "$response" | jq -r '.error')"
        fi
    else
        echo -e "${GREEN}✅ Response received${NC}"
    fi
    
    # Hiển thị response (giới hạn 200 ký tự)
    echo "Response preview:"
    echo "$response" | jq '.' 2>/dev/null | head -c 200
    echo "..."
}

# Kiểm tra jq có cài không
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq chưa cài đặt. Đang cài...${NC}"
    # Linux
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y jq
    # Mac
    elif command -v brew &> /dev/null; then
        brew install jq
    else
        echo "Vui lòng cài jq thủ công: https://stedolan.github.io/jq/"
        exit 1
    fi
fi

# Kiểm tra server có chạy không
echo -e "\n${BLUE}Checking if API server is running...${NC}"
if ! curl -s "$API_URL/health" > /dev/null 2>&1; then
    echo -e "${RED}❌ API server không chạy!${NC}"
    echo -e "${YELLOW}Vui lòng chạy: python api_server.py${NC}"
    exit 1
fi
echo -e "${GREEN}✅ API server is running${NC}"

# ============================================================================
# RUN TESTS
# ============================================================================

echo -e "\n${BLUE}=== BASIC TESTS ===${NC}"

# Test 1: Health Check
test_endpoint "Health Check" \
    "GET" \
    "/health"

# Test 2: List Scenarios
test_endpoint "List Scenarios" \
    "GET" \
    "/api/scenarios"

# Test 3: Get Scenario Detail
test_endpoint "Get Scenario Detail" \
    "GET" \
    "/api/scenarios/teacher"

echo -e "\n${BLUE}=== CHAT TESTS ===${NC}"

# Test 4: Simple Chat
test_endpoint "Simple Chat" \
    "POST" \
    "/api/chat" \
    '{"message": "Xin chào!"}'

# Test 5: Chat with Scenario
test_endpoint "Chat with Customer Support Scenario" \
    "POST" \
    "/api/chat" \
    '{"message": "Tôi quên mật khẩu", "scenario": "customer_support"}'

# Test 6: Chat with Temperature
test_endpoint "Chat with High Temperature" \
    "POST" \
    "/api/chat" \
    '{"message": "Viết một câu về bầu trời", "scenario": "creative", "temperature": 0.9}'

echo -e "\n${BLUE}=== SESSION TESTS ===${NC}"

# Test 7: Create Session
echo -e "\n${YELLOW}Testing: Create Session${NC}"
session_response=$(curl -s -X POST "$API_URL/api/session")
SESSION_ID=$(echo "$session_response" | jq -r '.session_id')
echo "Session ID: $SESSION_ID"
if [ ! -z "$SESSION_ID" ] && [ "$SESSION_ID" != "null" ]; then
    echo -e "${GREEN}✅ PASSED${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

# Test 8: Chat with History
if [ ! -z "$SESSION_ID" ] && [ "$SESSION_ID" != "null" ]; then
    test_endpoint "Chat with History - Message 1" \
        "POST" \
        "/api/chat" \
        "{\"message\": \"Tên tôi là Minh\", \"session_id\": \"$SESSION_ID\", \"use_history\": true}"
    
    test_endpoint "Chat with History - Message 2" \
        "POST" \
        "/api/chat" \
        "{\"message\": \"Tên tôi là gì?\", \"session_id\": \"$SESSION_ID\", \"use_history\": true}"
    
    # Test 9: Get Session Info
    test_endpoint "Get Session Info" \
        "GET" \
        "/api/session/$SESSION_ID"
    
    # Test 10: Clear History
    test_endpoint "Clear Session History" \
        "DELETE" \
        "/api/session/$SESSION_ID/history"
    
    # Test 11: Delete Session
    test_endpoint "Delete Session" \
        "DELETE" \
        "/api/session/$SESSION_ID"
fi

echo -e "\n${BLUE}=== ADVANCED TESTS ===${NC}"

# Test 12: List Models
test_endpoint "List Models" \
    "GET" \
    "/api/models"

# Test 13: Batch Processing
test_endpoint "Batch Processing" \
    "POST" \
    "/api/batch" \
    '{"messages": ["Xin chào", "2+2=?", "Python là gì?"], "scenario": "default"}'

echo -e "\n${BLUE}=== ERROR HANDLING TESTS ===${NC}"

# Test 14: Empty Message
test_endpoint "Empty Message (should fail)" \
    "POST" \
    "/api/chat" \
    '{"message": ""}'

# Test 15: Invalid Session
test_endpoint "Invalid Session (should fail)" \
    "GET" \
    "/api/session/invalid_session_id"

# Test 16: Invalid Endpoint
test_endpoint "Invalid Endpoint (should fail)" \
    "GET" \
    "/api/invalid_endpoint"

# ============================================================================
# SUMMARY
# ============================================================================

echo -e "\n${BLUE}"
echo "=========================================="
echo "  TEST SUITE COMPLETED"
echo "=========================================="
echo -e "${NC}"

echo -e "\n${GREEN}✅ All tests executed${NC}"
echo -e "\n${YELLOW}Để xem chi tiết từng test, hãy chạy curl thủ công:${NC}"
echo "  curl -X GET $API_URL/health"
echo "  curl -X POST $API_URL/api/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello\"}'"
echo -e "\n${BLUE}Đọc CURL_API_GUIDE.md để biết thêm chi tiết${NC}\n"
