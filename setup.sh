#!/bin/bash
# setup.sh - Script cài đặt tự động

echo "=================================================="
echo "🚀 SETUP DEEPSEEK AI - CUSTOM SCENARIOS"
echo "=================================================="
echo ""

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Hàm kiểm tra command
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Kiểm tra Python
echo "📋 Bước 1: Kiểm tra Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 chưa được cài đặt${NC}"
    echo "   Vui lòng cài Python 3.8 trở lên"
    exit 1
fi

# 2. Kiểm tra pip
echo ""
echo "📋 Bước 2: Kiểm tra pip..."
if command_exists pip3; then
    echo -e "${GREEN}✅ pip đã cài đặt${NC}"
else
    echo -e "${YELLOW}⚠️  pip chưa cài, đang cài đặt...${NC}"
    python3 -m ensurepip --upgrade
fi

# 3. Cài đặt dependencies Python
echo ""
echo "📋 Bước 3: Cài đặt Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Đã cài dependencies${NC}"
else
    echo -e "${RED}❌ Không tìm thấy requirements.txt${NC}"
    exit 1
fi

# 4. Kiểm tra Ollama
echo ""
echo "📋 Bước 4: Kiểm tra Ollama..."
if command_exists ollama; then
    OLLAMA_VERSION=$(ollama --version)
    echo -e "${GREEN}✅ Ollama đã cài: $OLLAMA_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama chưa được cài đặt${NC}"
    echo ""
    echo "Bạn có muốn cài Ollama không? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Đang cài Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        echo -e "${GREEN}✅ Đã cài Ollama${NC}"
    else
        echo -e "${YELLOW}⚠️  Vui lòng cài Ollama thủ công${NC}"
        echo "   curl -fsSL https://ollama.com/install.sh | sh"
    fi
fi

# 5. Kiểm tra Ollama đang chạy
echo ""
echo "📋 Bước 5: Kiểm tra Ollama service..."
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama đang chạy${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama chưa chạy${NC}"
    echo ""
    echo "Bạn có muốn khởi động Ollama không? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Đang khởi động Ollama..."
        ollama serve &
        sleep 3
        echo -e "${GREEN}✅ Ollama đã khởi động${NC}"
    else
        echo -e "${YELLOW}⚠️  Vui lòng chạy: ollama serve${NC}"
    fi
fi

# 6. Kiểm tra model DeepSeek
echo ""
echo "📋 Bước 6: Kiểm tra DeepSeek models..."
if ollama list | grep -q "deepseek"; then
    echo -e "${GREEN}✅ DeepSeek model đã được cài${NC}"
    ollama list | grep "deepseek"
else
    echo -e "${YELLOW}⚠️  Chưa có DeepSeek model${NC}"
    echo ""
    echo "Chọn model để tải:"
    echo "1) deepseek-r1:1.5b (Nhanh, 8GB RAM)"
    echo "2) deepseek-r1:7b (Thông minh, 16GB RAM)"
    echo "3) Bỏ qua"
    read -r choice
    
    case $choice in
        1)
            echo "Đang tải deepseek-r1:1.5b..."
            ollama pull deepseek-r1:1.5b
            echo -e "${GREEN}✅ Đã tải model 1.5b${NC}"
            ;;
        2)
            echo "Đang tải deepseek-r1:7b..."
            ollama pull deepseek-r1:7b
            echo -e "${GREEN}✅ Đã tải model 7b${NC}"
            ;;
        3)
            echo -e "${YELLOW}⚠️  Vui lòng tải model thủ công:${NC}"
            echo "   ollama pull deepseek-r1:1.5b"
            ;;
    esac
fi

# 7. Test hệ thống
echo ""
echo "📋 Bước 7: Test hệ thống..."
echo "Bạn có muốn chạy test không? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python3 test.py
fi

# Kết thúc
echo ""
echo "=================================================="
echo "🎉 CÀI ĐẶT HOÀN TẤT!"
echo "=================================================="
echo ""
echo "📝 Các bước tiếp theo:"
echo ""
echo "1️⃣  Chạy CLI:"
echo "   python3 cli.py"
echo ""
echo "2️⃣  Chạy Web Interface:"
echo "   python3 app.py"
echo "   Sau đó mở: http://localhost:5000"
echo ""
echo "3️⃣  Tùy chỉnh kịch bản:"
echo "   Chỉnh sửa file config.py"
echo ""
echo "📖 Đọc README.md để biết thêm chi tiết"
echo "=================================================="
