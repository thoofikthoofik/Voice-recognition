import speech_recognition as sr
import sys

def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Enhanced recognition settings for better accuracy
    recognizer.energy_threshold = 400  # Higher threshold to ignore background noise
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.1  # More aggressive noise adaptation
    recognizer.dynamic_energy_ratio = 1.5  # Better signal-to-noise ratio
    recognizer.pause_threshold = 1.0  # Wait longer for complete phrases
    recognizer.phrase_threshold = 0.2  # Start listening sooner
    recognizer.non_speaking_duration = 0.8  # Longer pause detection
    
    try:
        # Use microphone with better audio quality settings
        with sr.Microphone(sample_rate=44100, chunk_size=1024) as source:
            print("Adjusting for ambient noise...", file=sys.stderr)
            # Extended ambient noise adjustment for better accuracy
            recognizer.adjust_for_ambient_noise(source, duration=4)
            print("Ready! Listening... (Speak clearly and close to microphone)", file=sys.stderr)
            
            try:
                # Single attempt for cleaner, simpler recognition
                print("Listening for command...", file=sys.stderr)
                
                # Listen for audio input with optimized settings
                audio = recognizer.listen(source, timeout=30, phrase_time_limit=12)
                print("Processing speech...", file=sys.stderr)
                
                # Try primary recognition first
                try:
                    text = recognizer.recognize_google(audio, language='en-US', show_all=False)
                    if text and len(text.strip()) > 0:
                        print(f"Recognized: {text}", file=sys.stderr)
                        return text.lower().strip()
                except (sr.UnknownValueError, sr.RequestError):
                    pass
                
                # If primary fails, try with confidence scores
                try:
                    result = recognizer.recognize_google(audio, language='en-US', show_all=True)
                    if result and 'alternative' in result and len(result['alternative']) > 0:
                        best_result = result['alternative'][0]
                        if 'transcript' in best_result:
                            text = best_result['transcript']
                            confidence = best_result.get('confidence', 0.5)
                            print(f"Recognized with confidence {confidence:.2f}: {text}", file=sys.stderr)
                            return text.lower().strip()
                except (sr.UnknownValueError, sr.RequestError):
                    pass
                
                print("Could not understand audio", file=sys.stderr)
                return "unknown"
                        
            except sr.WaitTimeoutError:
                print("Listening timed out", file=sys.stderr)
                return "timeout"
            except Exception as e:
                print(f"Recognition failed: {str(e)}", file=sys.stderr)
                return "error"
                        
    except Exception as e:
        print(f"Microphone error: {str(e)}", file=sys.stderr)
        return "error"

if __name__ == "__main__":
    result = recognize_speech()
    print(result)  # This will be captured by the C program