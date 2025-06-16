# 🎤 Voice Command System

A modern web-based voice command system with a beautiful user interface that allows you to control your computer using voice commands.

## 🚀 Features

- **🎯 Voice Recognition**: Real-time speech-to-text using Google's speech recognition
- **🌐 Web Interface**: Modern, responsive web UI with live updates
- **⚡ Real-time Communication**: WebSocket-based instant feedback
- **📱 Cross-platform**: Works on Windows, with responsive design for mobile
- **🎨 Beautiful UI**: Animated buttons, gradients, and visual feedback
- **📝 Dual Input**: Voice commands + manual text input

## 🛠️ Installation

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:5000`

## 🎮 Usage

### Voice Commands
1. Click the **microphone button** (large circular button)
2. Wait for "Listening..." status
3. Speak your command clearly
4. See results in the output panel

### Text Commands
1. Type your command in the text input field
2. Press **Enter** or click the **Send** button
3. See results instantly

## 📋 Available Commands

### 🖥️ System Information
- `system info` / `about` - System information
- `memory` / `ram` - Memory usage
- `cpu` / `processor` - CPU information
- `disk` / `drive` - Disk usage
- `processes` / `tasks` - Running processes

### 📁 File Operations
- `list files` - List directory contents
- `date` / `time` - Current date and time

### 🌐 Network
- `ip` / `network` - Network configuration
- `ping google` - Test internet connectivity

### 🚀 Applications
- `open browser` - Open web browser
- `open notepad` - Open Notepad
- `open calculator` - Open Calculator

### 🔍 Search & Media
- `search [query]` - Google search
- `search [song name] song` - YouTube music search
- `search [movie name] movie` - IMDb movie search

### ⚙️ System Control
- `volume up` - Increase system volume
- `volume down` - Decrease system volume
- `clear` / `cls` - Clear output screen
- `help` / `commands` - Show available commands

## 📁 File Structure

```
voice-command-system/
├── app.py              # Flask web application
├── 1.py                # Speech recognition script
├── templates/
│   └── index.html      # Web interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

- **Backend**: Flask + SocketIO for real-time communication
- **Frontend**: HTML5, CSS3, JavaScript with Font Awesome icons
- **Speech Recognition**: Google Speech Recognition API
- **Threading**: Proper async handling for voice processing
- **WebSockets**: Real-time status updates and command results

## 🎨 UI Features

- **Animated Microphone Button**: Visual feedback for listening states
- **Status Indicators**: Real-time status updates (listening, processing, idle)
- **Command History**: Scrollable output with command results
- **Responsive Design**: Works on desktop and mobile devices
- **Modern Styling**: Gradients, animations, and smooth transitions

## 🐛 Troubleshooting

### Common Issues:
1. **Microphone not working**: Check browser permissions for microphone access
2. **Commands not recognized**: Speak clearly and ensure good microphone quality
3. **Flask not starting**: Ensure port 5000 is available
4. **Speech recognition errors**: Check internet connection (uses Google API)

### Voice Recognition Tips:
- Speak clearly and at normal pace
- Ensure minimal background noise
- Allow browser microphone permissions
- Wait for "Listening..." status before speaking

## 🔒 Security Notes

- This is a development server - not for production use
- Voice commands execute system commands - use with caution
- Runs on local network only (0.0.0.0:5000)

## ✅ Recent Improvements (v2.0)

### 🎯 Enhanced Voice Accuracy
- **Single Command Processing**: Fixed issue where one command triggered multiple times
- **Smart Recognition**: Uses enhanced engine with fallback to basic recognition
- **Confidence Scoring**: Real-time accuracy indicators (80%+ = green, 50-79% = orange, <50% = red)
- **Command Spacing**: 2-second pause between commands with visual countdown
- **Multiple Language Testing**: Tests 5 English variants for best results

### 🔧 Technical Fixes
- **Duplicate Prevention**: Ensures only one result per speech input
- **Improved Timing**: Proper delays between command processing
- **Better Error Handling**: Clear feedback for recognition issues
- **Visual Feedback**: Command completion countdown and accuracy indicators

## 🎯 Future Enhancements

- [ ] Offline speech recognition
- [ ] Custom command creation
- [ ] Voice response system
- [ ] Command scheduling
- [ ] Multi-language support

## 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Made with ❤️ using Flask, SocketIO, and modern web technologies** 