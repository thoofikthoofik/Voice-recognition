import speech_recognition as sr
import sys
import numpy as np
import time
from scipy.signal import butter, filtfilt
import io
import wave

def apply_audio_filter(audio_data, sample_rate=44100):
    """Apply audio filtering to reduce noise and enhance speech"""
    try:
        # Convert audio to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        
        # Normalize audio
        audio_np = audio_np / np.max(np.abs(audio_np))
        
        # Apply bandpass filter (human speech is typically 80Hz-8000Hz)
        nyquist = sample_rate / 2
        low_cutoff = 80 / nyquist
        high_cutoff = 8000 / nyquist
        
        # Design bandpass filter
        b, a = butter(4, [low_cutoff, high_cutoff], btype='band')
        filtered_audio = filtfilt(b, a, audio_np)
        
        # Apply noise gate (reduce very quiet sounds)
        threshold = 0.01
        filtered_audio = np.where(np.abs(filtered_audio) > threshold, filtered_audio, 0)
        
        # Convert back to int16
        filtered_audio = (filtered_audio * 32767).astype(np.int16)
        
        return filtered_audio.tobytes()
    except Exception as e:
        print(f"Filter error: {e}", file=sys.stderr)
        return audio_data

def detect_voice_activity(audio_data, sample_rate=44100, frame_duration=0.02):
    """Simple voice activity detection"""
    try:
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        frame_length = int(sample_rate * frame_duration)
        
        # Calculate energy for each frame
        num_frames = len(audio_np) // frame_length
        energy = []
        
        for i in range(num_frames):
            frame = audio_np[i * frame_length:(i + 1) * frame_length]
            frame_energy = np.sum(frame ** 2) / len(frame)
            energy.append(frame_energy)
        
        if not energy:
            return False
            
        # Voice activity if energy is above threshold
        avg_energy = np.mean(energy)
        max_energy = np.max(energy)
        
        # Dynamic threshold based on audio characteristics
        threshold = avg_energy * 3
        voice_frames = sum(1 for e in energy if e > threshold)
        voice_ratio = voice_frames / len(energy)
        
        return voice_ratio > 0.1  # At least 10% of frames contain voice
    except Exception as e:
        print(f"VAD error: {e}", file=sys.stderr)
        return True  # Assume voice present if detection fails

def recognize_speech_enhanced():
    """Enhanced speech recognition with better accuracy settings"""
    recognizer = sr.Recognizer()
    
    # Optimal settings for maximum accuracy
    recognizer.energy_threshold = 500  # Higher threshold for cleaner audio
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.05  # Very aggressive noise adaptation
    recognizer.dynamic_energy_ratio = 1.2  # Conservative ratio for better accuracy
    recognizer.pause_threshold = 1.2  # Wait for complete thoughts
    recognizer.phrase_threshold = 0.1  # Start listening immediately
    recognizer.non_speaking_duration = 1.0  # Clear pause detection
    
    try:
        # Use highest quality microphone settings
        with sr.Microphone(sample_rate=44100, chunk_size=512) as source:
            print("🎤 Calibrating microphone for optimal accuracy...", file=sys.stderr)
            
            # Extended calibration period
            recognizer.adjust_for_ambient_noise(source, duration=5)
            
            print("Ready! Speak clearly and naturally (6-12 inches from microphone)", file=sys.stderr)
            
            # Multiple recognition attempts with different strategies
            max_attempts = 3
            
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        print(f"Attempt {attempt + 1}/3 - Please repeat your command clearly", file=sys.stderr)
                    
                    # Optimized listening parameters
                    audio = recognizer.listen(
                        source, 
                        timeout=35, 
                        phrase_time_limit=10
                    )
                    
                    print("Audio captured, processing with multiple engines...", file=sys.stderr)
                    
                    # Multiple recognition engines/languages for best results
                    recognition_strategies = [
                        ('en-US', 'US English'),
                        ('en-GB', 'UK English'),
                        ('en-CA', 'Canadian English'),
                        ('en-AU', 'Australian English'),
                        ('en-IN', 'Indian English')
                    ]
                    
                    best_result = None
                    best_confidence = 0
                    
                    for lang_code, description in recognition_strategies:
                        try:
                            # Try with confidence scores first
                            result = recognizer.recognize_google(
                                audio, 
                                language=lang_code, 
                                show_all=True
                            )
                            
                            if result and 'alternative' in result:
                                for alternative in result['alternative']:
                                    if 'transcript' in alternative:
                                        transcript = alternative['transcript']
                                        confidence = alternative.get('confidence', 0.5)
                                        
                                        if confidence > best_confidence and len(transcript.strip()) > 0:
                                            best_result = transcript
                                            best_confidence = confidence
                                            print(f"Testing {description}: '{transcript}' (confidence: {confidence:.2f})", file=sys.stderr)
                            
                            # If we found a good result, break early
                            if best_result and best_confidence > 0.7:
                                break
                                        
                        except (sr.UnknownValueError, sr.RequestError):
                            continue
                        except Exception as e:
                            continue
                    
                    # Try standard recognition only if no good confident result
                    if not best_result or best_confidence < 0.5:
                        try:
                            text = recognizer.recognize_google(audio, language='en-US')
                            if text and len(text.strip()) > 0:
                                best_result = text
                                best_confidence = 0.6  # Assume decent confidence
                                print(f"Standard recognition: '{text}'", file=sys.stderr)
                        except (sr.UnknownValueError, sr.RequestError):
                            pass
                    
                    # Return best result if confidence is good enough
                    if best_result and best_confidence > 0.4:
                        final_result = best_result.lower().strip()
                        print(f"🎯 Final result: '{final_result}' (confidence: {best_confidence:.2f})", file=sys.stderr)
                        return final_result
                    
                    # If low confidence, try next attempt
                    if attempt < max_attempts - 1:
                        print(f"⚠️ Low confidence ({best_confidence:.2f}), trying again...", file=sys.stderr)
                        time.sleep(0.5)  # Brief pause
                        continue
                    else:
                        if best_result:
                            print(f"⚠️ Returning low-confidence result: '{best_result}'", file=sys.stderr)
                            return best_result.lower().strip()
                        else:
                            return "unknown"
                            
                except sr.WaitTimeoutError:
                    if attempt < max_attempts - 1:
                        print("⏱️ No speech detected, please try again", file=sys.stderr)
                        continue
                    else:
                        return "timeout"
                        
                except Exception as e:
                    if attempt < max_attempts - 1:
                        print(f"⚠️ Recognition error: {e}, retrying...", file=sys.stderr)
                        continue
                    else:
                        print(f"❌ Final attempt failed: {e}", file=sys.stderr)
                        return "error"
            
            return "max_attempts_exceeded"
            
    except Exception as e:
        print(f"❌ Microphone error: {e}", file=sys.stderr)
        return "microphone_error"

if __name__ == "__main__":
    try:
        result = recognize_speech_enhanced()
        print(result)  # This will be captured by the web application
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        print("interrupted")
    except Exception as e:
        print(f"Critical error: {e}", file=sys.stderr)
        print("critical_error") 