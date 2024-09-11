import pygame
import random
from collections import deque

# First, Initialize Pygame
pygame.init()

# Let's define the color in our snake ai
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions(Change this if you like)
width = 1600
height = 1000

# Set up our pygame display
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake AI')

# Game clock define as varible clock
clock = pygame.time.Clock()

# Snake settings(Snake_block: size of snake, snake speed:how fast the snake ai moves)
snake_block = 10
snake_speed = 100

# Font settings(You can change the fonts to whatever you like
font_style = pygame.font.SysFont("bahnschrift", 25)

#checking if a move is safe
def is_safe_move(snake_head, move, snake_body):
    next_x = snake_head[0] + move[0]
    next_y = snake_head[1] + move[1]

    # Check if the next move will make a collision
    if next_x >= width or next_x < 0 or next_y >= height or next_y < 0 or [next_x, next_y] in snake_body:
        return False
    return True

# Implementing pathfinding(find safe path)
def bfs_pathfinding(snake_head, snake_body, food):
    directions = [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]
    visited = set()
    queue = deque([(snake_head, [])])

    while queue:
        current_position, path = queue.popleft()
        x, y = current_position

        if current_position == food:
            return path[0] if path else None  # Return the first move

        # Try all four directions
        for move in directions:
            new_x = x + move[0]
            new_y = y + move[1]
            new_position = [new_x, new_y]

            if is_safe_move(current_position, move, snake_body) and tuple(new_position) not in visited:
                visited.add(tuple(new_position))
                queue.append((new_position, path + [move]))

    return None  # No path found that means there is no safe options

#AI decision making choice function with BFS lookahead
def making_a_decision(snake_head, snake_body, food):
    # Try to find a path using BFS
    best_move = bfs_pathfinding(snake_head, snake_body, food)

    # If BFS doesn't find a move, fall back to any safe move
    if best_move is None:
        possible_moves = [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]
        for move in possible_moves:
            if is_safe_move(snake_head, move, snake_body):
                return move

    return best_move

# to display score of the snake ai
def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# GameLoop
def gameLoop():
    game_over = False

    x1 = width / 2
    y1 = height / 2
    snake_List = [[x1, y1]]
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        x1, y1 = snake_List[0]

        # AI decision-making
        move = making_a_decision([x1, y1], snake_List[1:], [foodx, foody])
        if move is None:
            print('Game Over!')
            break

        # Update snake position based on AI move
        x1_change, y1_change = move
        x1 += x1_change
        y1 += y1_change

        snake_List.insert(0, [x1, y1])
        if len(snake_List) > Length_of_snake:
            del snake_List[-1]

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1  # Increase score by 1 when apple is collected

        # Render the game
        dis.fill(black)
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
        for piece in snake_List:
            pygame.draw.rect(dis, green, [piece[0], piece[1], snake_block, snake_block])

        # Display score
        display_score(score)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
