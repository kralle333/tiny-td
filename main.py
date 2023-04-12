import pygame
import consts
from game_controller import GameController
from input_controller import InputController, InputOption


def main():
    pygame.init()

    screen = pygame.display.set_mode((consts.game_width, consts.game_height))
    clock = pygame.time.Clock()

    gc = GameController(50)
    ks = InputController(mapping={
        InputOption.Cancel:     pygame.K_z,
        InputOption.Accept:     pygame.K_x,
        InputOption.Options:    pygame.K_s,
        InputOption.Start:      pygame.K_RETURN,
        InputOption.Select:     pygame.K_RSHIFT,
    })
    running = True
    font = pygame.font.SysFont(None, 24)
    while running:
        clock.tick(60)
        delta_time = clock.get_time()
        screen.fill((0, 0, 0))
        ks.set_keys()
        gc.update(delta_time, ks)

        gc.draw(screen)
        img = font.render(f'Fps: {clock.get_fps()}', True, (200,100,200))
        screen.blit(img, (20, 50))

        ks.set_prev()
        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


if __name__ == '__main__':
    main()
