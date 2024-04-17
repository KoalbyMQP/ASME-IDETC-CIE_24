import pygame
import sys
import ConverseWithFinleyWithActions
import ConverseWithFinley

# Initialize Pygame
pygame.init()

# Create a Pygame window
window_size = (800, 480)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pygame Clickable Buttons')

# Define colors
peach = (255, 182, 155)
dark_peach = (255, 182, 155)
light_peach = (255, 237, 220)
black = (0, 0, 0)
gray = (150, 150, 150)
white = (255, 255, 255)

# Load the font
font = pygame.font.Font("Power Smurf.otf", 36)  # Replace "your_font.ttf" with the path to your font file

# Define button texts
button_texts = ["Speak With Finley", "Control Finley"]

# Calculate button size and position
button_width, button_height = 500, 100
button_spacing = 50
start_y = (window_size[1] - (button_height * 2 + button_spacing)) // 2

buttons = []
for i, text in enumerate(button_texts):
    x = (window_size[0] - button_width) // 2
    y = start_y + (button_height + button_spacing) * i
    buttons.append({"rect": pygame.Rect(x, y, button_width, button_height), "text": text, "hover": False})

# Start the main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    button["hover"] = True
                else:
                    button["hover"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button["rect"].collidepoint(event.pos):
                    if i == 0:
                        ConverseWithFinley.main()
                    elif i == 1:
                        ConverseWithFinleyWithActions.main()

    # Draw buttons
    screen.fill(peach)
    for button in buttons:
        color = gray if button["hover"] else light_peach
        pygame.draw.rect(screen, color, button["rect"])
        pygame.draw.rect(screen, black, button["rect"], 2)

    # Draw button text
    for button in buttons:
        button_text = font.render(button["text"], True, black)
        text_rect = button_text.get_rect(center=button["rect"].center)
        screen.blit(button_text, text_rect)

    pygame.display.flip()