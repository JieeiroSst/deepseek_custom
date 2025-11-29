# api_server.py
# REST API Server cho DeepSeek AI

from flask import Flask, request, jsonify
from flask_cors import CORS
from deepseek_client import DeepSeekClient, ScenarioManager
import secrets
import time

app = Flask(__name__)
CORS(app)  # Cho phép CORS

# Lưu trữ sessions
sessions = {}

def get_or_create_session(session_id=None):
    """Lấy hoặc tạo session mới"""
    if not session_id:
        session_id = secrets.token_hex(16)
    
    if session_id not in sessions:
        sessions[session_id] = {
            'client': DeepSeekClient(),
            'created_at': time.time(),
            'last_active': time.time()
        }
    
    sessions[session_id]['last_active'] = time.time()
    return session_id, sessions[session_id]['client']


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái API"""
    client = DeepSeekClient()
    connected = client.check_connection()
    
    return jsonify({
        'status': 'healthy' if connected else 'unhealthy',
        'timestamp': time.time(),
        'ollama_connected': connected,
        'active_sessions': len(sessions)
    })


# ============================================================================
# SCENARIOS
# ============================================================================

@app.route('/api/scenarios', methods=['GET'])
def list_scenarios():
    """Lấy danh sách tất cả kịch bản"""
    scenarios = ScenarioManager.list_scenarios()
    
    return jsonify({
        'success': True,
        'count': len(scenarios),
        'scenarios': scenarios
    })


@app.route('/api/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Lấy chi tiết một kịch bản"""
    scenario = ScenarioManager.get_scenario(scenario_id)
    
    if scenario:
        return jsonify({
            'success': True,
            'scenario_id': scenario_id,
            'scenario': scenario
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Scenario not found'
        }), 404


# ============================================================================
# CHAT
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat với AI
    
    Body:
    {
        "message": "Câu hỏi của bạn",
        "scenario": "default",  # optional
        "session_id": "xxx",    # optional
        "use_history": false,   # optional
        "temperature": 0.7      # optional
    }
    """
    try:
        data = request.json
        
        # Validate
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: message'
            }), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Lấy parameters
        scenario = data.get('scenario', 'default')
        session_id = data.get('session_id')
        use_history = data.get('use_history', False)
        temperature = data.get('temperature')
        
        # Lấy hoặc tạo session
        session_id, client = get_or_create_session(session_id)
        
        # Chat với AI
        start_time = time.time()
        response = client.chat(
            user_message=message,
            scenario=scenario,
            use_history=use_history,
            temperature=temperature
        )
        elapsed_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'response': response,
            'scenario': scenario,
            'elapsed_time': round(elapsed_time, 2),
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """
    Chat với streaming response
    
    Body tương tự /api/chat
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: message'
            }), 400
        
        message = data['message'].strip()
        scenario = data.get('scenario', 'default')
        temperature = data.get('temperature')
        
        client = DeepSeekClient()
        
        def generate():
            for chunk in client.chat_stream(message, scenario, temperature):
                yield f"data: {chunk}\n\n"
        
        return app.response_class(
            generate(),
            mimetype='text/event-stream'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

@app.route('/api/session', methods=['POST'])
def create_session():
    """Tạo session mới"""
    session_id = secrets.token_hex(16)
    sessions[session_id] = {
        'client': DeepSeekClient(),
        'created_at': time.time(),
        'last_active': time.time()
    }
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'created_at': sessions[session_id]['created_at']
    })


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Lấy thông tin session"""
    if session_id not in sessions:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    session = sessions[session_id]
    history = session['client'].get_history()
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'created_at': session['created_at'],
        'last_active': session['last_active'],
        'message_count': len(history),
        'history': history
    })


@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Xóa session"""
    if session_id in sessions:
        del sessions[session_id]
        return jsonify({
            'success': True,
            'message': 'Session deleted'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404


@app.route('/api/session/<session_id>/history', methods=['DELETE'])
def clear_session_history(session_id):
    """Xóa lịch sử chat của session"""
    if session_id not in sessions:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    sessions[session_id]['client'].clear_history()
    
    return jsonify({
        'success': True,
        'message': 'History cleared'
    })


# ============================================================================
# MODELS
# ============================================================================

@app.route('/api/models', methods=['GET'])
def list_models():
    """Lấy danh sách models đã cài"""
    client = DeepSeekClient()
    models = client.list_models()
    
    return jsonify({
        'success': True,
        'count': len(models),
        'models': models,
        'current_model': client.model_name
    })


# ============================================================================
# BATCH PROCESSING
# ============================================================================

@app.route('/api/batch', methods=['POST'])
def batch_process():
    """
    Xử lý nhiều câu hỏi cùng lúc
    
    Body:
    {
        "messages": ["câu 1", "câu 2", "câu 3"],
        "scenario": "default",
        "temperature": 0.7
    }
    """
    try:
        data = request.json
        
        if not data or 'messages' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: messages'
            }), 400
        
        messages = data['messages']
        if not isinstance(messages, list) or len(messages) == 0:
            return jsonify({
                'success': False,
                'error': 'messages must be a non-empty array'
            }), 400
        
        scenario = data.get('scenario', 'default')
        temperature = data.get('temperature')
        
        client = DeepSeekClient()
        results = []
        
        start_time = time.time()
        
        for i, message in enumerate(messages):
            try:
                response = client.chat(
                    user_message=message,
                    scenario=scenario,
                    temperature=temperature
                )
                results.append({
                    'index': i,
                    'message': message,
                    'response': response,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'message': message,
                    'error': str(e),
                    'success': False
                })
        
        total_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'total_messages': len(messages),
            'successful': len([r for r in results if r['success']]),
            'failed': len([r for r in results if not r['success']]),
            'total_time': round(total_time, 2),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 DEEPSEEK AI - REST API SERVER")
    print("="*70)
    print("\n📝 API đang chạy tại: http://localhost:8000")
    print("\n📖 Endpoints:")
    print("   GET  /health                      - Health check")
    print("   GET  /api/scenarios               - Danh sách kịch bản")
    print("   GET  /api/scenarios/<id>          - Chi tiết kịch bản")
    print("   POST /api/chat                    - Chat với AI")
    print("   POST /api/chat/stream             - Chat streaming")
    print("   POST /api/session                 - Tạo session mới")
    print("   GET  /api/session/<id>            - Thông tin session")
    print("   DELETE /api/session/<id>          - Xóa session")
    print("   DELETE /api/session/<id>/history  - Xóa lịch sử")
    print("   GET  /api/models                  - Danh sách models")
    print("   POST /api/batch                   - Batch processing")
    print("\n⚠️  Đảm bảo Ollama đang chạy: ollama serve")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
