"""
VHALINOR Sistema Sensorial v6.0
================================
Sistema sensorial completo para ai_geral:
- Câmera como olhos (OpenCV)
- Microfone como ouvidos (PyAudio/SoundDevice)
- Auto-falantes como voz (pyttsx3/gTTS)
- Detecção automática de dispositivos
- Processamento de entrada sensorial
- Síntese de fala
- Análise de áudio e vídeo

@module sensorial
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque
import threading
import time
import os
import platform
import subprocess
import json
import base64
import io

# Imports opcionais com fallback
OPENCV_AVAILABLE = False
PYAUDIO_AVAILABLE = False
SOUNDDEVICE_AVAILABLE = False
PYTTSX3_AVAILABLE = False
GTTS_AVAILABLE = False
PIL_AVAILABLE = False
LIBROSA_AVAILABLE = False

# Tentar importar OpenCV para visão
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    cv2 = None

# Tentar importar PyAudio para áudio
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None

# Tentar importar SoundDevice como alternativa
try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    sd = None
    sf = None

# Tentar importar pyttsx3 para fala local
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pyttsx3 = None

# Tentar importar gTTS para fala online
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    gTTS = None

# Tentar importar PIL para processamento de imagem
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    Image = None

# Tentar importar librosa para análise de áudio
try:
    import librosa
    import librosa.display
    LIBROSA_AVAILABLE = True
except ImportError:
    librosa = None


class TipoSensor(Enum):
    """Tipos de sensores disponíveis"""
    CAMERA = "camera"           # Visão
    MICROFONE = "microfone"     # Audição
    AUTO_FALANTE = "auto_falante"  # Fala/Voz
    TOQUE = "toque"             # Haptic (futuro)
    MOVIMENTO = "movimento"     # Aceleração/Giro (futuro)


class EstadoSensor(Enum):
    """Estados de um sensor"""
    INATIVO = "inativo"
    INICIALIZANDO = "inicializando"
    ATIVO = "ativo"
    CAPTURANDO = "capturando"
    REPRODUZINDO = "reproduzindo"
    ERRO = "erro"
    PAUSADO = "pausado"


class QualidadeVideo(Enum):
    """Qualidades de vídeo disponíveis"""
    BAIXA = (320, 240, 15)
    MEDIA = (640, 480, 30)
    ALTA = (1280, 720, 30)
    FULL_HD = (1920, 1080, 30)
    
    def __init__(self, largura, altura, fps):
        self.largura = largura
        self.altura = altura
        self.fps = fps


class QualidadeAudio(Enum):
    """Qualidades de áudio disponíveis"""
    BAIXA = (8000, 8, 1)       # 8kHz, 8bit, mono
    MEDIA = (16000, 16, 1)     # 16kHz, 16bit, mono
    ALTA = (44100, 16, 2)      # 44.1kHz, 16bit, stereo
    CD = (44100, 24, 2)        # 44.1kHz, 24bit, stereo
    
    def __init__(self, taxa_amostragem, bits, canais):
        self.taxa_amostragem = taxa_amostragem
        self.bits = bits
        self.canais = canais


@dataclass
class DispositivoSensor:
    """Representação de um dispositivo sensorial"""
    id: str
    nome: str
    tipo: TipoSensor
    indice: int
    esta_disponivel: bool = True
    estado: EstadoSensor = EstadoSensor.INATIVO
    capacidades: Dict[str, Any] = field(default_factory=dict)
    driver: str = "desconhecido"
    caminho_dispositivo: Optional[str] = None
    
    def __str__(self) -> str:
        status = "✓" if self.esta_disponivel else "✗"
        return f"[{status}] {self.nome} ({self.tipo.value}) - {self.estado.value}"


@dataclass
class FrameCapturado:
    """Frame de vídeo capturado"""
    dados: np.ndarray
    timestamp: str
    largura: int
    altura: int
    taxa_fps: float
    dispositivo_id: str
    formato: str = "bgr"
    
    @property
    def tamanho_bytes(self) -> int:
        return self.dados.nbytes if self.dados is not None else 0
    
    def para_rgb(self) -> Optional[np.ndarray]:
        """Converter para RGB se necessário"""
        if self.formato == "bgr" and self.dados is not None:
            return cv2.cvtColor(self.dados, cv2.COLOR_BGR2RGB) if OPENCV_AVAILABLE else None
        return self.dados
    
    def para_base64(self) -> str:
        """Converter frame para string base64"""
        if self.dados is None:
            return ""
        try:
            if OPENCV_AVAILABLE:
                _, buffer = cv2.imencode('.jpg', self.dados)
                return base64.b64encode(buffer).decode('utf-8')
        except Exception:
            pass
        return ""


@dataclass
class AmostraAudio:
    """Amostra de áudio capturada"""
    dados: np.ndarray
    timestamp: str
    taxa_amostragem: int
    canais: int
    duracao_segundos: float
    dispositivo_id: str
    volume_medio: float = 0.0
    
    def __post_init__(self):
        if self.dados is not None and len(self.dados) > 0:
            self.volume_medio = np.abs(self.dados).mean()


@dataclass
class ReconhecimentoVisual:
    """Resultado de reconhecimento visual"""
    tipo: str  # "rosto", "objeto", "texto", "movimento"
    confianca: float
    localizacao: Optional[Tuple[int, int, int, int]] = None  # x, y, w, h
    descricao: str = ""
    dados_adicionais: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnaliseAudio:
    """Análise de áudio capturado"""
    tem_voz: bool
    volume: float
    frequencia_dominante: Optional[float] = None
    pitch: Optional[float] = None
    ruido_estimado: float = 0.0
    transcrição: Optional[str] = None
    sentimento_vocal: Optional[str] = None  # "calmo", "agitado", "feliz", "triste"


class SistemaSensorial:
    """
    Sistema sensorial completo da VHALINOR ai_geral.
    
    Simula os sentidos humanos através de hardware:
    - Olhos: Câmeras (visão)
    - Ouvidos: Microfones (audição)
    - Voz: Auto-falantes (fala)
    """
    
    def __init__(self):
        self.nome = "VHALINOR Sensorial"
        self.versao = "6.0.0"
        
        # Dispositivos detectados
        self.dispositivos: Dict[str, DispositivoSensor] = {}
        self.dispositivos_por_tipo: Dict[TipoSensor, List[str]] = {
            TipoSensor.CAMERA: [],
            TipoSensor.MICROFONE: [],
            TipoSensor.AUTO_FALANTE: []
        }
        
        # Estado atual
        self.camera_ativa: Optional[str] = None
        self.microfone_ativo: Optional[str] = None
        self.auto_falante_ativo: Optional[str] = None
        
        # Captura em andamento
        self._captura_video_ativa = False
        self._captura_audio_ativa = False
        self._thread_captura: Optional[threading.Thread] = None
        
        # Buffers
        self.buffer_frames: deque = deque(maxlen=30)  # ~1 segundo a 30fps
        self.buffer_audio: deque = deque(maxlen=10)   # ~1 segundo de áudio
        
        # Engines
        self._engine_fala = None
        self._captura_opencv = None
        self._stream_audio = None
        
        # Callbacks
        self._on_frame: List[Callable] = []
        self._on_audio: List[Callable] = []
        self._on_fala_concluida: List[Callable] = []
        
        # Métricas
        self.frames_capturados = 0
        self.amostras_audio_capturadas = 0
        self.falas_reproduzidas = 0
        
        # Detectar dispositivos na inicialização
        self._detectar_todos_dispositivos()
    
    def _detectar_todos_dispositivos(self):
        """Detectar todos os dispositivos sensoriais disponíveis na máquina"""
        self._detectar_cameras()
        self._detectar_microfones()
        self._detectar_auto_falantes()
    
    def _detectar_cameras(self):
        """Detectar câmeras disponíveis na máquina"""
        if not OPENCV_AVAILABLE:
            # Fallback: tentar detectar via sistema operacional
            self._detectar_cameras_sistema()
            return
        
        indice = 0
        max_cameras = 10
        
        while indice < max_cameras:
            try:
                cap = cv2.VideoCapture(indice)
                if cap.isOpened():
                    # Obter informações da câmera
                    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    
                    dispositivo = DispositivoSensor(
                        id=f"cam_{indice}",
                        nome=f"Câmera {indice} ({largura}x{altura}@{fps:.0f}fps)",
                        tipo=TipoSensor.CAMERA,
                        indice=indice,
                        esta_disponivel=True,
                        estado=EstadoSensor.INATIVO,
                        capacidades={
                            "largura": largura,
                            "altura": altura,
                            "fps": fps,
                            "formatos": ["MJPG", "YUY2", "RGB"]
                        },
                        driver="OpenCV/DirectShow" if platform.system() == "Windows" else "Video4Linux2"
                    )
                    
                    self.dispositivos[dispositivo.id] = dispositivo
                    self.dispositivos_por_tipo[TipoSensor.CAMERA].append(dispositivo.id)
                    
                    cap.release()
                
                indice += 1
                
            except Exception as e:
                break
        
        # Se não encontrou câmeras, usar fallback
        if not self.dispositivos_por_tipo[TipoSensor.CAMERA]:
            self._detectar_cameras_sistema()
    
    def _detectar_cameras_sistema(self):
        """Detectar câmeras via comandos do sistema operacional"""
        sistema = platform.system()
        cameras_encontradas = []
        
        try:
            if sistema == "Windows":
                # Usar PowerShell para listar dispositivos de vídeo
                comando = "Get-PnpDevice -Class Camera | Select-Object Name, Status"
                resultado = subprocess.run(
                    ["powershell", "-Command", comando],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if resultado.returncode == 0:
                    linhas = resultado.stdout.strip().split('\n')
                    for i, linha in enumerate(linhas[2:], start=0):  # Pular header
                        if linha.strip() and "---" not in linha:
                            partes = linha.strip().split(None, 1)
                            if len(partes) >= 1:
                                nome = partes[0] if partes[0] else f"Câmera {i}"
                                status = partes[1] if len(partes) > 1 else "OK"
                                
                                dispositivo = DispositivoSensor(
                                    id=f"cam_{i}",
                                    nome=nome,
                                    tipo=TipoSensor.CAMERA,
                                    indice=i,
                                    esta_disponivel="error" not in status.lower(),
                                    estado=EstadoSensor.INATIVO,
                                    capacidades={},
                                    driver="DirectShow/Windows"
                                )
                                cameras_encontradas.append(dispositivo)
            
            elif sistema == "Linux":
                # Listar dispositivos de vídeo do Linux
                try:
                    resultado = subprocess.run(
                        ["ls", "-la", "/dev/video*"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if resultado.returncode == 0:
                        linhas = resultado.stdout.strip().split('\n')
                        for i, linha in enumerate(linhas):
                            if "/dev/video" in linha:
                                dispositivo = DispositivoSensor(
                                    id=f"cam_{i}",
                                    nome=f"Dispositivo de Vídeo Linux {i}",
                                    tipo=TipoSensor.CAMERA,
                                    indice=i,
                                    esta_disponivel=True,
                                    estado=EstadoSensor.INATIVO,
                                    capacidades={},
                                    driver="Video4Linux2",
                                    caminho_dispositivo=f"/dev/video{i}"
                                )
                                cameras_encontradas.append(dispositivo)
                except Exception:
                    pass
                
                # Tentar v4l2-ctl se disponível
                try:
                    resultado = subprocess.run(
                        ["v4l2-ctl", "--list-devices"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if resultado.returncode == 0:
                        # Parse output v4l2-ctl
                        pass  # Implementação específica
                except Exception:
                    pass
            
            elif sistema == "Darwin":  # macOS
                # macOS usa AVFoundation
                dispositivo = DispositivoSensor(
                    id="cam_0",
                    nome="Câmera Padrão macOS",
                    tipo=TipoSensor.CAMERA,
                    indice=0,
                    esta_disponivel=True,
                    estado=EstadoSensor.INATIVO,
                    capacidades={},
                    driver="AVFoundation"
                )
                cameras_encontradas.append(dispositivo)
        
        except Exception as e:
            pass
        
        # Adicionar câmeras encontradas
        for i, cam in enumerate(cameras_encontradas):
            if cam.id not in self.dispositivos:
                self.dispositivos[cam.id] = cam
                self.dispositivos_por_tipo[TipoSensor.CAMERA].append(cam.id)
    
    def _detectar_microfones(self):
        """Detectar microfones disponíveis na máquina"""
        if PYAUDIO_AVAILABLE and pyaudio is not None:
            self._detectar_microfones_pyaudio()
        elif SOUNDDEVICE_AVAILABLE and sd is not None:
            self._detectar_microfones_sounddevice()
        else:
            self._detectar_microfones_sistema()
    
    def _detectar_microfones_pyaudio(self):
        """Detectar microfones usando PyAudio"""
        try:
            audio = pyaudio.PyAudio()
            info = audio.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            for i in range(numdevices):
                device_info = audio.get_device_info_by_host_api_device_index(0, i)
                
                if device_info.get('maxInputChannels') > 0:
                    nome = device_info.get('name', f"Microfone {i}")
                    
                    dispositivo = DispositivoSensor(
                        id=f"mic_{i}",
                        nome=nome,
                        tipo=TipoSensor.MICROFONE,
                        indice=i,
                        esta_disponivel=True,
                        estado=EstadoSensor.INATIVO,
                        capacidades={
                            "canais": device_info.get('maxInputChannels'),
                            "taxa_amostragem_padrao": int(device_info.get('defaultSampleRate', 44100))
                        },
                        driver="PyAudio/PortAudio"
                    )
                    
                    self.dispositivos[dispositivo.id] = dispositivo
                    self.dispositivos_por_tipo[TipoSensor.MICROFONE].append(dispositivo.id)
            
            audio.terminate()
            
        except Exception as e:
            self._detectar_microfones_sistema()
    
    def _detectar_microfones_sounddevice(self):
        """Detectar microfones usando SoundDevice"""
        try:
            dispositivos = sd.query_devices()
            
            for i, device in enumerate(dispositivos):
                if device.get('max_input_channels', 0) > 0:
                    nome = device.get('name', f"Microfone {i}")
                    
                    dispositivo = DispositivoSensor(
                        id=f"mic_{i}",
                        nome=nome,
                        tipo=TipoSensor.MICROFONE,
                        indice=i,
                        esta_disponivel=True,
                        estado=EstadoSensor.INATIVO,
                        capacidades={
                            "canais": device.get('max_input_channels'),
                            "taxa_amostragem_padrao": int(device.get('default_samplerate', 44100))
                        },
                        driver="SoundDevice/CoreAudio"
                    )
                    
                    self.dispositivos[dispositivo.id] = dispositivo
                    self.dispositivos_por_tipo[TipoSensor.MICROFONE].append(dispositivo.id)
                    
        except Exception as e:
            self._detectar_microfones_sistema()
    
    def _detectar_microfones_sistema(self):
        """Detectar microfones via sistema operacional"""
        sistema = platform.system()
        
        try:
            if sistema == "Windows":
                # Listar dispositivos de áudio no Windows
                comando = "Get-PnpDevice -Class AudioEndpoint | Where-Object {$_.FriendlyName -like '*microphone*' -or $_.FriendlyName -like '*mic*'} | Select-Object Name"
                resultado = subprocess.run(
                    ["powershell", "-Command", comando],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if resultado.returncode == 0:
                    linhas = resultado.stdout.strip().split('\n')
                    for i, linha in enumerate(linhas[2:], start=0):
                        if linha.strip() and "---" not in linha:
                            dispositivo = DispositivoSensor(
                                id=f"mic_{i}",
                                nome=linha.strip(),
                                tipo=TipoSensor.MICROFONE,
                                indice=i,
                                esta_disponivel=True,
                                estado=EstadoSensor.INATIVO,
                                capacidades={},
                                driver="Windows Audio"
                            )
                            self.dispositivos[dispositivo.id] = dispositivo
                            self.dispositivos_por_tipo[TipoSensor.MICROFONE].append(dispositivo.id)
            
            elif sistema == "Linux":
                # Tentar detectar via ALSA
                try:
                    resultado = subprocess.run(
                        ["arecord", "-l"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if resultado.returncode == 0:
                        # Parse arecord -l output
                        dispositivo = DispositivoSensor(
                            id="mic_0",
                            nome="Dispositivo de Captura ALSA",
                            tipo=TipoSensor.MICROFONE,
                            indice=0,
                            esta_disponivel=True,
                            estado=EstadoSensor.INATIVO,
                            capacidades={},
                            driver="ALSA"
                        )
                        self.dispositivos[dispositivo.id] = dispositivo
                        self.dispositivos_por_tipo[TipoSensor.MICROFONE].append(dispositivo.id)
                except Exception:
                    pass
            
            elif sistema == "Darwin":
                dispositivo = DispositivoSensor(
                    id="mic_0",
                    nome="Microfone Padrão macOS",
                    tipo=TipoSensor.MICROFONE,
                    indice=0,
                    esta_disponivel=True,
                    estado=EstadoSensor.INATIVO,
                    capacidades={},
                    driver="CoreAudio"
                )
                self.dispositivos[dispositivo.id] = dispositivo
                self.dispositivos_por_tipo[TipoSensor.MICROFONE].append(dispositivo.id)
        
        except Exception as e:
            pass
    
    def _detectar_auto_falantes(self):
        """Detectar dispositivos de saída de áudio (auto-falantes)"""
        if PYAUDIO_AVAILABLE and pyaudio is not None:
            self._detectar_auto_falantes_pyaudio()
        elif SOUNDDEVICE_AVAILABLE and sd is not None:
            self._detectar_auto_falantes_sounddevice()
        else:
            self._detectar_auto_falantes_sistema()
    
    def _detectar_auto_falantes_pyaudio(self):
        """Detectar auto-falantes usando PyAudio"""
        try:
            audio = pyaudio.PyAudio()
            info = audio.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            for i in range(numdevices):
                device_info = audio.get_device_info_by_host_api_device_index(0, i)
                
                if device_info.get('maxOutputChannels') > 0:
                    nome = device_info.get('name', f"Auto-falante {i}")
                    
                    dispositivo = DispositivoSensor(
                        id=f"spk_{i}",
                        nome=nome,
                        tipo=TipoSensor.AUTO_FALANTE,
                        indice=i,
                        esta_disponivel=True,
                        estado=EstadoSensor.INATIVO,
                        capacidades={
                            "canais": device_info.get('maxOutputChannels'),
                            "taxa_amostragem_padrao": int(device_info.get('defaultSampleRate', 44100))
                        },
                        driver="PyAudio/PortAudio"
                    )
                    
                    self.dispositivos[dispositivo.id] = dispositivo
                    self.dispositivos_por_tipo[TipoSensor.AUTO_FALANTE].append(dispositivo.id)
            
            audio.terminate()
            
        except Exception as e:
            self._detectar_auto_falantes_sistema()
    
    def _detectar_auto_falantes_sounddevice(self):
        """Detectar auto-falantes usando SoundDevice"""
        try:
            dispositivos = sd.query_devices()
            
            for i, device in enumerate(dispositivos):
                if device.get('max_output_channels', 0) > 0:
                    nome = device.get('name', f"Auto-falante {i}")
                    
                    dispositivo = DispositivoSensor(
                        id=f"spk_{i}",
                        nome=nome,
                        tipo=TipoSensor.AUTO_FALANTE,
                        indice=i,
                        esta_disponivel=True,
                        estado=EstadoSensor.INATIVO,
                        capacidades={
                            "canais": device.get('max_output_channels'),
                            "taxa_amostragem_padrao": int(device.get('default_samplerate', 44100))
                        },
                        driver="SoundDevice/CoreAudio"
                    )
                    
                    self.dispositivos[dispositivo.id] = dispositivo
                    self.dispositivos_por_tipo[TipoSensor.AUTO_FALANTE].append(dispositivo.id)
                    
        except Exception as e:
            self._detectar_auto_falantes_sistema()
    
    def _detectar_auto_falantes_sistema(self):
        """Detectar auto-falantes via sistema operacional"""
        sistema = platform.system()
        
        dispositivos_padrao = [
            ("spk_0", "Auto-falantes Padrão", "Sistema"),
            ("spk_hdmi", "HDMI Audio", "HDMI"),
            ("spk_bt", "Bluetooth Audio", "Bluetooth")
        ]
        
        for id_disp, nome, driver in dispositivos_padrao:
            if id_disp not in self.dispositivos:
                dispositivo = DispositivoSensor(
                    id=id_disp,
                    nome=nome,
                    tipo=TipoSensor.AUTO_FALANTE,
                    indice=0,
                    esta_disponivel=True,
                    estado=EstadoSensor.INATIVO,
                    capacidades={},
                    driver=driver
                )
                self.dispositivos[dispositivo.id] = dispositivo
                self.dispositivos_por_tipo[TipoSensor.AUTO_FALANTE].append(dispositivo.id)
    
    # ============== MÉTODOS DE CONTROLE DE CÂMERA ==============
    
    def inicializar_camera(self, dispositivo_id: str, qualidade: QualidadeVideo = QualidadeVideo.MEDIA) -> bool:
        """Inicializar câmera para captura"""
        if dispositivo_id not in self.dispositivos:
            return False
        
        dispositivo = self.dispositivos[dispositivo_id]
        if dispositivo.tipo != TipoSensor.CAMERA:
            return False
        
        if not OPENCV_AVAILABLE or cv2 is None:
            dispositivo.estado = EstadoSensor.ERRO
            return False
        
        try:
            self._captura_opencv = cv2.VideoCapture(dispositivo.indice)
            
            if not self._captura_opencv.isOpened():
                dispositivo.estado = EstadoSensor.ERRO
                return False
            
            # Configurar resolução e FPS
            self._captura_opencv.set(cv2.CAP_PROP_FRAME_WIDTH, qualidade.largura)
            self._captura_opencv.set(cv2.CAP_PROP_FRAME_HEIGHT, qualidade.altura)
            self._captura_opencv.set(cv2.CAP_PROP_FPS, qualidade.fps)
            
            dispositivo.estado = EstadoSensor.ATIVO
            self.camera_ativa = dispositivo_id
            
            return True
            
        except Exception as e:
            dispositivo.estado = EstadoSensor.ERRO
            return False
    
    def capturar_frame(self) -> Optional[FrameCapturado]:
        """Capturar um único frame da câmera ativa"""
        if not OPENCV_AVAILABLE or self._captura_opencv is None:
            return None
        
        if not self._captura_opencv.isOpened():
            return None
        
        ret, frame = self._captura_opencv.read()
        
        if not ret or frame is None:
            return None
        
        altura, largura = frame.shape[:2]
        fps = self._captura_opencv.get(cv2.CAP_PROP_FPS)
        
        frame_capturado = FrameCapturado(
            dados=frame,
            timestamp=datetime.now(timezone.utc).isoformat(),
            largura=largura,
            altura=altura,
            taxa_fps=fps if fps > 0 else 30.0,
            dispositivo_id=self.camera_ativa or "unknown",
            formato="bgr"
        )
        
        self.buffer_frames.append(frame_capturado)
        self.frames_capturados += 1
        
        # Notificar callbacks
        for callback in self._on_frame:
            callback(frame_capturado)
        
        return frame_capturado
    
    def iniciir_captura_continua(self, fps_alvo: int = 30):
        """Iniciar captura contínua em thread separada"""
        if self._captura_video_ativa:
            return False
        
        self._captura_video_ativa = True
        
        def loop_captura():
            intervalo = 1.0 / fps_alvo
            while self._captura_video_ativa:
                self.capturar_frame()
                time.sleep(intervalo)
        
        self._thread_captura = threading.Thread(target=loop_captura, daemon=True)
        self._thread_captura.start()
        
        if self.camera_ativa:
            self.dispositivos[self.camera_ativa].estado = EstadoSensor.CAPTURANDO
        
        return True
    
    def parar_captura_video(self):
        """Parar captura contínua de vídeo"""
        self._captura_video_ativa = False
        
        if self._thread_captura:
            self._thread_captura.join(timeout=1.0)
        
        if self.camera_ativa and self.camera_ativa in self.dispositivos:
            self.dispositivos[self.camera_ativa].estado = EstadoSensor.ATIVO
    
    def liberar_camera(self):
        """Liberar recursos da câmera"""
        self.parar_captura_video()
        
        if self._captura_opencv:
            self._captura_opencv.release()
            self._captura_opencv = None
        
        if self.camera_ativa and self.camera_ativa in self.dispositivos:
            self.dispositivos[self.camera_ativa].estado = EstadoSensor.INATIVO
            self.camera_ativa = None
    
    # ============== MÉTODOS DE CONTROLE DE MICROFONE ==============
    
    def inicializar_microfone(
        self,
        dispositivo_id: str,
        qualidade: QualidadeAudio = QualidadeAudio.ALTA,
        duracao_chunk: float = 0.5
    ) -> bool:
        """Inicializar microfone para captura"""
        if dispositivo_id not in self.dispositivos:
            return False
        
        dispositivo = self.dispositivos[dispositivo_id]
        if dispositivo.tipo != TipoSensor.MICROFONE:
            return False
        
        dispositivo.estado = EstadoSensor.ATIVO
        self.microfone_ativo = dispositivo_id
        
        return True
    
    def capturar_audio(self, duracao_segundos: float = 3.0) -> Optional[AmostraAudio]:
        """Capturar áudio do microfone"""
        if not self.microfone_ativo:
            return None
        
        if SOUNDDEVICE_AVAILABLE and sd is not None:
            return self._capturar_audio_sounddevice(duracao_segundos)
        elif PYAUDIO_AVAILABLE and pyaudio is not None:
            return self._capturar_audio_pyaudio(duracao_segundos)
        else:
            # Fallback: gerar silêncio
            taxa = 44100
            amostras = int(taxa * duracao_segundos)
            dados = np.zeros(amostras, dtype=np.float32)
            
            return AmostraAudio(
                dados=dados,
                timestamp=datetime.now(timezone.utc).isoformat(),
                taxa_amostragem=taxa,
                canais=1,
                duracao_segundos=duracao_segundos,
                dispositivo_id=self.microfone_ativo or "fallback",
                volume_medio=0.0
            )
    
    def _capturar_audio_sounddevice(self, duracao: float) -> Optional[AmostraAudio]:
        """Capturar áudio usando SoundDevice"""
        try:
            taxa = 44100
            amostras = int(taxa * duracao)
            
            dados = sd.rec(amostras, samplerate=taxa, channels=1, dtype='float32')
            sd.wait()
            
            return AmostraAudio(
                dados=dados.flatten(),
                timestamp=datetime.now(timezone.utc).isoformat(),
                taxa_amostragem=taxa,
                canais=1,
                duracao_segundos=duracao,
                dispositivo_id=self.microfone_ativo or "sd",
                volume_medio=float(np.abs(dados).mean())
            )
        except Exception:
            return None
    
    def _capturar_audio_pyaudio(self, duracao: float) -> Optional[AmostraAudio]:
        """Capturar áudio usando PyAudio"""
        try:
            taxa = 44100
            chunk = 1024
            formato = pyaudio.paFloat32
            canais = 1
            
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=formato,
                channels=canais,
                rate=taxa,
                input=True,
                frames_per_buffer=chunk
            )
            
            frames = []
            for _ in range(0, int(taxa / chunk * duracao)):
                data = stream.read(chunk)
                frames.append(np.frombuffer(data, dtype=np.float32))
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            dados = np.concatenate(frames) if frames else np.array([])
            
            return AmostraAudio(
                dados=dados,
                timestamp=datetime.now(timezone.utc).isoformat(),
                taxa_amostragem=taxa,
                canais=canais,
                duracao_segundos=duracao,
                dispositivo_id=self.microfone_ativo or "pa",
                volume_medio=float(np.abs(dados).mean()) if len(dados) > 0 else 0.0
            )
        except Exception:
            return None
    
    def analisar_audio(self, amostra: AmostraAudio) -> AnaliseAudio:
        """Analisar áudio capturado"""
        if amostra.dados is None or len(amostra.dados) == 0:
            return AnaliseAudio(tem_voz=False, volume=0.0)
        
        volume = amostra.volume_medio
        tem_voz = volume > 0.01  # Threshold simples
        
        frequencia_dominante = None
        if LIBROSA_AVAILABLE and librosa is not None and len(amostra.dados) > 1024:
            try:
                # Calcular FFT
                fft = np.fft.fft(amostra.dados)
                freqs = np.fft.fftfreq(len(fft), 1.0 / amostra.taxa_amostragem)
                magnitude = np.abs(fft)
                
                # Encontrar frequência dominante
                idx_dominante = np.argmax(magnitude[:len(magnitude)//2])
                frequencia_dominante = abs(freqs[idx_dominante])
            except Exception:
                pass
        
        return AnaliseAudio(
            tem_voz=tem_voz,
            volume=volume,
            frequencia_dominante=frequencia_dominante,
            ruido_estimado=1.0 - min(1.0, volume * 10)
        )
    
    # ============== MÉTODOS DE FALA (AUTO-FALANTES) ==============
    
    def inicializar_fala(self, dispositivo_id: str = "auto") -> bool:
        """Inicializar sistema de fala"""
        if dispositivo_id != "auto" and dispositivo_id not in self.dispositivos:
            return False
        
        # Inicializar engine TTS
        if PYTTSX3_AVAILABLE and pyttsx3 is not None:
            try:
                self._engine_fala = pyttsx3.init()
                self._engine_fala.setProperty('rate', 150)  # Velocidade
                self._engine_fala.setProperty('volume', 0.9)  # Volume
                
                if dispositivo_id != "auto":
                    self.auto_falante_ativo = dispositivo_id
                    self.dispositivos[dispositivo_id].estado = EstadoSensor.ATIVO
                
                return True
            except Exception:
                pass
        
        # Se não conseguiu inicializar pyttsx3, usar gTTS
        if GTTS_AVAILABLE and gTTS is not None:
            self._engine_fala = "gtts"  # Marcador para usar gTTS
            if dispositivo_id != "auto":
                self.auto_falante_ativo = dispositivo_id
            return True
        
        return False
    
    def falar(self, texto: str, velocidade: str = "normal") -> bool:
        """Reproduzir texto como fala"""
        if not self._engine_fala:
            return False
        
        try:
            if isinstance(self._engine_fala, str) and self._engine_fala == "gtts":
                return self._falar_gtts(texto)
            else:
                return self._falar_pyttsx3(texto)
        except Exception:
            return False
    
    def _falar_pyttsx3(self, texto: str) -> bool:
        """Falar usando pyttsx3"""
        try:
            self._engine_fala.say(texto)
            self._engine_fala.runAndWait()
            self.falas_reproduzidas += 1
            
            # Notificar callbacks
            for callback in self._on_fala_concluida:
                callback(texto)
            
            return True
        except Exception:
            return False
    
    def _falar_gtts(self, texto: str) -> bool:
        """Falar usando gTTS (Google Text-to-Speech)"""
        try:
            tts = gTTS(text=texto, lang='pt-br')
            
            # Salvar em arquivo temporário
            arquivo_temp = io.BytesIO()
            tts.write_to_fp(arquivo_temp)
            arquivo_temp.seek(0)
            
            # Reproduzir usando sounddevice se disponível
            if SOUNDDEVICE_AVAILABLE and sf is not None:
                dados, taxa = sf.read(arquivo_temp)
                sd.play(dados, taxa)
                sd.wait()
            
            self.falas_reproduzidas += 1
            
            for callback in self._on_fala_concluida:
                callback(texto)
            
            return True
        except Exception:
            return False
    
    def parar_fala(self):
        """Parar reprodução de fala"""
        if PYTTSX3_AVAILABLE and self._engine_fala and not isinstance(self._engine_fala, str):
            try:
                self._engine_fala.stop()
            except Exception:
                pass
        elif SOUNDDEVICE_AVAILABLE and sd is not None:
            try:
                sd.stop()
            except Exception:
                pass
    
    def salvar_audio(self, amostra: AmostraAudio, caminho: str) -> bool:
        """Salvar amostra de áudio em arquivo"""
        if SOUNDDEVICE_AVAILABLE and sf is not None:
            try:
                sf.write(caminho, amostra.dados, amostra.taxa_amostragem)
                return True
            except Exception:
                return False
        return False
    
    def salvar_frame(self, frame: FrameCapturado, caminho: str) -> bool:
        """Salvar frame em arquivo de imagem"""
        if OPENCV_AVAILABLE and cv2 is not None and frame.dados is not None:
            try:
                cv2.imwrite(caminho, frame.dados)
                return True
            except Exception:
                return False
        return False
    
    # ============== MÉTODOS DE CALLBACK ==============
    
    def on_frame(self, callback: Callable):
        """Registrar callback para novos frames"""
        self._on_frame.append(callback)
    
    def on_audio(self, callback: Callable):
        """Registrar callback para novas amostras de áudio"""
        self._on_audio.append(callback)
    
    def on_fala_concluida(self, callback: Callable):
        """Registrar callback para fala concluída"""
        self._on_fala_concluida.append(callback)
    
    # ============== MÉTODOS DE UTILIDADE ==============
    
    def listar_dispositivos(self, tipo: Optional[TipoSensor] = None) -> List[DispositivoSensor]:
        """Listar todos os dispositivos ou filtrar por tipo"""
        if tipo:
            return [self.dispositivos[did] for did in self.dispositivos_por_tipo.get(tipo, [])]
        return list(self.dispositivos.values())
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status completo do sistema sensorial"""
        return {
            "nome": self.nome,
            "versao": self.versao,
            "dispositivos": {
                "total": len(self.dispositivos),
                "cameras": len(self.dispositivos_por_tipo[TipoSensor.CAMERA]),
                "microfones": len(self.dispositivos_por_tipo[TipoSensor.MICROFONE]),
                "auto_falantes": len(self.dispositivos_por_tipo[TipoSensor.AUTO_FALANTE])
            },
            "ativos": {
                "camera": self.camera_ativa,
                "microfone": self.microfone_ativo,
                "auto_falante": self.auto_falante_ativo
            },
            "capturando": {
                "video": self._captura_video_ativa,
                "audio": self._captura_audio_ativa
            },
            "metricas": {
                "frames_capturados": self.frames_capturados,
                "amostras_audio": self.amostras_audio_capturadas,
                "falas_reproduzidas": self.falas_reproduzidas
            },
            "bibliotecas_disponiveis": {
                "opencv": OPENCV_AVAILABLE,
                "pyaudio": PYAUDIO_AVAILABLE,
                "sounddevice": SOUNDDEVICE_AVAILABLE,
                "pyttsx3": PYTTSX3_AVAILABLE,
                "gtts": GTTS_AVAILABLE,
                "librosa": LIBROSA_AVAILABLE
            },
            "sistema_operacional": platform.system()
        }
    
    def __del__(self):
        """Destrutor - liberar recursos"""
        self.liberar_camera()
        if self._engine_fala and not isinstance(self._engine_fala, str):
            try:
                self._engine_fala.stop()
            except Exception:
                pass
