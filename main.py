import pygame
import os
import random
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

pygame.init()

WIDTH, HEIGHT = 900, 400
MAIN_COLOR = (165, 184, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (106, 104, 122)
GREEN = (0, 122, 6)
RED = (191, 0, 26)
FONT =  pygame.font.SysFont("Comic Sans MS", 30)
TITLE_FONT = pygame.font.SysFont("Comic Sans MS", 42)
FPS = 60
LEFT_IMAGE_START = 100
RIGHT_IMAGE_START = 576

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Leopard or Jaguar')


def draw_window():
    window.fill(MAIN_COLOR)
    pygame.draw.rect(window, BLACK, pygame.Rect(12, 10, 875, 380), 3, 23)
    pygame.display.update()


def draw_menu(startRect):
    titleText = TITLE_FONT.render("Leopard or Jaguar", True, BLACK)
    startText = FONT.render("Start", True, WHITE)
    
    pygame.draw.rect(window, GRAY, startRect, border_radius=10)
    window.blit(titleText, (282, 107))
    window.blit(startText, (410, 204))
    pygame.display.update()


def draw_leopard(rectangle, leopardImages, index):
    leopardPath = os.path.join("images\AFRICAN LEOPARD", leopardImages[index])
    leopardImage = pygame.image.load(leopardPath)
    window.blit(leopardImage, (rectangle.x, rectangle.y))
    pygame.display.update()

    return leopardPath


def draw_jaguar(rectangle, jaguarImages, index):
    jaguarPath = os.path.join("images\JAGUAR", jaguarImages[index])
    jaguarImage = pygame.image.load(jaguarPath)
    window.blit(jaguarImage, (rectangle.x, rectangle.y))
    pygame.display.update()

    return jaguarPath


def draw_task_text():
    text = FONT.render("Select the Jaguar", True, BLACK)
    window.blit(text, (325, 30))


def check_answer(imagePath):
    """ 
        Takes in the imagePath of the image selected by the user, 
        and validates it against the pretrained ResNet50V2 model. 
        
        Returns True if the image is a JAGUAR
        Returns False otherwise
    """
    classes = ['AFRICAN LEOPARD', 'CARACAL', 'CHEETAH', 'CLOUDED LEOPARD', 'JAGUAR', 'LIONS', 'OCELOT', 'PUMA', 'SNOW LEOPARD', 'TIGER']
    index = [i for i in range(len(classes))]
    indexToClass = dict(zip(index, classes))

    model = load_model('models\\best_resnetmodel_BIGCATS.h5') 

    # Load and preprocess the input image
    img_path = imagePath
    img = cv2.imread(img_path)
    img = tf.keras.applications.resnet_v2.preprocess_input(img)
    # Run inference on the input image
    preds = model.predict(np.array([img]))

    indexPred = np.argmax(preds[0])
    classPred = indexToClass[indexPred]

    if classPred == "JAGUAR":
        draw_result_screen(True)
        return True
    else:
        draw_result_screen(False)
        return False


def draw_result_screen(correct):
    window.fill(MAIN_COLOR)
    if correct:
        resultText = FONT.render("Correct!", True, GREEN)
    else:
        resultText = FONT.render("Wrong!", True, RED)
    window.blit(resultText, (375, 175))
    pygame.display.update()
    pygame.time.delay(2000)


def draw_loading_screen():
    loadingSurface = pygame.Surface((900, 400))
    loadingSurface.set_alpha(128)
    loadingSurface.fill((0, 0, 0))

    loadingText = FONT.render("Checking...", True, WHITE)

    window.blit(loadingSurface, (0,0))
    window.blit(loadingText, (375, 175))
    pygame.display.update()


def draw_score(currentScore, totalScore):
    scoreText = FONT.render(f"{currentScore} / {totalScore}", True, BLACK)
    window.blit(scoreText, (410, 335))
    pygame.display.update()


def update_score(answer, score):
    if answer == True:
        score += 1
    return score


def draw_end(score, total, playAgainRect):
    playAgainText = FONT.render("Play Again", True, WHITE)
    playAgainTextRect = playAgainText.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60))
    pygame.draw.rect(window, GRAY, playAgainRect, border_radius=10)

    percentage = float(score) / total * 100
    scoreText = TITLE_FONT.render(f"{score} / {total}", True, BLACK)
    percentageText = TITLE_FONT.render(f"{percentage:.0f}%", True, BLACK)
    scoreTextRect = scoreText.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
    percentageTextRect = percentageText.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    window.blit(scoreText, scoreTextRect)
    window.blit(percentageText, percentageTextRect)
    window.blit(playAgainText, playAgainTextRect)
    pygame.display.update()


def main():
    gamestate = "menu"
    currentScore = 0
    totalScore = 0

    startButton = pygame.Rect(372, 200, 155, 55)
    playAgainButton = pygame.Rect(420, 200, 155, 55)
    playAgainButton.center = (WIDTH / 2, HEIGHT / 2 + 60)

    leopardImages = os.listdir("images\AFRICAN LEOPARD")
    jaguarImages = os.listdir("images\JAGUAR")
    index = 0

    leftRect = pygame.Rect(LEFT_IMAGE_START, 100, 224, 224)
    rightRect = pygame.Rect(RIGHT_IMAGE_START, 100, 224, 224)
    
    clock = pygame.time.Clock()
    pygame.event.set_blocked(None) # Stop all events from entering the event queue
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN]) # Allow some events into the event queue
    
    rightImagePath = None
    leftImagePath = None

    # Main game loop
    while True:
        clock.tick(FPS) # Limit the game to run at a max framerate

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if gamestate == "play":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if leftRect.collidepoint(x, y):
                    index += 1

                    draw_loading_screen()
                    answer = check_answer(leftImagePath)
                    currentScore = update_score(answer, currentScore)
                    totalScore += 1
                elif rightRect.collidepoint(x, y):
                    index += 1

                    draw_loading_screen()
                    answer = check_answer(rightImagePath)
                    currentScore = update_score(answer, currentScore)
                    totalScore += 1
                else: 
                    continue

            # Ending condition when all images looped through
            if index >= len(jaguarImages):
                gamestate = "end"
                index = 0

            # Update the window
            draw_window()
            pygame.draw.rect(window, BLACK, leftRect.inflate(10, 10), 10, 2)
            pygame.draw.rect(window, BLACK, rightRect.inflate(10, 10), 10, 2)
            draw_task_text()
            draw_score(currentScore, totalScore)

            # Determine what side the jaguar picture will be on
            imageSide = random.choice(["left", "right"])
            if imageSide == "right":
                leftImagePath = draw_leopard(leftRect, leopardImages, index)
                rightImagePath = draw_jaguar(rightRect, jaguarImages, index)
            else:
                rightImagePath = draw_leopard(rightRect, leopardImages, index)
                leftImagePath = draw_jaguar(leftRect, jaguarImages, index)

        if gamestate == "menu":
            draw_window()
            draw_menu(startButton)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if startButton.collidepoint(x, y):
                    gamestate = "play"

                    # Update the window
                    draw_window()
                    pygame.draw.rect(window, BLACK, leftRect.inflate(10, 10), 10, 2)
                    pygame.draw.rect(window, BLACK, rightRect.inflate(10, 10), 10, 2)
                    draw_task_text()
                    draw_score(currentScore, totalScore)

                    # Determine what side the jaguar picture will be on
                    imageSide = random.choice(["left", "right"])
                    if imageSide == "right":
                        leftImagePath = draw_leopard(leftRect, leopardImages, index)
                        rightImagePath = draw_jaguar(rightRect, jaguarImages, index)
                    else:
                        rightImagePath = draw_leopard(rightRect, leopardImages, index)
                        leftImagePath = draw_jaguar(leftRect, jaguarImages, index)
                    

        if gamestate == "end":
            draw_window()
            draw_end(currentScore, totalScore, playAgainButton)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if playAgainButton.collidepoint(x, y):
                    gamestate = "play"
                    currentScore = 0
                    totalScore = 0

                    # Update the window
                    draw_window()
                    pygame.draw.rect(window, BLACK, leftRect.inflate(10, 10), 10, 2)
                    pygame.draw.rect(window, BLACK, rightRect.inflate(10, 10), 10, 2)
                    draw_task_text()
                    draw_score(currentScore, totalScore)

                    # Determine what side the jaguar picture will be on
                    imageSide = random.choice(["left", "right"])
                    if imageSide == "right":
                        leftImagePath = draw_leopard(leftRect, leopardImages, index)
                        rightImagePath = draw_jaguar(rightRect, jaguarImages, index)
                    else:
                        rightImagePath = draw_leopard(rightRect, leopardImages, index)
                        leftImagePath = draw_jaguar(leftRect, jaguarImages, index)
        pygame.event.clear()


    pygame.quit()
    

if __name__ == "__main__":
    main()