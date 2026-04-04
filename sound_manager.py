import pygame
import os
import math
import array


class SoundManager:
    """游戏音效管理器 - 改进版"""
    
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.5
        
        # 初始化混音器
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            self.enabled = False
            print("Warning: Cannot initialize sound system")
            return
        
        # 创建sounds目录
        self.sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # 加载或生成音效
        self._init_sounds()
    
    def _init_sounds(self):
        """初始化所有音效"""
        # 生成更动听的音效
        self.sounds['move'] = self._generate_tone(400, 60, 0.25, 'sine')  # 清脆短音
        self.sounds['rotate'] = self._generate_sweep(350, 450, 80, 0.3)   # 滑音效果
        self.sounds['drop'] = self._generate_tone(150, 100, 0.4, 'sine')  # 沉重低音
        self.sounds['clear'] = self._generate_arpeggio()                   # 琶音
        self.sounds['level_up'] = self._generate_victory_fanfare()         # 胜利号角
        self.sounds['game_over'] = self._generate_sad_tone()               # 悲伤长音
    
    def _generate_tone(self, frequency, duration_ms, volume=0.5, wave_type='sine', fade=True):
        """生成单音调"""
        try:
            sample_rate = 44100
            duration = duration_ms / 1000.0
            num_samples = int(sample_rate * duration)
            
            sound_data = array.array('h')
            
            for i in range(num_samples):
                t = i / sample_rate
                
                # ADSR包络
                attack = min(1.0, i / (sample_rate * 0.01))  # 10ms attack
                release = max(0.0, 1.0 - (i - num_samples * 0.7) / (num_samples * 0.3)) if i > num_samples * 0.7 else 1.0
                envelope = attack * release if fade else 1.0
                
                # 生成波形
                if wave_type == 'sine':
                    # 正弦波加谐波
                    value = 0.6 * math.sin(2 * math.pi * frequency * t)
                    value += 0.3 * math.sin(2 * math.pi * frequency * 2 * t)
                    value += 0.1 * math.sin(2 * math.pi * frequency * 3 * t)
                elif wave_type == 'triangle':
                    # 三角波
                    period = 1.0 / frequency
                    phase = (t % period) / period
                    value = 2 * abs(2 * phase - 1) - 1
                else:
                    value = math.sin(2 * math.pi * frequency * t)
                
                value *= volume * envelope
                sample = int(value * 32767)
                sound_data.append(sample)
                sound_data.append(sample)
            
            return pygame.mixer.Sound(buffer=sound_data.tobytes())
        except:
            return None
    
    def _generate_sweep(self, start_freq, end_freq, duration_ms, volume=0.5):
        """生成频率滑音"""
        try:
            sample_rate = 44100
            duration = duration_ms / 1000.0
            num_samples = int(sample_rate * duration)
            
            sound_data = array.array('h')
            
            for i in range(num_samples):
                t = i / sample_rate
                progress = i / num_samples
                
                # 对数频率插值
                freq = start_freq * (end_freq / start_freq) ** progress
                
                # 包络
                envelope = 1.0
                if progress < 0.1:
                    envelope = progress / 0.1
                elif progress > 0.7:
                    envelope = 1.0 - (progress - 0.7) / 0.3
                
                value = math.sin(2 * math.pi * freq * t)
                value *= volume * envelope
                
                sample = int(value * 32767)
                sound_data.append(sample)
                sound_data.append(sample)
            
            return pygame.mixer.Sound(buffer=sound_data.tobytes())
        except:
            return None
    
    def _generate_arpeggio(self):
        """生成消行琶音（C大调和弦分解）"""
        try:
            sample_rate = 44100
            duration = 0.15  # 每个音符150ms
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            
            sound_data = array.array('h')
            total_samples = int(sample_rate * duration * len(notes))
            
            for i in range(total_samples):
                t = i / sample_rate
                note_index = int(t / duration)
                note_progress = (t % duration) / duration
                
                if note_index >= len(notes):
                    note_index = len(notes) - 1
                
                freq = notes[note_index]
                
                # 包络
                attack = min(1.0, note_progress / 0.1)
                release = max(0.0, 1.0 - (note_progress - 0.6) / 0.4) if note_progress > 0.6 else 1.0
                envelope = attack * release
                
                # 方波（8位风格）
                value = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
                
                # 添加少量锯齿波丰富音色
                period = 1.0 / freq
                phase = (t % period) / period
                value += 0.2 * (2 * phase - 1)
                
                value *= 0.4 * envelope
                
                sample = int(value * 32767)
                sound_data.append(sample)
                sound_data.append(sample)
            
            return pygame.mixer.Sound(buffer=sound_data.tobytes())
        except:
            return None
    
    def _generate_victory_fanfare(self):
        """生成胜利号角（更丰富的音效）"""
        try:
            sample_rate = 44100
            # 胜利旋律音符 (G4, C5, E5, G5, C6)
            melody = [
                (392.00, 0.12),  # G4
                (523.25, 0.12),  # C5
                (659.25, 0.12),  # E5
                (783.99, 0.15),  # G5
                (1046.50, 0.4),  # C6 (长音)
            ]
            
            sound_data = array.array('h')
            current_time = 0
            
            for freq, duration in melody:
                num_samples = int(sample_rate * duration)
                for i in range(num_samples):
                    t = current_time + i / sample_rate
                    progress = i / num_samples
                    
                    # 包络
                    attack = min(1.0, progress / 0.05)
                    release = max(0.0, 1.0 - (progress - 0.7) / 0.3) if progress > 0.7 else 1.0
                    envelope = attack * release
                    
                    # 混合波形
                    value = 0.4 * math.sin(2 * math.pi * freq * t)  # 基频
                    value += 0.3 * math.sin(2 * math.pi * freq * 2 * t)  # 2次谐波
                    value += 0.2 * math.sin(2 * math.pi * freq * 0.5 * t)  # 低音
                    
                    value *= 0.5 * envelope
                    
                    sample = int(value * 32767)
                    sound_data.append(sample)
                    sound_data.append(sample)
                
                current_time += duration
            
            return pygame.mixer.Sound(buffer=sound_data.tobytes())
        except:
            return None
    
    def _generate_sad_tone(self):
        """生成游戏结束音效（悲伤下降）"""
        try:
            sample_rate = 44100
            duration = 1.0
            num_samples = int(sample_rate * duration)
            
            sound_data = array.array('h')
            
            for i in range(num_samples):
                t = i / sample_rate
                progress = i / num_samples
                
                # 频率下降
                start_freq = 300
                end_freq = 80
                freq = start_freq * (end_freq / start_freq) ** progress
                
                # 包络
                envelope = 1.0 - progress ** 0.5
                
                # 锯齿波
                period = 1.0 / max(freq, 1)
                phase = (t % period) / period
                value = 2 * phase - 1
                
                # 添加一些噪声
                noise = (hash(str(i)) % 1000) / 1000 - 0.5
                value += noise * 0.1 * (1 - progress)
                
                value *= 0.5 * envelope
                
                sample = int(value * 32767)
                sound_data.append(sample)
                sound_data.append(sample)
            
            return pygame.mixer.Sound(buffer=sound_data.tobytes())
        except:
            return None
    
    def play(self, sound_name):
        """播放指定音效"""
        if not self.enabled or not self.sounds:
            return
        
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()
    
    def play_move(self):
        """播放移动音效"""
        self.play('move')
    
    def play_rotate(self):
        """播放旋转音效"""
        self.play('rotate')
    
    def play_drop(self):
        """播放下落音效"""
        self.play('drop')
    
    def play_clear(self, lines_count=1):
        """播放消行音效"""
        if lines_count == 4:
            # 四连消播放两次琶音
            self.play('clear')
            pygame.time.set_timer(pygame.USEREVENT + 1, 150)
        else:
            self.play('clear')
    
    def play_level_up(self):
        """播放升级音效"""
        self.play('level_up')
    
    def play_game_over(self):
        """播放游戏结束音效"""
        self.play('game_over')
    
    def start_music(self):
        """开始播放背景音乐"""
        if not self.enabled or self.music_playing:
            return
        
        try:
            self._play_background_music()
            self.music_playing = True
        except Exception as e:
            print(f"Music play failed: {e}")
    
    def _play_background_music(self):
        """生成并播放背景音乐（更动听的电子乐）"""
        try:
            sample_rate = 44100
            bpm = 100
            beat_duration = 60.0 / bpm
            num_beats = 16
            
            # 低音进行 (C - G - Am - F)
            bass_progression = [
                130.81, 130.81, 98.00, 98.00,  # C3, G2
                110.00, 110.00, 87.31, 87.31,  # A2, F2
                130.81, 130.81, 98.00, 98.00,
                110.00, 110.00, 87.31, 87.31
            ]
            
            music_data = array.array('h')
            samples_per_beat = int(sample_rate * beat_duration)
            
            for beat, note in enumerate(bass_progression):
                for i in range(samples_per_beat):
                    t = i / sample_rate
                    progress = i / samples_per_beat
                    
                    # 低音正弦波
                    bass = 0.3 * math.sin(2 * math.pi * note * t)
                    
                    # 添加低音的八度
                    bass += 0.15 * math.sin(2 * math.pi * note * 2 * t)
                    
                    # 简单的节奏鼓点
                    kick = 0
                    if beat % 4 == 0 and progress < 0.1:
                        # 重拍鼓
                        kick_freq = 150 * (1 - progress * 10)
                        kick = 0.4 * math.sin(2 * math.pi * kick_freq * t)
                    elif beat % 2 == 1 and progress < 0.05:
                        # 轻拍手
                        noise = ((i % 13) / 13 - 0.5)
                        kick = noise * 0.2
                    
                    # 混音
                    value = bass + kick
                    value = max(-0.8, min(0.8, value))
                    value *= 0.25 * 32767
                    
                    music_data.append(int(value))
                    music_data.append(int(value))
            
            # 创建背景音乐并循环播放
            music_sound = pygame.mixer.Sound(buffer=music_data.tobytes())
            music_sound.set_volume(0.15)
            pygame.mixer.Channel(7).play(music_sound, loops=-1)
            
        except Exception as e:
            print(f"Generate music failed: {e}")
    
    def stop_music(self):
        """停止背景音乐"""
        if self.enabled:
            pygame.mixer.Channel(7).stop()
            self.music_playing = False
    
    def set_volume(self, volume):
        """设置音量 (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def toggle(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
        return self.enabled
