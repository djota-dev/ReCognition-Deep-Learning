import cv2
import mediapipe as mp
import numpy as np
import pyvirtualcam
from PIL import Image, ImageDraw, ImageFont, ImageOps

class SignLanguageTranslator:
    def __init__(self):
        # Configuración de cámara
        self.cam_config = {
            'width': 640,
            'height': 480,
            'fps': 30
        }
        
        # Estado y configuración
        self.current_text = "Acercá tu mano a la cámara"
        self.gesture_history = []
        self.history_length = 5
        self.detection_threshold = 0.8  # Confianza requerida
        
        # Inicializar modelos y recursos
        self.initialize_models()
        self.load_sign_dictionary()
        self.setup_fonts()

    def setup_fonts(self):
        """Configura las fuentes para los subtítulos"""
        try:
            # Intentar cargar una fuente profesional
            self.font = ImageFont.truetype("arialbd.ttf", 36)
            self.small_font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Fuentes de respaldo
            self.font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

    def load_sign_dictionary(self):
        """Diccionario ampliado de señas"""
        self.sign_dict = {
            # Gestos básicos
            "hand_open": "Hola",
            "hand_closed": "Gracias",
            "thumb_up": "Sí",
            "thumb_down": "No",
            "pointing": "Tú/Yo",
            "victory": "Victoria",
            "rock": "Música",
            "ok": "OK/Entendido",
            "phone": "Llamar",
            "money": "Dinero",
            "shaka": "Relajado",
            "ily": "Te quiero",
            "wave": "Adiós"
        }

    def initialize_models(self):
        """Inicializa MediaPipe para detección de manos"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7)
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles

    def get_finger_state(self, landmarks, finger_tip, finger_pip, finger_mcp, wrist):
        """Determina si un dedo está abierto o cerrado"""
        tip_to_wrist = self.calculate_distance(finger_tip, wrist)
        pip_to_wrist = self.calculate_distance(finger_pip, wrist)
        return tip_to_wrist > pip_to_wrist * 1.1

    def calculate_distance(self, point1, point2):

        return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)**0.5

    def detect_complex_gesture(self, hand_landmarks):
     
     
        landmarks = hand_landmarks.landmark
        
        # Puntos clave
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        wrist = landmarks[0]
        
        # Estado de cada dedo
        thumb_open = self.get_finger_state(landmarks, thumb_tip, landmarks[2], landmarks[1], wrist)
        index_open = self.get_finger_state(landmarks, index_tip, landmarks[6], landmarks[5], wrist)
        middle_open = self.get_finger_state(landmarks, middle_tip, landmarks[10], landmarks[9], wrist)
        ring_open = self.get_finger_state(landmarks, ring_tip, landmarks[14], landmarks[13], wrist)
        pinky_open = self.get_finger_state(landmarks, pinky_tip, landmarks[18], landmarks[17], wrist)
        
        # Distancias entre dedos
        thumb_index_dist = self.calculate_distance(thumb_tip, index_tip)
        index_middle_dist = self.calculate_distance(index_tip, middle_tip)
        
        # Determinar gesto (lógica mejorada) hay que ajustar eso che!
        if not any([thumb_open, index_open, middle_open, ring_open, pinky_open]):
            return "hand_closed"
        elif all([index_open, middle_open, not ring_open, not pinky_open]):
            return "victory"
        elif thumb_open and index_open and not middle_open and not ring_open and not pinky_open:
            return "pointing"
        elif not thumb_open and index_open and middle_open and not ring_open and not pinky_open:
            return "rock"
        elif thumb_open and index_open and middle_open and ring_open and pinky_open:
            return "hand_open"
        elif thumb_open and not index_open and not middle_open and not ring_open and not pinky_open:
            return "thumb_up"
        elif not thumb_open and index_open and not middle_open and not ring_open and not pinky_open:
            return "thumb_down"
        elif thumb_open and index_open and middle_open and not ring_open and not pinky_open and thumb_index_dist < 0.1:
            return "ok"
        elif thumb_open and pinky_open and not index_open and not middle_open and not ring_open:
            return "phone"
        elif not thumb_open and index_open and middle_open and ring_open and not pinky_open:
            return "money"
        elif not thumb_open and not index_open and not middle_open and not ring_open and pinky_open:
            return "shaka"
        elif thumb_open and index_open and pinky_open and not middle_open and not ring_open:
            return "ily"
        elif index_open and middle_open and ring_open and pinky_open and not thumb_open:
            return "wave"
        else:
            return "unknown"

    def update_gesture_history(self, gesture):
       
       
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.history_length:
            self.gesture_history.pop(0)
        
       
        if len(self.gesture_history) == self.history_length:
            from collections import Counter
            most_common = Counter(self.gesture_history).most_common(1)[0]
            if most_common[1] >= self.history_length * self.detection_threshold:
                return most_common[0]
        return "unknown"

    def process_frame(self, frame):
        """Procesa un frame para detectar señas"""
        # Convertir a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detección de manos
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Detectar gesto
                gesture = self.detect_complex_gesture(hand_landmarks)
                confirmed_gesture = self.update_gesture_history(gesture)
                
                if confirmed_gesture != "unknown":
                    self.current_text = self.sign_dict.get(confirmed_gesture, "")
                
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.drawing_styles.get_default_hand_landmarks_style(),
                    self.drawing_styles.get_default_hand_connections_style())
        
        else:
            self.current_text = "Acercá tu mano a la cámara"
            self.gesture_history = []
        
        return frame

    def add_youtube_style_subtitles(self, frame):

        if not self.current_text:
            return frame
            
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        
        # Texto principal y secundario
        main_text = self.current_text
        help_text = "Lenguaje de señas en tiempo real"
        
        main_bbox = draw.textbbox((0, 0), main_text, font=self.font)
        help_bbox = draw.textbbox((0, 0), help_text, font=self.small_font)
        
        main_width = main_bbox[2] - main_bbox[0]
        help_width = help_bbox[2] - help_bbox[0]
        
        padding = 20
        x_main = (self.cam_config['width'] - main_width) // 2
        y_main = self.cam_config['height'] - 150
        x_help = (self.cam_config['width'] - help_width) // 2
        y_help = y_main + 50
        
        overlay = Image.new('RGBA', pil_img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        
        draw_overlay.rectangle(
            [(x_main - padding, y_main - padding), 
             (x_main + main_width + padding, y_main + main_bbox[3] - main_bbox[1] + padding)],
            fill=(0, 0, 0, 180))  # Negro semitransparente
        
        draw_overlay.rectangle(
            [(x_help - padding//2, y_help - padding//2),
             (x_help + help_width + padding//2, y_help + help_bbox[3] - help_bbox[1] + padding//2)],
            fill=(0, 0, 0, 120))
        
        pil_img = Image.alpha_composite(pil_img.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(pil_img)
        
        border_width = 2
        
        # Texto principal
        for dx in [-border_width, 0, border_width]:
            for dy in [-border_width, 0, border_width]:
                if dx != 0 or dy != 0:
                    draw.text((x_main + dx, y_main + dy), main_text, 
                             fill=(0, 0, 0, 200), font=self.font)
        
        draw.text((x_main, y_main), main_text, fill=(255, 255, 255), font=self.font)
        
        draw.text((x_help, y_help), help_text, fill=(200, 200, 200), font=self.small_font)
        
        return cv2.cvtColor(np.array(pil_img.convert('RGB')), cv2.COLOR_RGB2BGR)

    def run_videocall(self):
        cap = cv2.VideoCapture(0)
        
        with pyvirtualcam.Camera(
            width=self.cam_config['width'],
            height=self.cam_config['height'],
            fps=self.cam_config['fps']) as vcam:
            
            print(f"Usando cámara virtual: {vcam.device}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Procesar frame
                processed_frame = self.process_frame(frame)
                subtitled_frame = self.add_youtube_style_subtitles(processed_frame)
                
                # Mostrar localmente
                cv2.imshow('Traductor de Lenguaje de Señas', subtitled_frame)
                
                # Enviar a cámara virtual
                vcam.send(cv2.cvtColor(subtitled_frame, cv2.COLOR_BGR2RGB))
                vcam.sleep_until_next_frame()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        
    def run_videocall(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("No se pudo abrir la cámara.")
            return

        with pyvirtualcam.Camera(
            width=self.cam_config['width'],
            height=self.cam_config['height'],
            fps=self.cam_config['fps'],
            print_fps=False
        ) as cam:
            print(f"Cámara virtual iniciada: {cam.device}")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error al capturar el frame.")
                    break

                frame = cv2.resize(frame, (self.cam_config['width'], self.cam_config['height']))

                # Procesar frame
                frame = self.process_frame(frame)
                frame_with_subtitles = self.add_youtube_style_subtitles(frame.copy())

                # Enviar a cámara virtual
                cam.send(frame_with_subtitles)
                cam.sleep_until_next_frame()

                # Mostrar en ventana
                cv2.imshow('Traducción de Señas', frame_with_subtitles)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    translator = SignLanguageTranslator()
    translator.run_videocall()