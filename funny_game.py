import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
START_SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
FAKE_FOOD_COLOR = "#FF0000"  # تبدأ حمراء
FAKE_FOOD_NEAR_COLOR = "#888888"  # تصبح رمادية عند الاقتراب
BONUS_FOOD_COLOR = "#FFD700"
BG_COLORS = ["#222244", "#224466", "#226688", "#2288AA", "#22AACC", "#22CCEE", "#44FFDD"]
WIN_SCORE = 100

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []

class Food:
    def __init__(self, canvas, snake, color=FOOD_COLOR, tag="food"):
        while True:
            x = random.randint(0, (GAME_WIDTH//SPACE_SIZE)-1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT//SPACE_SIZE)-1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break
        self.coordinates = [x, y]
        self.food = canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=color, tag=tag)
        self.color = color
        self.tag = tag

    def update_color(self, canvas, color):
        self.color = color
        canvas.itemconfig(self.food, fill=color)

def next_turn(snake, food, fake_food, bonus_food):
    global direction, score, speed, bg_index, running, normal_apples_eaten, bonus_food_visible

    if not running:
        return

    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    ate = False

    # أكل التفاح العادي
    if [x, y] == food.coordinates:
        score += 1
        normal_apples_eaten += 1
        ate = True
        canvas.delete("food")
        food.__init__(canvas, snake)
        # إظهار التفاحة الذهبية بعد كل 5 تفاحات عادية
        if normal_apples_eaten % 5 == 0:
            if not bonus_food_visible:
                bonus_food.__init__(canvas, snake, BONUS_FOOD_COLOR, "bonus_food")
                bonus_food_visible = True
    # أكل التفاح الوهمي
    elif [x, y] == fake_food.coordinates:
        canvas.delete("fake_food")
        fake_food.__init__(canvas, snake, FAKE_FOOD_COLOR, "fake_food")
        ate = True  # لا نقاط
    # أكل التفاح الذهبي (تظهر فقط إذا حان وقتها)
    elif bonus_food_visible and [x, y] == bonus_food.coordinates:
        score += 5
        ate = True
        canvas.delete("bonus_food")
        bonus_food_visible = False
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    label.config(text=f"النقاط: {score}")

    # تغيير لون التفاحة الوهمية عند الاقتراب
    fx, fy = fake_food.coordinates
    if abs(x - fx) <= SPACE_SIZE and abs(y - fy) <= SPACE_SIZE:
        fake_food.update_color(canvas, FAKE_FOOD_NEAR_COLOR)
    else:
        fake_food.update_color(canvas, FAKE_FOOD_COLOR)

    # تغيير الخلفية حسب النقاط
    bg_index = min(len(BG_COLORS)-1, score // 15)
    canvas.config(bg=BG_COLORS[bg_index])

    # زيادة السرعة تدريجياً
    speed = max(30, START_SPEED - score)

    if check_collisions(x, y, snake):
        game_over()
    elif score >= WIN_SCORE:
        win_game()
    else:
        root.after(speed, next_turn, snake, food, fake_food, bonus_food)

def change_direction(new_direction):
    global direction
    opposites = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
    if new_direction != opposites.get(direction):
        direction = new_direction

def check_collisions(x, y, snake):
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    if [x, y] in snake.coordinates[1:]:
        return True
    return False

def game_over():
    global running
    running = False
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=('Arial', 24), fill='red', text=f"انتهت اللعبة! نقاطك: {score}")

def win_game():
    global running
    running = False
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=('Arial', 24), fill='gold', text=f"مبروك! فزت! نقاطك: {score}")

def restart_game():
    global score, direction, speed, running, bg_index, normal_apples_eaten, bonus_food_visible
    score = 0
    direction = "right"
    speed = START_SPEED
    bg_index = 0
    running = True
    normal_apples_eaten = 0
    bonus_food_visible = False
    label.config(text=f"النقاط: {score}")
    canvas.config(bg=BG_COLORS[bg_index])
    canvas.delete(tk.ALL)
    snake = Snake()
    for x, y in snake.coordinates:
        square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.append(square)
    food = Food(canvas, snake)
    fake_food = Food(canvas, snake, FAKE_FOOD_COLOR, "fake_food")
    bonus_food = Food(canvas, snake, BONUS_FOOD_COLOR, "bonus_food")
    # لا تظهر التفاحة الذهبية إلا بعد أكل 5 تفاحات عادية
    canvas.delete("bonus_food")
    root.after(speed, next_turn, snake, food, fake_food, bonus_food)

root = tk.Tk()
root.title("لعبة الثعبان")
score = 0
direction = "right"
speed = START_SPEED
bg_index = 0
running = True
normal_apples_eaten = 0
bonus_food_visible = False

label = tk.Label(root, text=f"النقاط: {score}", font=('Arial', 16))
label.pack()

restart_btn = tk.Button(root, text="إعادة اللعب", font=('Arial', 14), command=restart_game)
restart_btn.pack(pady=5)

canvas = tk.Canvas(root, bg=BG_COLORS[bg_index], height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

snake = Snake()
for x, y in snake.coordinates:
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.append(square)

food = Food(canvas, snake)
fake_food = Food(canvas, snake, FAKE_FOOD_COLOR, "fake_food")
bonus_food = Food(canvas, snake, BONUS_FOOD_COLOR, "bonus_food")
canvas.delete("bonus_food")  # لا تظهر في البداية

root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))
root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))

root.after(speed, next_turn, snake, food, fake_food, bonus_food)
root.mainloop()
