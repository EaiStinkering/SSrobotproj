from sparkybotmini import SparkyBotMini
robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
robot.connect()

m1 = 0
m2 = 0
m3 = 0
m4 = 0
motor_speed = 50
turn_speed = 30


def robo_movement(movement):
    global m1, m2, m3, m4
    move = movement
    if move == "forward":
        # Forward: all motors forward
        m1 = motor_speed
        m2 = motor_speed
        m3 = motor_speed
        m4 = motor_speed

    if move == "backward":
        # Backward: all motors backward
        m1 = -motor_speed
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = -motor_speed

    if move == "left":
        # Left strafe: top-left and back-right backward, top-right and back-left forward
        m1 = -motor_speed
        m2 = motor_speed
        m3 = motor_speed
        m4 = -motor_speed

    if move == "right":
        # Right strafe: top-left and back-right forward, top-right and back-left backward
        m1 = motor_speed
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = motor_speed

    if move == "top_left":
        m1 = 0
        m2 = motor_speed
        m3 = motor_speed
        m4 = 0

    if move == "bottom_right":
        m1 = 0
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = 0

    if move == "bottom_left":
        m1 = -motor_speed
        m2 = 0
        m3 = 0
        m4 = -motor_speed

    if move == "top_right":
        m1 = motor_speed
        m2 = 0
        m3 = 0
        m4 = motor_speed

    # Handle turning
    if move == "turn_left":
        # Turn left: counterclockwise rotation
        m1 = -turn_speed
        m2 = -turn_speed
        m3 = turn_speed
        m4 = turn_speed

    if move == "turn_right":
        # Turn right: clockwise rotation
        m1 = turn_speed
        m2 = turn_speed
        m3 = -turn_speed
        m4 = -turn_speed
    #stop
    if move == "stop":
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0

    robot.set_motor(m1, m2, m3, m4)

while True:
    moving_direction = input("direction? ").lower()
    print("forward, backward, left, right, top_left, bottom_right, bottom_left, top_right, turn_left, turn_right")
    if moving_direction.lower() == "q":
        break
    robo_movement(moving_direction)


#corn_found = False
#while corn_found == False:
#    if move != "left":
#        robo_movement("left")
