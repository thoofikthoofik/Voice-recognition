from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import sys
import threading
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'voice_command_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class VoiceCommandSystem:
    def __init__(self):
        self.is_listening = False
        self.current_session = None
        self.current_dir = os.getcwd()
        # Use enhanced speech recognition for better accuracy
        self.python_cmd = f'python "{self.current_dir}\\enhanced_speech.py"'
        self.fallback_cmd = f'python "{self.current_dir}\\1.py"'
    
    def execute_command(self, cmd):
        """Execute voice command and return result"""
        cmd = cmd.lower().strip()
        
        # System information commands
        if "system info" in cmd or "about" in cmd:
            result = subprocess.run("systeminfo", shell=True, capture_output=True, text=True)
            return {"type": "system", "output": result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout}
        
        elif "list" in cmd or "files" in cmd:
            result = subprocess.run("dir", shell=True, capture_output=True, text=True)
            return {"type": "files", "output": result.stdout}
        
        elif "date" in cmd or "time" in cmd:
            result = subprocess.run("date /t && time /t", shell=True, capture_output=True, text=True)
            return {"type": "datetime", "output": result.stdout}
        
        elif "ip" in cmd or "network" in cmd:
            result = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True)
            return {"type": "network", "output": result.stdout[:1500] + "..." if len(result.stdout) > 1500 else result.stdout}
        
        elif "memory" in cmd or "ram" in cmd:
            result = subprocess.run('systeminfo | findstr "Memory"', shell=True, capture_output=True, text=True)
            return {"type": "memory", "output": result.stdout}
        
        elif "cpu" in cmd or "processor" in cmd:
            result = subprocess.run("wmic cpu get name, numberofcores, maxclockspeed", shell=True, capture_output=True, text=True)
            return {"type": "cpu", "output": result.stdout}
        
        elif "disk" in cmd or "drive" in cmd:
            result = subprocess.run("wmic logicaldisk get size,freespace,caption", shell=True, capture_output=True, text=True)
            return {"type": "disk", "output": result.stdout}
        
        elif "processes" in cmd or "tasks" in cmd:
            result = subprocess.run("tasklist", shell=True, capture_output=True, text=True)
            return {"type": "processes", "output": result.stdout[:2000] + "..." if len(result.stdout) > 2000 else result.stdout}
        
        elif "open browser" in cmd:
            subprocess.run("start https://www.google.com", shell=True)
            return {"type": "action", "output": "Opening browser..."}
        
        elif "open notepad" in cmd:
            subprocess.run("start notepad", shell=True)
            return {"type": "action", "output": "Opening Notepad..."}
        
        elif "open calculator" in cmd:
            subprocess.run("calc", shell=True)
            return {"type": "action", "output": "Opening Calculator..."}
        
        elif "clear" in cmd or "cls" in cmd:
            return {"type": "action", "output": "Screen cleared", "clear": True}
        
        elif "volume up" in cmd:
            subprocess.run('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"', shell=True)
            return {"type": "action", "output": "Volume increased"}
        
        elif "volume down" in cmd:
            subprocess.run('powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"', shell=True)
            return {"type": "action", "output": "Volume decreased"}
        
        elif "search" in cmd:
            search_term = cmd.replace("search", "").strip()
            if search_term:
                if "song" in cmd or "music" in cmd:
                    search_term = search_term.replace("song", "").replace("music", "").strip()
                    url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                    subprocess.run(f"start {url}", shell=True)
                    return {"type": "search", "output": f"Searching for song: {search_term}"}
                elif "movie" in cmd or "film" in cmd:
                    search_term = search_term.replace("movie", "").replace("film", "").strip()
                    url = f"https://www.imdb.com/find?q={search_term.replace(' ', '+')}"
                    subprocess.run(f"start {url}", shell=True)
                    return {"type": "search", "output": f"Searching for movie: {search_term}"}
                else:
                    url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                    subprocess.run(f"start {url}", shell=True)
                    return {"type": "search", "output": f"Searching for: {search_term}"}
            else:
                return {"type": "help", "output": "Please specify what you want to search for"}
        
        elif "help" in cmd or "commands" in cmd:
            help_text = """Available commands:
• System: system info, memory, cpu, disk, processes
• Files: list files
• Time: date, time
• Network: ip, network
• Apps: open browser, open notepad, open calculator
• Control: clear, volume up, volume down
• Search: search [query], search [song name] song, search [movie name] movie"""
            return {"type": "help", "output": help_text}
        
        else:
            return {"type": "error", "output": f"Command not recognized: {cmd}"}

voice_system = VoiceCommandSystem()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_listening')
def handle_start_listening():
    """Start listening for voice commands"""
    if not voice_system.is_listening:
        voice_system.is_listening = True
        voice_system.current_session = request.sid
        emit('status_update', {'status': 'adjusting', 'message': 'Starting speech recognition...'})
        
        def listen_loop():
            while voice_system.is_listening:
                try:
                    socketio.emit('status_update', {'status': 'listening', 'message': '🎤 Listening... Speak clearly!'}, 
                                room=voice_system.current_session)
                    
                    # Try enhanced speech recognition first
                    result = None
                    try:
                        result = subprocess.run(voice_system.python_cmd, shell=True, capture_output=True, text=True, timeout=90)
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        # Fallback to basic recognition if enhanced fails
                        socketio.emit('status_update', {'status': 'processing', 'message': '🔄 Trying fallback recognition...'}, 
                                    room=voice_system.current_session)
                        result = subprocess.run(voice_system.fallback_cmd, shell=True, capture_output=True, text=True, timeout=60)
                    
                    if result and result.returncode == 0 and result.stdout.strip():
                        recognized_text = result.stdout.strip().lower()
                        
                        # Handle special recognition results
                        if recognized_text in ["unknown", "error", "timeout", "microphone_error", "critical_error"]:
                            if recognized_text == "unknown":
                                socketio.emit('status_update', {'status': 'error', 'message': '❓ Could not understand speech - please try again'}, 
                                            room=voice_system.current_session)
                            elif recognized_text == "timeout":
                                socketio.emit('status_update', {'status': 'error', 'message': '⏱️ No speech detected - please try again'}, 
                                            room=voice_system.current_session)
                            elif recognized_text in ["microphone_error", "critical_error"]:
                                socketio.emit('status_update', {'status': 'error', 'message': '🎤 Microphone error - check your audio settings'}, 
                                            room=voice_system.current_session)
                            else:
                                socketio.emit('status_update', {'status': 'error', 'message': f'⚠️ Recognition issue: {recognized_text}'}, 
                                            room=voice_system.current_session)
                            continue
                        
                        # Extract confidence score if present in stderr
                        confidence = None
                        if result.stderr:
                            confidence_match = None
                            for line in result.stderr.split('\n'):
                                if 'confidence' in line.lower():
                                    import re
                                    match = re.search(r'confidence[:\s]+(\d+\.?\d*)', line, re.IGNORECASE)
                                    if match:
                                        confidence = float(match.group(1))
                                        break
                        
                        socketio.emit('command_recognized', {
                            'command': recognized_text,
                            'confidence': confidence
                        }, room=voice_system.current_session)
                        
                        if recognized_text == "exit" or "stop listening" in recognized_text:
                            voice_system.is_listening = False
                            socketio.emit('status_update', {'status': 'stopped', 'message': '🛑 Stopped listening'}, 
                                        room=voice_system.current_session)
                            break
                        
                        socketio.emit('status_update', {'status': 'processing', 'message': '⚡ Processing command...'}, 
                                    room=voice_system.current_session)
                        command_result = voice_system.execute_command(recognized_text)
                        socketio.emit('command_result', command_result, room=voice_system.current_session)
                        
                        # Add longer pause after successful command to prevent duplicates
                        socketio.emit('status_update', {'status': 'idle', 'message': '✅ Command completed. Ready for next command...'}, 
                                    room=voice_system.current_session)
                        time.sleep(2)  # 2-second pause after successful command
                        
                    else:
                        socketio.emit('status_update', {'status': 'error', 'message': '🔇 No speech detected - please try again'}, 
                                    room=voice_system.current_session)
                        time.sleep(1)  # Brief pause for errors
                    
                except subprocess.TimeoutExpired:
                    socketio.emit('status_update', {'status': 'error', 'message': 'Speech recognition timed out'}, 
                                room=voice_system.current_session)
                    continue
                except Exception as e:
                    socketio.emit('status_update', {'status': 'error', 'message': f'Error: {str(e)}'}, 
                                room=voice_system.current_session)
                    voice_system.is_listening = False
                    break
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=listen_loop)
        listen_thread.daemon = True
        listen_thread.start()

@socketio.on('stop_listening')
def handle_stop_listening():
    """Stop listening for voice commands"""
    voice_system.is_listening = False
    emit('status_update', {'status': 'stopped', 'message': 'Stopped listening'})

@socketio.on('execute_command')
def handle_execute_command(data):
    """Execute a text command"""
    command = data['command']
    result = voice_system.execute_command(command)
    emit('command_result', result)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 