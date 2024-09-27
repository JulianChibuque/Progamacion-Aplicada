import time
import wifi
import socketpool
import json
import pwmio
import board

# Conéctate al Wi-Fi (usa el SSID y la clave de tu hotspot)
SSID = "ejemplo"
PASSWORD = "12345678"

print("Conectando a la red...")
wifi.radio.connect(SSID, PASSWORD)

# Imprime la dirección IP asignada
print("Conectado a", SSID)
print("Dirección IP:", wifi.radio.ipv4_address)

# Crea un socket de red para el servidor HTTP
pool = socketpool.SocketPool(wifi.radio)
server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server_socket.bind((str(wifi.radio.ipv4_address), 8080))
server_socket.listen(1)
print(f"Servidor corriendo en http://{wifi.radio.ipv4_address}:8080")

# Inicializar PWM para los servos
pwm_1 = pwmio.PWMOut(board.GP0, frequency=50)
pwm_2 = pwmio.PWMOut(board.GP1, frequency=50)
pwm_3 = pwmio.PWMOut(board.GP2, frequency=50)

def set_servo_pulse(pwm, angle):
    # Convierte el ángulo en el ancho del pulso para un servo estándar
    # El rango típico de pulsos es de 500 a 2500 microsegundos (us)
    # Este rango puede variar según el servo que estés usando
    min_pulse = 500    # en microsegundos
    max_pulse = 2500   # en microsegundos
    pulse_width = min_pulse + (angle + 90) * (max_pulse - min_pulse) / 180

    # Convertir microsegundos a duty cycle (65535 es el ciclo completo)
    duty_cycle = int((pulse_width / 20000) * 65535)
    pwm.duty_cycle = duty_cycle

def handle_post_request(request_body):
    try:
        # Procesa el cuerpo de la solicitud POST como JSON
        servo_values = json.loads(request_body)

        # Imprime los valores de los servos recibidos
        print("Valores de los servos recibidos:")
        print("Servo 1:", servo_values.get("servo1"))
        print("Servo 2:", servo_values.get("servo2"))
        print("Servo 3:", servo_values.get("servo3"))

        # Actualiza los pulsos PWM de los servos
        if "servo1" in servo_values:
            set_servo_pulse(pwm_1, servo_values["servo1"])
        if "servo2" in servo_values:
            set_servo_pulse(pwm_2, servo_values["servo2"])
        if "servo3" in servo_values:
            set_servo_pulse(pwm_3, servo_values["servo3"])

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
    except Exception as e:
        print(f"Error al manejar los datos: {e}")

def enviar_por_fragmentos(socket, data, chunk_size=512):
    for i in range(0, len(data), chunk_size):
        fragmento = data[i:i + chunk_size]
        socket.send(fragmento.encode("utf-8"))

        
# Página web más grande que 1KB
pagina_grande = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulación de Brazo Robótico con Joystick</title>
    <style>
        /* Estilo del Joystick */
        #joystickArea {
            width: 200px;
            height: 200px;
            background-color: lightgray;
            border-radius: 50%;
            position: relative;
            margin: 50px auto;
        }

        #joystick {
            width: 50px;
            height: 50px;
            background-color: blue;
            border-radius: 50%;
            position: absolute;
            top: 75px; /* Centrado en el área */
            left: 75px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <h1>Simulación de Brazo Robótico con Joystick Virtual</h1>

    <div>
        <label for="servo1">Ángulo Servo 1: </label>
        <input type="range" id="servo1" min="-90" max="90" value="0">
        <span id="servo1Value">0</span>°
    </div>

    <h2>Joystick Virtual (Control Servos 2 y 3)</h2>
    <div id="joystickArea">
        <div id="joystick"></div>
    </div>

    <div>
        <p>Ángulo Servo 2: <span id="servo2Value">0</span>°</p>
        <p>Ángulo Servo 3: <span id="servo3Value">0</span>°</p>
    </div>

    <div id="container"></div>

    <script>
        // Inicializar la escena de Three.js para el brazo robótico
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const material = new THREE.MeshBasicMaterial({ color: 0x0077ff, wireframe: true });
        
        // Sección 1 del brazo (base)
        const geometry1 = new THREE.BoxGeometry(1, 0.2, 0.2);
        const segment1 = new THREE.Mesh(geometry1, material);
        segment1.position.y = 0.6;
        scene.add(segment1);

        // Sección 2 del brazo (medio)
        const geometry2 = new THREE.BoxGeometry(0.8, 0.2, 0.2);
        const segment2 = new THREE.Mesh(geometry2, material);
        segment2.position.y = 1.2;
        segment1.add(segment2);

        // Sección 3 del brazo (final)
        const geometry3 = new THREE.BoxGeometry(0.6, 0.2, 0.2);
        const segment3 = new THREE.Mesh(geometry3, material);
        segment3.position.y = 0.8;
        segment2.add(segment3);

        camera.position.z = 5;

        // Joystick Virtual
        const joystick = document.getElementById("joystick");
        const joystickArea = document.getElementById("joystickArea");
        const servo1ValueDisplay = document.getElementById("servo1Value");
        const servo2ValueDisplay = document.getElementById("servo2Value");
        const servo3ValueDisplay = document.getElementById("servo3Value");

        const areaRadius = joystickArea.clientWidth / 2;
        const joystickRadius = joystick.clientWidth / 2;

        let isDragging = false;

        // Limitar el movimiento del joystick dentro del círculo
        function limitMovement(x, y) {
            const distance = Math.sqrt(x * x + y * y);
            if (distance > areaRadius - joystickRadius) {
                const angle = Math.atan2(y, x);
                x = (areaRadius - joystickRadius) * Math.cos(angle);
                y = (areaRadius - joystickRadius) * Math.sin(angle);
            }
            return { x, y };
        }

        function updateServoAngles(x, y) {
            // Convertir las coordenadas del joystick en ángulos para los servos
            const maxAngleY = 90;
            const maxAngleX = 45;
            const servo2Angle = (x / (areaRadius - joystickRadius)) * maxAngleX;
            const servo3Angle = -(y / (areaRadius - joystickRadius)) * maxAngleY;

            // Mostrar los valores de los servos
            servo2ValueDisplay.textContent = Math.round(servo2Angle);
            servo3ValueDisplay.textContent = Math.round(servo3Angle);

            // Actualizar las rotaciones de las articulaciones del brazo
            segment2.rotation.z = THREE.Math.degToRad(servo2Angle);
            segment3.rotation.z = THREE.Math.degToRad(servo3Angle);

            // Enviar los valores de los servos a la Raspberry Pi Pico W
            fetch('/update_servos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    servo2: servo2Angle,
                    servo3: servo3Angle
                })
            });
        }

        // Eventos de arrastre del joystick
        joystick.addEventListener("mousedown", () => {
            isDragging = true;
        });

        document.addEventListener("mousemove", (event) => {
            if (!isDragging) return;

            const x = event.clientX - joystickArea.offsetLeft - areaRadius;
            const y = event.clientY - joystickArea.offsetTop - areaRadius;

            const limitedPos = limitMovement(x, y);

            joystick.style.left = `${limitedPos.x + areaRadius - joystickRadius}px`;
            joystick.style.top = `${limitedPos.y + areaRadius - joystickRadius}px`;

            updateServoAngles(limitedPos.x, limitedPos.y);
        });

        document.addEventListener("mouseup", () => {
            isDragging = false;
            // Regresa el joystick al centro
            joystick.style.left = `${areaRadius - joystickRadius}px`;
            joystick.style.top = `${areaRadius - joystickRadius}px`;
            updateServoAngles(0, 0);  // Resetea los ángulos
        });

        // Renderizar la escena del brazo robótico
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexión desde {addr}")

    # Creamos un buffer para leer los datos del cliente
    buffer = bytearray(1024)
    client_socket.recv_into(buffer)

    # Decodifica la solicitud HTTP
    request = buffer.decode("utf-8")
    print(request)

    if "POST /update_servos" in request:
        # Extraer el cuerpo de la solicitud POST
        try:
            request_body = request.split("\r\n\r\n", 1)[1]  # Extrae solo el cuerpo después de los headers
            handle_post_request(request_body)
        except IndexError:
            print("Error: Cuerpo de la solicitud POST no encontrado")
        
    elif "GET" in request:
        # Envía la página web en fragmentos
        response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        client_socket.send(response_header.encode("utf-8"))
        enviar_por_fragmentos(client_socket, pagina_grande)
    
    client_socket.close()


