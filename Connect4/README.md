# Connect 4
### Práctica Agente Q-Learning

---
En esta práctica se implementó un agente de *Q-Learning en Python*, capaz de aprender a jugar el juego de *Conecta 4*.

El agente se entrena automáticamente mediante múltiples partidas simuladas, y almacena se conocimiento
en archivos *Q-table* en formato JSON, los cuales son utilizados posteriormente para jugar contra el usuario.
---
### Reglas del juego

- El tablero es de 7 columnas x 6 filas.
- Dos jugadores (usuario y CPU) toman turnos soltando fichas.
- En cada turno, se selecciona una columna y la ficha cae a la posición más baja disponible.
- No se puede jugar en columnas llenas.
- El objetivo es conectar *4 fichas* consecutivas:
  - Horizontalmente
  - Verticalmente
  - Diagonalmente
- Si el tablero se llena sin un ganador, el juego termina en empate.
---
### Opciones del menu

- PLAY: Permite iniciar una partida contra la CPU, después de elegir la dificultad.
  - Las diferentes dificultades son simulaciones de comportamiento que se le dió al CPU.
  - Dependiendo de la cantidad de entrenamiento, puede que las dificultades jueguen iguales.
  - Opciones de dificultad:
      - EASY: comportamiento simple.
      - NORMAL: comportamiento balanceado.
      - HARD: comportamiento más analítico.
      - RETURN: regresar al menú anterior.
- SET RNG: Permite modificar el valor de "epsilon", el cual controla la probabilidad de que la CPU realice un movimiento exploratorio/aleatorio (default: 0.1 = 10%).
- EXIT: Cierra el programa.
---
### Estructura del proyecto

- Connect4
  - AI_cpu
    - agent.py
    - config.py
    - game_logic.py
    - train_data.py
  - Data
    - Qtables
      - qtable_easy.json
      - qtable_normal.json
      - qtable_hard.json
    - Reports
      - report_easy_10.json
      - report_easy_1000.json
      - report_easy_10000.json
      - report_normal_10.json
      - report_normal_1000.json
      - report_normal_10000.json
      - report_hard_10.json
      - report_hard_1000.json
      - report_hard_10000.json
    - settings.json
  - UI
    - menus.py
    - theme.py
    - ui_pygame.py
  - main.py
  - main_pygame.py
  - play_terminal.py
  - README.md
---
### Notas

- El agente utiliza *Q-Learning* tabular.
- El aprendizaje se guarda en archivos JSON para ser reutilizados.
- Las dificultades están diseñadas mediante diferentes configuraciones de recompensas, simulando distintos comportamientos de jugadores.
- Debido a la gran cantidad de posibles estados en el juego, el agente puede presentar comportamiento aleatorio en situaciones no vistas durante el entrenamiento.
---
### Como ejecutar el programa

#### Versión completa:
Se puede ejecutar "main_pygame.py" para jugar la versión completa/final.

O También se puede ejecutar con el siguiente comando en la terminal:
>python -m Connect4.main

#### Versión simple en terminal:
Se puede ejecutar "main.py" para jugar una versión sencilla.

Tambien se puede ejecutar con el siguente comando en la terminal:
>python -m Connect4.main_terminal