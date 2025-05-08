# 🗣️ VocalizeIt

> 🔊 Convert your text to speech with style and flexibility!

## ✨ Features

- 🖥️ **User-friendly Terminal Interface**: Navigate easily through a clear menu system
- 🔤 **Multiple Text Input Methods**: Type directly or import from files
- 🎭 **Voice Selection**: Choose from all available system voices
- 🎛️ **Customizable Speech**: Adjust rate and volume to your preference
- 💾 **Multiple Export Formats**: Save as WAV (offline) or MP3 (using Google TTS)
- 🌐 **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites

- 🐍 Python 3.6 or higher

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/qusai-Kagalwala/vocalize-it.git
   cd vocalize-it
   ```

2. Install the required dependencies:
   ```bash
   pip install pyttsx3
   pip install gtts  # Optional - for MP3 export functionality
   ```

## 🎮 Usage

Run the tool with:
```bash
python vocalize_it.py
```

### Main Menu Navigation:
- **1️⃣ Enter/Load Text**: Input text or load from a file
- **2️⃣ Select Voice**: Choose from available system voices
- **3️⃣ Speak Current Text**: Listen to the current text with selected settings
- **4️⃣ Save to File**: Export speech as WAV or MP3
- **5️⃣ Adjust Settings**: Modify speech rate and volume
- **6️⃣ Exit**: Close the application

## 📋 Example

```python
# Direct usage in your Python code:
from vocalize_it import EnhancedTTS

tts = EnhancedTTS()
tts.speak("Hello world! This is VocalizeIt in action.")

# Save to a file
tts.save_to_file("This text will be saved as audio.", "output.wav")
```

## 🛠️ Customization

### Speech Parameters

Adjust these parameters to customize the voice output:
- **Rate**: Speed of speech (words per minute) - Range: 50-300
- **Volume**: Loudness level - Range: 0.0-1.0

### Supported File Formats

- **WAV**: Using local pyttsx3 engine (offline)
- **MP3**: Using Google's Text-to-Speech service (requires internet)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest enhancements
- Submit pull requests

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📚 Dependencies

- [pyttsx3](https://pypi.org/project/pyttsx3/): Offline text-to-speech conversion
- [gTTS](https://pypi.org/project/gTTS/) (optional): Google Text-to-Speech for MP3 export

---

💡 **Tip**: On different operating systems, you might need additional dependencies:
- **Windows**: No additional requirements
- **macOS**: `pip install pyobjc`
- **Linux**: `sudo apt-get install espeak`

---

Made with ❤️ by [Qusai Kagalwala](https://github.com/qusai-Kagalwala)
