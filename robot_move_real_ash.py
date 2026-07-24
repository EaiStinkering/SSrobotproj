from sparkybotmini import SparkyBotMini
robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
robot.connect()

m1 = 0
m2 = 0
m3 = 0
m4 = 0
motor_speed = 50
turn_speed = 30
corn_found = False

def robo_movement(movement):
    global m1, m2, m3, m4, corn_found
    move = movement
    if move != "ta" or move!= "no_corn":
        corn_found = True
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
    if move == "x":
        m1 = 0
        m2 = 0
        m3 = 0
        m4 = 0

    #beep
    if move == "b":
        robot.beep()

    robot.set_motor(m1, m2, m3, m4)

quit = False
while True:
    moving_direction = input("direction? ").lower()
    print("forward: w, backward: s, left: a, right: d, top_left: wa, bottom_right: sd , bottom_left: sa, top_right: wd, turn_left: ta, turn_right: td, stop: s")
    if moving_direction.lower() == "q":
        quit == True
        break
    robo_movement(moving_direction)


quit = False
moving_direction = ""
while True:
    
    if moving_direction == "no_corn":
        robo_movement("ta")
        print("look for corn")
        corn_found = False
    
    
    moving_direction = input("direction? ").lower()
    print("forward: w, backward: s, left: a, right: d, top_left: wa, bottom_right: sd , bottom_left: sa, top_right: wd, turn_left: ta, turn_right: td, stop: x")
    if moving_direction.lower() == "q":
        quit == True
        break
    robo_movement(moving_direction)
