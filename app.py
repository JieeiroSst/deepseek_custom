# app.py
# Flask web application cho DeepSeek Custom AI

from flask import Flask, render_template, request, jsonify, session
from deepseek_client import DeepSeekClient, ScenarioManager
from config import SCENARIOS
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Lưu client cho mỗi session
clients = {}

def get_client(session_id):
    """Lấy hoặc tạo client cho session"""
    if session_id not in clients:
        clients[session_id] = DeepSeekClient()
    return clients[session_id]

@app.route('/')
def index():
    """Trang chủ"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
    return render_template('index.html')

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """API lấy danh sách kịch bản"""
    scenarios = ScenarioManager.list_scenarios()
    return jsonify({
        'success': True,
        'scenarios': scenarios
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """API chat với AI"""
    try:
        data = request.json
        session_id = session.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Không tìm thấy session'
            }), 400
        
        client = get_client(session_id)
        
        message = data.get('message', '').strip()
        scenario = data.get('scenario', 'default')
        use_history = data.get('use_history', False)
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Tin nhắn không được để trống'
            }), 400
        
        # Gọi AI
        response = client.chat(
            message,
            scenario=scenario,
            use_history=use_history
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'scenario': scenario
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """API lấy lịch sử chat"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'error': 'No session'}), 400
    
    client = get_client(session_id)
    history = client.get_history()
    
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """API xóa lịch sử chat"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'error': 'No session'}), 400
    
    client = get_client(session_id)
    client.clear_history()
    
    return jsonify({
        'success': True,
        'message': 'Đã xóa lịch sử'
    })

@app.route('/api/status', methods=['GET'])
def check_status():
    """Kiểm tra trạng thái kết nối"""
    client = DeepSeekClient()
    connected = client.check_connection()
    models = client.list_models() if connected else []
    
    return jsonify({
        'success': True,
        'connected': connected,
        'models': models
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DEEPSEEK AI WEB INTERFACE")
    print("="*60)
    print("\n📝 Mở trình duyệt và truy cập: http://localhost:5000")
    print("\n⚠️  Đảm bảo Ollama đang chạy: ollama serve")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
