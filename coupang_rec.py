import numpy as np
import random
import pygame
import pygame.surfarray
import threading

# Initialize Pygame
pygame.init()




class Rectangle():
    def __init__(self, x,y, width, height, color_map):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_map = color_map
    
    def is_inside(self, x, y, z_map, z_index):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height and z_map[x][y] == z_index
    
    def is_insides(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height
    

    def flood_fill(self, x, y, screen, z_map, z_index, lock, num_of_pixel = 10):
        i = 0
        pixel_stack = [(x, y)]
        mode = random.randint(0, 3)
        clock = pygame.time.Clock()


        while pixel_stack:
            x, y = pixel_stack.pop()
            if not self.is_inside(x, y, z_map, z_index) or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                mode = (mode + 1)%4
                continue
            with lock:
                clock.tick(6000)
                screen.set_at((x, y), self.color_map[x][y])
                screen.set_at((x+1, y), self.color_map[x][y])
                screen.set_at((x, y-1), self.color_map[x][y])
                screen.set_at((x, y+1), self.color_map[x][y])
                screen.set_at((x-1, y), self.color_map[x][y])
                screen.set_at((x+1, y+1), self.color_map[x][y])
                screen.set_at((x+1, y-1), self.color_map[x][y])
                screen.set_at((x-1, y+1), self.color_map[x][y])
                screen.set_at((x-1, y-1), self.color_map[x][y])

                i += 1
                if i % num_of_pixel == 0:
                    pygame.display.update()
            way_LEFT = [(x, y+2),(x, y-2),(x+2,y),(x-2,y)]
            way_RIGHT = [(x, y+2),(x, y-2),(x-2,y),(x+2,y)]
            way_UP = [(x-2, y),(x, y+2),(x+2,y),(x,y-2)]
            way_DOWN = [(x-2, y),(x, y-2),(x+2,y),(x,y+2)]
            # way_LEFT_UP = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x-1, y - 1), (x - 1, y + 1)]
            # way_RIGHT_DOWN = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x + 1, y - 1), (x + 1, y + 1)]
            # way_LEFT_DOWN = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x - 1, y - 1), (x + 1, y - 1)]
            # way_RIGHT_UP = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x + 1, y + 1), (x - 1, y - 1)]
            way_LEFT_UP = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x-2, y - 2), (x - 2, y + 2)]
            way_RIGHT_DOWN = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x + 2, y - 2), (x + 2, y + 2)]
            way_LEFT_DOWN = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x - 2, y - 2), (x + 2, y - 2)]
            way_RIGHT_UP = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x + 2, y + 2), (x - 2, y - 2)]
        
            
            modes = [way_LEFT, way_RIGHT, way_UP, way_DOWN]
            #modes = [way_LEFT_UP, way_RIGHT_DOWN, way_LEFT_DOWN, way_RIGHT_UP]

            # if i % 2400 == 1:
            #     mode = random.randint(0, 3)

            pixel_stack.extend(modes[mode])
    def flood_fill_2(self, x, y, screen, z_map, z_index, lock, num_of_pixel = 10):
        i = 0
        pixel_stack = [(x, y)]
        mode = 0
        clock = pygame.time.Clock()


        while pixel_stack:
            x, y = pixel_stack.pop()
            if not self.is_inside(x, y, z_map, z_index) or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                continue
            with lock:
                clock.tick(6000)
                screen.set_at((x, y), self.color_map[x][y])
                screen.set_at((x+1, y), self.color_map[x][y])
                screen.set_at((x, y-1), self.color_map[x][y])
                screen.set_at((x, y+1), self.color_map[x][y])
                screen.set_at((x-1, y), self.color_map[x][y])
                screen.set_at((x+1, y+1), self.color_map[x][y])
                screen.set_at((x+1, y-1), self.color_map[x][y])
                screen.set_at((x-1, y+1), self.color_map[x][y])
                screen.set_at((x-1, y-1), self.color_map[x][y])

                i += 1
                if i % num_of_pixel == 0:
                    pygame.display.update()
            way_LEFT = [(x, y+1),(x, y-1),(x+1,y),(x-1,y)]
            way_RIGHT = [(x, y+1),(x, y-1),(x-1,y),(x+1,y)]
            way_UP = [(x-1, y),(x, y+1),(x+1,y),(x,y-1)]
            way_DOWN = [(x-1, y),(x, y-1),(x+1,y),(x,y+1)]
            # way_LEFT_UP = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x-1, y - 1), (x - 1, y + 1)]
            # way_RIGHT_DOWN = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x + 1, y - 1), (x + 1, y + 1)]
            # way_LEFT_DOWN = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x - 1, y - 1), (x + 1, y - 1)]
            # way_RIGHT_UP = [(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x + 1, y + 1), (x - 1, y - 1)]
            way_LEFT_UP = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x-2, y - 2), (x - 2, y + 2)]
            way_RIGHT_DOWN = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x + 2, y - 2), (x + 2, y + 2)]
            way_LEFT_DOWN = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x - 2, y - 2), (x + 2, y - 2)]
            way_RIGHT_UP = [(x, y+2),(x, y-2),(x+2,y),(x-2,y), (x + 2, y + 2), (x - 2, y - 2)]
        
            
            modes = [way_LEFT, way_RIGHT, way_UP, way_DOWN]
            # modes = [way_LEFT_UP, way_RIGHT_DOWN, way_LEFT_DOWN, way_RIGHT_UP]

            if i % 2400 == 1:
                mode = random.randint(0, 3)

            pixel_stack.extend(modes[mode])
background_color = (255, 255, 255)

def main():
    width, height = 900, 1600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Coupang")
    pygame.time.delay(1000)
    running = True

    lock = threading.Lock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Create a circle and set a color map
        color_map = np.zeros((width, height, 3), dtype=np.uint8)
        background_map = np.full((width, height, 3), background_color, dtype=np.uint8)
        z_map = np.zeros((width, height), dtype=np.float32)
        z_index = 1

        red_map = np.full((width, height, 3), [255, 0, 0], dtype=np.uint8)
        grey_map = np.full((width, height, 3), [128, 128, 128], dtype=np.uint8)
        blue_map = np.full((width, height, 3), [0, 0, 255], dtype=np.uint8)

        
        pygame.display.flip()
        back = Rectangle(0, 0, width, height, background_map)
        rec1 = Rectangle(54, 387, 533, 826, grey_map)
        rec2 = Rectangle(54, 387, 263, 414, red_map)
        rec3 = Rectangle(587, 387, 258, 278, blue_map)


        for i in range(width): # z_index = 1
            for j in range(height):
                if rec1.is_insides(i, j):
                    z_map[i, j] = 1
        
        for i in range(width): # z_index = 2
            for j in range(height):
                if rec2.is_insides(i, j):
                    z_map[i, j] = 2

        for i in range(width): # z_index = 3
            for j in range(height):
                if rec3.is_insides(i, j):
                    z_map[i, j] = 3

        # make delay 1000ms
        pygame.time.delay(1000)



        back_pixels = 80
        back_thread = threading.Thread(target=back.flood_fill, args=(10, 20, screen, z_map, 0, lock, back_pixels))
        back_thread2 = threading.Thread(target=back.flood_fill, args=(width-2, height-2, screen, z_map, 0, lock, back_pixels))
        back_thread3 = threading.Thread(target=back.flood_fill, args=(width-1, height-1, screen, z_map, 0, lock, back_pixels))
        back_thread4 = threading.Thread(target=back.flood_fill, args=(1, 1, screen, z_map, 0, lock, back_pixels))
        back_thread5 = threading.Thread(target=back.flood_fill, args=(100, height-1, screen, z_map, 0, lock, back_pixels))
        rec1_thread = threading.Thread(target=rec1.flood_fill, args=(429, 549, screen, z_map, 1, lock))
        rec1_thread2 = threading.Thread(target=rec1.flood_fill, args=(231, 965, screen, z_map, 1, lock))
        rec2_thread = threading.Thread(target=rec2.flood_fill, args=(146, 497, screen, z_map, 2, lock))
        rec3_thread = threading.Thread(target=rec3.flood_fill, args=(672, 542, screen, z_map, 3, lock))
        
        
        back_thread.start()
        back_thread2.start()
        back_thread3.start()
        back_thread4.start()
        back_thread5.start()
        rec1_thread.start()
        rec1_thread2.start()
        rec2_thread.start()
        rec3_thread.start()



        back_thread.join()
        back_thread2.join()
        back_thread3.join()
        back_thread4.join()
        back_thread5.join()
        rec1_thread.join()
        rec1_thread2.join()
        rec2_thread.join()
        rec3_thread.join()


        pygame.display.flip() 

        pygame.time.delay(1000)   
        screen.fill((0, 0, 0))

    pygame.quit()


if __name__ == "__main__":
    main()
