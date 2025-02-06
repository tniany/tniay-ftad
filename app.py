from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO, emit
import pyperclip
import json
from datetime import datetime
import os
try:
    import requests # type: ignore
except ImportError:
    print("请安装 requests: pip install requests")
    requests = None

try:
    from PIL import Image # type: ignore
except ImportError:
    print("请安装 Pillow: pip install Pillow")
    Image = None

import base64
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大限制
socketio = SocketIO(app, async_mode='threading')

# 添加文件图标过滤器
@app.template_filter('get_file_icon')
def get_file_icon(filename):
    """获取文件类型对应的图标"""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    icons = {
        # 文档
        'txt': '📝',
        'pdf': '📄',
        'doc': '📃',
        'docx': '📃',
        'xls': '📊',
        'xlsx': '📊',
        'ppt': '📺',
        'pptx': '📺',
        # 图片
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'gif': '🖼️',
        'bmp': '🖼️',
        'webp': '🖼️',
        # 音频
        'mp3': '🎵',
        'wav': '🎵',
        'ogg': '🎵',
        'flac': '🎵',
        'm4a': '🎵',
        # 视频
        'mp4': '🎥',
        'avi': '🎥',
        'mkv': '🎥',
        'mov': '🎥',
        'wmv': '🎥',
        # 压缩包
        'zip': '📦',
        'rar': '📦',
        '7z': '📦',
        'tar': '📦',
        'gz': '📦'
    }
    return icons.get(ext, '📄')  # 默认文件图标

# 设置上传文件夹路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 扩展允许的文件类型
ALLOWED_EXTENSIONS = {
    # 文档
    'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    # 图片
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp',
    # 音频
    'mp3', 'wav', 'ogg', 'flac', 'm4a',
    # 视频
    'mp4', 'avi', 'mkv', 'mov', 'wmv',
    # 压缩包
    'zip', 'rar', '7z', 'tar', 'gz'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 消息历史文件路径
MESSAGES_FILE = 'messages.json'

def call_ai_api(text):
    """调用AI API"""
    if not requests:
        return "请先安装 requests 模块"
    
    url = "https://apiserver.alcex.cn/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": text}],
        "stream": False
    }
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"AI API调用失败: {e}")
        return "AI思考失败，请稍后重试"

def load_messages():
    """从JSON文件加载消息历史"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_message(message_data):
    """保存消息到JSON文件"""
    messages = load_messages()
    messages.append(message_data)
    messages = messages[-100:]  # 只保留最近的100条消息
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    messages = load_messages()
    return render_template('index.html', messages=messages)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_name, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                filename = f"{base_name}_{counter}{extension}"
                counter += 1
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 确定文件类型
            ext = filename.lower().split('.')[-1]
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']:
                file_type = 'image'
                # 处理图片...（保持原有的图片处理代码）
            elif ext in ['mp3', 'wav', 'ogg', 'flac', 'm4a']:
                file_type = 'audio'
                img_str = None
            elif ext in ['mp4', 'avi', 'mkv', 'mov', 'wmv']:
                file_type = 'video'
                img_str = None
            else:
                file_type = 'file'
                img_str = None
            
            message_data = {
                'id': str(datetime.now().timestamp()),
                'type': file_type,
                'filename': filename,
                'path': file_path,
                'image_data': img_str if file_type == 'image' else None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            save_message(message_data)
            socketio.emit('receive_file', message_data)
            return jsonify({'success': True, 'message': '文件上传成功'})
        
        return jsonify({'error': '不支持的文件类型'}), 400
    
    except Exception as e:
        print(f"上传失败: {e}")
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                    as_attachment=True)

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    auto_copy = data['autoCopy']
    
    message_data = {
        'id': str(datetime.now().timestamp()),
        'type': 'text',
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'shouldAutoCopy': auto_copy
    }
    
    save_message(message_data)
    emit('receive_message', message_data, broadcast=True)

@socketio.on('delete_message')
def handle_delete_message(data):
    """处理删除单条消息"""
    try:
        message_id = data.get('messageId')
        messages = load_messages()
        messages = [msg for msg in messages if str(msg.get('id')) != str(message_id)]
        
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        # 广播删除消息的事件
        emit('message_deleted', {'messageId': message_id}, broadcast=True)
    except Exception as e:
        print(f"删除消息失败: {e}")

@socketio.on('think_about_message')
def handle_think_request(data):
    text = data['text']
    ai_response = call_ai_api(text)
    
    message_data = {
        'id': str(datetime.now().timestamp()),
        'type': 'ai_response',
        'message': ai_response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'isAiResponse': True,
        'originalText': text
    }
    
    save_message(message_data)
    emit('receive_ai_response', message_data, broadcast=True)

@socketio.on('clear_messages')
def handle_clear_messages():
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        emit('messages_cleared', broadcast=True)
    except Exception as e:
        print(f"清除消息失败: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True) 