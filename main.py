import pygame
import pygame.gfxdraw
import time
import math


def drawFilledCircle(window, colour: tuple, center: tuple, radius):
    pygame.gfxdraw.aacircle(window, int(
        center[0]), int(center[1]), radius, colour)
    for x in range(radius):
        pygame.gfxdraw.filled_circle(window, int(
            center[0]), int(center[1]), radius, colour)
        # pygame.draw.circle(window, colour, center, radius-x, 2)


def getPointsOnCircle(radius, angle, Center: tuple):
    LocalX = int((radius * math.cos(math.radians(angle) - math.pi/2)))
    LocalY = int((radius * math.sin(math.radians(angle) - math.pi/2)))
    return (Center[0] + LocalX, Center[1] + LocalY)


# Constants
background_colour = (20, 20, 30)
CircleBlue = (100, 190, 230)
PolygonColour = (230, 30, 30)
ClockColour = (225, 225, 225)
rotationSpeed = 150
arcDistance = 0.95

CircleRadius = 300
FontSize = 50

circlebreathingSpeed = 20
OuterBreathingDistance = math.floor(CircleRadius * 0.005)

SecondRadius = CircleRadius * 0.02
MinuteRadius = CircleRadius * 0.04
HourRadius = CircleRadius * 0.06

segments = 60
inner = 2


SCREEN_SIZE = (1900, 1000)
FPS = 300
Center = (int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2))
window = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

Center = (int(pygame.display.get_window_size()[0]/2), int(pygame.display.get_window_size()[1]/2))
SCREEN_SIZE = pygame.display.get_window_size()

# Main loop
running = True
pygame.init()
Clock = pygame.time.Clock()
pygame.display.set_caption('Clock')
window.fill(background_colour)
arcDisplacement = 0
arcRadisuDisplacement = 0


while running:
    dt = Clock.tick(FPS) / 1000
    arcDisplacement += 0.1 * rotationSpeed * dt
    arcRadisuDisplacement += (circlebreathingSpeed * dt)
    arcRadisuDisplacement %= 360
    seconds = float(time.time() % (24 * 3600))
    minutes = float(time.time() % 3600 // 60)
    hours = float(seconds // 3600)

    MaxMinute = 60
    MaxHour = 12
    MaxSecond = 60

    trueHour = hours

    if hours > 12:
        hours -= 12

    # print(f"H:{hours} M:{minutes} S:{seconds}")

    Coords = []
   # Center of the screen
    CurrentAngle = ((seconds / MaxSecond) * 360,
                    (minutes/MaxMinute)*360, (hours/MaxHour)*360)

    for i in range(3):

        LocalX = (((CircleRadius*0.9)) *
                  math.cos(math.radians(CurrentAngle[i]) - math.pi/2))
        LocalY = ((CircleRadius*0.9) *
                  math.sin(math.radians(CurrentAngle[i]) - math.pi/2))

        Coords.append([Center[0] + LocalX, Center[1] + LocalY])

    # Draw Loop
    window.fill(background_colour)

    distanceChange = abs(int(math.degrees(
        math.sin(math.radians(arcRadisuDisplacement))) * OuterBreathingDistance))

    print(f"{str(distanceChange)}: {str(arcRadisuDisplacement)} : {str(math.radians(arcRadisuDisplacement))} : {str(math.degrees(math.sin(math.radians(arcRadisuDisplacement))))}")

    for x in range(segments):
        pygame.gfxdraw.arc(window, Center[0], Center[1], int((CircleRadius * arcDistance)) + distanceChange, int(
            ((360/segments)*x) + arcDisplacement) + inner, int(((360/segments)*(x+1)) + arcDisplacement), ClockColour)

    drawFilledCircle(window, background_colour, Center, CircleRadius)

    pygame.gfxdraw.aapolygon(window, Coords, PolygonColour)
    pygame.gfxdraw.filled_polygon(window, Coords, PolygonColour)

    pygame.gfxdraw.aacircle(
        window, Center[0], Center[1], CircleRadius, ClockColour)
    pygame.gfxdraw.aacircle(
        window, Center[0], Center[1], CircleRadius-1, ClockColour)

    # pygame.draw.circle(window, (200,200,200), (500, 500), 380, 20)
    # pygame.draw.circle(window, (150,150,150), (500, 500), 360, 20)

    # pygame.draw.line(window, (255,0,0), Center, Coords[0], 1)
    # pygame.draw.line(window, (0,255,0), Center, Coords[1], 1)
    # pygame.draw.line(window, (0,0,255), Center, Coords[2], 1)

    # pygame.gfxdraw.line(window, int(Coords[0][0]), int(Coords[0][1]), Center[0], Center[1], ClockColour)
    # pygame.gfxdraw.line(window, int(Coords[1][0]), int(Coords[1][1]), Center[0], Center[1], ClockColour)
    # pygame.gfxdraw.line(window, int(Coords[2][0]), int(Coords[2][1]), Center[0], Center[1], ClockColour)

    for x in range(12):
        StartPos = getPointsOnCircle(CircleRadius-10, (360/12)*x, Center)
        EndPos = getPointsOnCircle(CircleRadius, (360/12)*x, Center)
        pygame.gfxdraw.line(
            window, StartPos[0], StartPos[1], EndPos[0], EndPos[1], ClockColour)

    drawFilledCircle(window, background_colour, Coords[2], int(HourRadius) + 3)
    drawFilledCircle(window, CircleBlue, Coords[2], int(HourRadius))

    drawFilledCircle(window, background_colour,
                     Coords[1], int(MinuteRadius) + 3)
    drawFilledCircle(window, CircleBlue, Coords[1], int(MinuteRadius))

    drawFilledCircle(window, background_colour, Coords[0], int(SecondRadius)+3)
    drawFilledCircle(window, CircleBlue, Coords[0], int(SecondRadius))

    strseconds = ""
    if math.floor(seconds % 60) < 10:
        strseconds = str("0" + str(math.floor(seconds % 60)))
    else:
        strseconds = str(math.floor(seconds % 60))

    pygame.font.init()
    font = pygame.font.SysFont('ARIAL.TTF', FontSize)
    font.set_italic(True)
    TimeText = font.render(str(
        f"{math.floor(trueHour)} : {math.floor(minutes)} : {strseconds}"), True, (255, 255, 255))
    FPStext = font.render(
        str(f"{int(Clock.get_fps())}"), True, (255, 255, 255))
    window.blit(FPStext, (5, 5))
    window.blit(
        TimeText, (Center[0] - TimeText.get_width()/2, Center[1] - TimeText.get_height()/2))

    pygame.display.update()

    # Event Loop
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?

        # Did the user click the window close button? If so, stop the loop.
        if event.type == pygame.QUIT:
            running = False
