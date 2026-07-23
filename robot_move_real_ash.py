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
    if move == "w":
        # Forward: all motors forward
        m1 = motor_speed
        m2 = motor_speed
        m3 = motor_speed
        m4 = motor_speed

    if move == "s":
        # Backward: all motors backward
        m1 = -motor_speed
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = -motor_speed

    if move == "a":
        # Left strafe: top-left and back-right backward, top-right and back-left forward
        m1 = -motor_speed
        m2 = motor_speed
        m3 = motor_speed
        m4 = -motor_speed

    if move == "d":
        # Right strafe: top-left and back-right forward, top-right and back-left backward
        m1 = motor_speed
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = motor_speed

    if move == "wa":
        m1 = 0
        m2 = motor_speed
        m3 = motor_speed
        m4 = 0

    if move == "sd":
        m1 = 0
        m2 = -motor_speed
        m3 = -motor_speed
        m4 = 0

    if move == "sa":
        m1 = -motor_speed
        m2 = 0
        m3 = 0
        m4 = -motor_speed

    if move == "wd":
        m1 = motor_speed
        m2 = 0
        m3 = 0
        m4 = motor_speed

    # Handle turning
    if move == "ta":
        # Turn left: counterclockwise rotation
        m1 = -turn_speed
        m2 = -turn_speed
        m3 = turn_speed
        m4 = turn_speed

    if move == "td":
        # Turn right: clockwise rotation
        m1 = turn_speed
        m2 = turn_speed
        m3 = -turn_speed
        m4 = -turn_speed
    #stop
    if move == "s":
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0

    robot.set_motor(m1, m2, m3, m4)

while True:
    moving_direction = input("direction? ").lower()
    print("forward: w, backward: s, left: a, right: d, top_left: wa, bottom_right: sd , bottom_left: sa, top_right: wd, turn_left: ta, turn_right: td, stop: s")
    if moving_direction.lower() == "q":
        break
    robo_movement(moving_direction)


#corn_found = False
#while corn_found == False:
#    if move != "left":
#        robo_movement("left")
