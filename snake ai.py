import pygame
import random
from collections import deque
pygame.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
width = 600
height = 600
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake AI')
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 30000
font_style = pygame.font.SysFont("bahnschrift", 25)
def is_safe_move(x, y, snake_body):
    return 0 <= x < width and 0 <= y < height and [x, y] not in snake_body
def bfs_pathfinding(snake_head, snake_body, food):
    directions = [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]
    visited = set()
    queue = deque([(snake_head, [])])
    while queue:
        current_position, path = queue.popleft()
        if current_position == food:
            return path[0] if path else None  # Return the first move
        for move in directions:
            new_position = [current_position[0] + move[0], current_position[1] + move[1]]
            if tuple(new_position) not in visited and is_safe_move(new_position[0], new_position[1], snake_body):
                visited.add(tuple(new_position))
                queue.append((new_position, path + [move]))
    return None
def making_a_decision(snake_head, snake_body, food):
    best_move = bfs_pathfinding(snake_head, snake_body, food)
    if best_move is None:
        directions = [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]
        best_move = None
        min_dist = float('inf')
        for move in directions:
            new_x, new_y = snake_head[0] + move[0], snake_head[1] + move[1]
            if is_safe_move(new_x, new_y, snake_body):
                dist_to_food_sq = (new_x - food[0]) ** 2 + (new_y - food[1]) ** 2  # Squared Euclidean distance
                if dist_to_food_sq < min_dist:
                    min_dist = dist_to_food_sq
                    best_move = move
    return best_move
def display_score(score):
    value = font_style.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
def spawn_food(snake_body):
    while True:
        foodx = random.randint(0, (width - snake_block) // snake_block) * snake_block
        foody = random.randint(0, (height - snake_block) // snake_block) * snake_block
        if [foodx, foody] not in snake_body:
            return foodx, foody
def gameLoop():
    game_over = False
    x1 = width // 2
    y1 = height // 2
    snake_List = [[x1, y1]]
    Length_of_snake = 1
    score = 0
    foodx, foody = spawn_food(snake_List)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        move = making_a_decision([x1, y1], snake_List, [foodx, foody])
        if move is None:
            print('Game Over!')
            game_over = True
            continue
        x1 += move[0]
        y1 += move[1]
        snake_List.insert(0, [x1, y1])
        if len(snake_List) > Length_of_snake:
            del snake_List[-1]
        if x1 == foodx and y1 == foody:
            foodx, foody = spawn_food(snake_List)
            Length_of_snake += 1
            score += 1
        dis.fill(black)
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
        for piece in snake_List:
            pygame.draw.rect(dis, green, [piece[0], piece[1], snake_block, snake_block])
        display_score(score)
        pygame.display.update()
        clock.tick(snake_speed)
    print(f"Final Score: {score}")  # Print the score after the game ends
    pygame.quit()
    quit()
gameLoop()
