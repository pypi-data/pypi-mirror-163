"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""
import os
from turtle import *
from random import randrange
from freegames import square, vector, get_data, set_data, save
from winsound import PlaySound,SND_FILENAME,SND_ASYNC

def randvector():
    return vector(randrange(-17,18)*10, randrange(-17,18)*10)

food = randvector()
snake = [randvector()]
aim = vector(0, -10)
record = get_data("snake",0)

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    "Move snake forward one segment."
    global record
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        PlaySound("sounds\\eat.wav",SND_FILENAME+SND_ASYNC)
        # Update the record
        if record<len(snake):
            record=len(snake)
            set_data("snake", record)
            save()

        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    # draw score and record
    penup()
    color("black")
    goto(130,180)
    write("Score:{}\nRecord: {}".format(
        len(snake),record), font=(None,10))

    update()
    ontimer(move, 100)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()