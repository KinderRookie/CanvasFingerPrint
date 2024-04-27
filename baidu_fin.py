import numpy as np
import random
import pygame
import pygame.surfarray
import threading

# Initialize Pygame
pygame.init()

def lerp_color(start_color, end_color, t):
    """Linear interpolation between two colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(start_color, end_color))

class Triangle():
    def __init__(self, vertices, color_map):
        self.vertices = vertices
        self.color_map = color_map
        

    def is_inside(self, x, y):
        # Barycentric coordinates for triangle inside check
        
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign((x, y), self.vertices[0], self.vertices[1]) < 0.0
        b2 = sign((x, y), self.vertices[1], self.vertices[2]) < 0.0
        b3 = sign((x, y), self.vertices[2], self.vertices[0]) < 0.0

        return ((b1 == b2) and (b2 == b3))
    
    def flood_fill(self, x, y, screen, z_map, z_index, mode, lock):
        i = 0
        pixel_stack = [(x, y)]
        time = pygame.time.Clock()


        while pixel_stack:
            x, y = pixel_stack.pop()
            if not self.is_inside(x, y) or x<0 or x>=screen.get_width() or y<0 or y>=screen.get_height() or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                continue
            with lock:
                #time.tick(300)
                screen.set_at((x, y), self.color_map[x][y])
                screen.set_at((x-1, y), self.color_map[x][y])
                screen.set_at((x+1, y), self.color_map[x][y])
                screen.set_at((x, y-1), self.color_map[x][y])
                screen.set_at((x, y+1), self.color_map[x][y])

                i += 1
                if i % 10 == 0:
                    pygame.display.update()
            if mode==0: # left up
                elements = [(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
                random.shuffle(elements)
                pixel_stack.extend(elements)
                # pixel_stack.extend([(x, y + 1), (x, y - 1),(x + 1, y), (x - 1, y), (x - 1, y), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)])
            elif mode==1: # right down
                elements = [(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 1), (x - 1, y + 1)]
                random.shuffle(elements)
                pixel_stack.extend(elements)
                # pixel_stack.extend([(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)])
            elif mode==2: # left down
                elements = [(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
                random.shuffle(elements)
                pixel_stack.extend(elements)
                # pixel_stack.extend([(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 1), (x - 1, y + 1)])
            else:
                pixel_stack.extend([(x, y+1),(x, y-1),(x+1,y),(x-1,y),(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)])
class Rectangle():
    def __init__(self, x,y, width, height, color_map):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_map = color_map

    def is_inside(self, x, y, z_map, z_index):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height and z_map[x][y] == z_index
    
    def flood_fill(self, x, y, screen, z_map, z_index, lock):
        i = 0
        pixel_stack = [(x, y)]
        
        rand = random.randint(0, 3)
        while pixel_stack:
            x, y = pixel_stack.pop()
            if not self.is_inside(x, y, z_map, z_index) or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                continue
            with lock:
                screen.set_at((x, y), self.color_map[x][y])
                screen.set_at((x+1, y), self.color_map[x][y])
                screen.set_at((x-1, y), self.color_map[x][y])
                screen.set_at((x, y+1), self.color_map[x][y])
                screen.set_at((x, y-1), self.color_map[x][y])
                i += 1
                if i % 10 == 0:
                    pygame.display.update()
            
            if rand == 0:
                pixel_stack.extend([(x, y + 1), (x, y - 1),(x + 1, y), (x - 1, y), (x - 1, y), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)])
            elif rand == 1:
                pixel_stack.extend([(x, y+1),(x, y-1),(x+1,y),(x-1,y+1),(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 1), (x - 1, y)])
            elif rand == 2:
                pixel_stack.extend([(x, y+1),(x, y-1),(x+1,y),(x-1,y), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1)])
            else:
                pixel_stack.extend([(x, y+1),(x+1,y),(x-1,y),(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),(x + 1, y + 1), (x, y-1)])

background_color = (255, 255, 255)

def main():

    width, height = 900, 1600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Baidu")

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

        # Gradient Setting
        point1 = (300, 259)
        point2 = (300, 1200)
        color1 = (255, 255, 0)  # Yellow
        color2 = (212, 50, 0)  # Orange

        # 두 점 사이의 거리
        distance = np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

        for y in range(height):
            for x in range(width):
                # 현재 픽셀과 point1 사이의 거리
                current_distance = np.sqrt((x - point1[0]) ** 2 + (y - point1[1]) ** 2)
                t = current_distance / distance
                t = min(max(t, 0), 1)  # t를 [0, 1] 범위로 제한
                color_map[x, y] = lerp_color(color1, color2, t)

        pygame.display.flip()

        back = Rectangle(0, 0, width, height, background_map)
        tri = Triangle([(321, 259), (60, 1279), (828, 889)], color_map)

        min_x, min_y = 10000, 10000 # top
        max_x, max_y = 0, 0 # right
        min_xx, min_yy = 10000, 10000 # left

        for i in range(width):
            for j in range(height):
                if tri.is_inside(i, j):
                    z_map[i, j] = z_index

        z_index += 1
        # search for top point
        for i in range(width):
            for j in range(height):
                if z_map[i, j] == 1:
                    if(j < min_y):
                        min_x = i
                        min_y = j
        
        # search for right point
        for i in range(width):
            for j in range(height):
                if z_map[i, j] == 1:
                    if(i > max_x):
                        max_x = i
                        max_y = j

        # search for left point
        for i in range(width):
            for j in range(height):
                if z_map[i, j] == 1:
                    if(i < min_xx):
                        min_xx = i
                        min_yy = j


        back_thread = threading.Thread(target=back.flood_fill, args=(1, 1, screen, z_map, 0, lock))
        back_thread2 = threading.Thread(target=back.flood_fill, args=(width-1, height-1, screen, z_map, 0, lock))
        back_thread3 = threading.Thread(target=back.flood_fill, args=(1, height-1, screen, z_map, 0, lock))
        back_thread4 = threading.Thread(target=back.flood_fill, args=(width-1, 1, screen, z_map, 0, lock))
        tri_thread = threading.Thread(target=tri.flood_fill, args=(min_x, min_y, screen, z_map, 1, 2, lock))
        tri_thread2 = threading.Thread(target=tri.flood_fill, args=(max_x, max_y, screen, z_map, 1, 0 , lock))
        tri_thread3 = threading.Thread(target=tri.flood_fill, args=(min_xx, min_yy, screen, z_map, 1, 0, lock))
        back_thread.start()
        back_thread2.start()
        back_thread3.start()
        back_thread4.start()
        tri_thread.start()
        tri_thread2.start()
        tri_thread3.start()

        back_thread.join()
        back_thread2.join()
        back_thread3.join()
        back_thread4.join()
        tri_thread.join()
        tri_thread2.join()
        tri_thread3.join()


        pygame.display.flip()
        pygame.time.delay(1000)    
        screen.fill((0, 0, 0))

    pygame.quit()


if __name__ == "__main__":
    main()
