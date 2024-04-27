import numpy as np
import pygame
import random
import threading

# Initialize Pygame
pygame.init()
local_data = threading.local()

def lerp_color(start_color, end_color, t):
    """선형 보간을 사용하여 두 색상 사이를 보간합니다."""
    return tuple(int(a + (b - a) * t) for a, b in zip(start_color, end_color))


def create_circle_mask(center, radius, width, height):
    """원 내부에 있는지를 판단하는 불리언 행렬 생성"""
    x = np.arange(0, width)
    y = np.arange(0, height)
    X, Y = np.meshgrid(x, y)
    
    distance_sq = (X - center[0])**2 + (Y - center[1])**2
    mask = distance_sq <= radius**2
    return mask.transpose()  # X, Y 축 교환하여 반환

def create_triangle_mask(vertices, width, height):
    """삼각형 내부에 있는지를 판단하는 불리언 행렬 생성"""
    # 바리센트릭 좌표 계산 함수
    def barycentric_coords(p, a, b, c):
        v0 = b - a
        v1 = c - a
        v2 = p - a
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d11 = np.dot(v1, v1)
        d20 = np.dot(v2, v0)
        d21 = np.dot(v2, v1)
        denom = d00 * d11 - d01 * d01
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1.0 - v - w
        return u, v, w
    
    x = np.arange(0, width)
    y = np.arange(0, height)
    X, Y = np.meshgrid(x, y)
    
    # 삼각형의 세 꼭짓점
    A, B, C = np.array(vertices[0]), np.array(vertices[1]), np.array(vertices[2])
    
    # 모든 픽셀에 대해 바리센트릭 좌표 계산
    U, V, W = barycentric_coords(np.dstack([X, Y]), A, B, C)
    
    # 바리센트릭 좌표를 사용하여 삼각형 내부에 있는지 판단
    mask = (U >= 0) & (V >= 0) & (W >= 0)
    return mask


class Circle():
    def __init__(self, center, radius, color_map):
        self.center = center
        self.radius = radius
        self.color_map = color_map

    def is_inside(self, x, y):
        return (x - self.center[0]) ** 2 + (y - self.center[1]) ** 2 <= self.radius ** 2
    
    def draw_flood_fill_queue(self, screen, block_size=20):
        screen_array = pygame.surfarray.pixels3d(screen)

        y_start = max(0, self.center[1] - self.radius)
        y_end = min(screen.get_height(), self.center[1] + self.radius)
        x_start = max(0, self.center[0] - self.radius)
        x_end = min(screen.get_width(), self.center[0] + self.radius)

        for y_block in range(y_start, y_end, block_size):
            if(y_block // block_size % 2 == 0):
                x_range = range(x_start, x_end, block_size)
            else:
                x_range = range(x_end - block_size, x_start - block_size, -block_size)
            for x_block in x_range:
                block_pixels = []
                for dy in range(min(block_size, y_end - y_block)):
                    y = y_block + dy
                    row_pixels = []
                    for dx in range(min(block_size, x_end - x_block)):
                        x = x_block + dx
                        if self.is_inside(x, y):
                            row_pixels.append((x, y))
                    
                    if dy % 2 == 1:  # 홀수 번째 행에서는 순서를 뒤집어 지그재그 패턴을 만듭니다.
                        row_pixels.reverse()
                    block_pixels.extend(row_pixels)

                random.shuffle(block_pixels)  # 블록 내의 픽셀 순서를 랜덤하게 섞습니다.
                for x, y in block_pixels:
                        screen_array[x, y] = 0  # 이 부분은 color_map의 적절한 사용 방식에 따라 수정할 수 있습니다.
                        pygame.display.flip()  # 모든 처리가 완료된 후 한 번만 화면을 갱신합니다.

        pygame.display.flip()  # 모든 처리가 완료된 후 한 번만 화면을 갱신합니다.

import pygame
import pygame.surfarray
import numpy as np
import random




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
        clock = pygame.time.Clock()

        while pixel_stack:
            x, y = pixel_stack.pop()
            if not self.is_inside(x, y, z_map, z_index) or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                continue
            with lock:
                clock.tick(60000)
                screen.set_at((x, y), self.color_map[x][y])
                screen.set_at((x-1, y), self.color_map[x][y])
                screen.set_at((x+1, y), self.color_map[x][y])
                screen.set_at((x, y-1), self.color_map[x][y])
                screen.set_at((x, y+1), self.color_map[x][y])
                i += 1
                if i % 40 == 0:
                    pygame.display.update()
                        
            pixel_stack.extend([(x - 1, y), (x, y + 1), (x + 1, y),(x, y - 1),(x - 1, y-1), (x+1, y + 1), (x + 1, y-1),(x+1, y + 1) ,(x - 2, y-2), (x+2, y + 2), (x + 2, y-2),(x+2 , y - 2) ,(x - 2, y), (x, y + 2), (x + 2, y),(x , y - 2),(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),(x + 1, y + 1)])


class Text():
    def __init__(self, text, font_size, color_map, screen):
        self.text = text
        self.font_size = font_size
        self.color_map = color_map
        self.font = pygame.font.Font("/Users/snagreakim/Desktop/SNU/Sm4/web/pj1/coupang/opensans.ttf", size=self.font_size)


        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.center_x = (screen.get_width() - self.text_surface.get_width()) // 2
        self.center_y = (screen.get_height() - self.text_surface.get_height()) // 2
        
        self.screen_array = pygame.surfarray.array3d(screen)




        for y in range(self.text_surface.get_height()):
            for x in range(self.text_surface.get_width()):
                if self.text_surface.get_at((x, y)) == (255, 255, 255):
                    screen_x = self.center_x + x
                    screen_y = self.center_y + y
                    self.screen_array[screen_x, screen_y] = (225, 225, 225)

    def is_inside(self, x, y, screen):
        return self.screen_array[x, y][0] == 225


    def draw(self, x, y, screen, z_map, z_index, lock):
        # Create a font object
        i = 0
        local_data.counter = 0
        pixel_stack = [(x, y)]
        clock = pygame.time.Clock()
        color = (60, 60, 60)

        while pixel_stack:
            
            local_data.counter += 1
            # delay


            x, y = pixel_stack.pop()
            if not self.is_inside(x, y, screen) or screen.get_at((x, y)) != (0, 0, 0) or z_map[x][y] != z_index:
                continue
            clock.tick(300)
            with lock:
                screen.set_at((x, y), color)
                screen.set_at((x-1, y-1), color)
                screen.set_at((x+1, y+1), color)
                screen.set_at((x+1, y-1), color)
                screen.set_at((x-1, y+1), color)
                # screen.set_at((x-1, y), (255, 255, 255))
                # screen.set_at((x+1, y), (255, 255, 255))
                # screen.set_at((x, y-1), (255, 255, 255))
                # screen.set_at((x, y+1), (255, 255, 255))
                i += 1
                if i % 10 == 0:
                    pygame.display.update()
            pixel_stack.extend([(x - 1, y), (x, y + 1), (x + 1, y),(x, y - 1),(x - 1, y-1), (x+1, y + 1), (x + 1, y-1),(x+1, y + 1) ,(x - 2, y-2), (x+2, y + 2), (x + 2, y-2),(x+2 , y - 2) ,(x - 2, y), (x, y + 2), (x + 2, y),(x , y - 2)])


    

background_color = (0, 0, 0)




lock = threading.Lock()

def main():
    width, height = 900, 1600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("flood_fill")
    pygame.time.delay(10000)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)
        z_map = np.zeros((width, height), dtype=np.float32)
        z_index = 1
        color_map = np.full((width, height, 3), (225, 225, 225), dtype=np.uint8)



        back = Rectangle(0, 0, width, height, color_map)
        text = Text('573', 400, color_map, screen=screen)
        
        for i in range(width):
            for j in range(height):
                if text.is_inside(i, j, screen):
                    z_map[i, j] = z_index
                
        back_thread = threading.Thread(target=back.flood_fill, args=(100, 100, screen, z_map, 0, lock))
        back_thread2 = threading.Thread(target=back.flood_fill, args=(600, 10, screen, z_map, 0, lock))
        text_thread = threading.Thread(target=text.draw, args=(191, 680, screen, z_map, 1, lock))
        text_thread2 = threading.Thread(target=text.draw, args=(458, 680, screen, z_map, 1, lock))
        text_thread3 = threading.Thread(target=text.draw, args=(651, 680, screen, z_map, 1, lock))

        back_thread.start()
        back_thread2.start()
        text_thread.start()
        text_thread2.start()
        text_thread3.start()

        back_thread.join()
        back_thread2.join()
        text_thread.join()
        text_thread2.join()
        text_thread3.join()

        pygame.display.flip()
        # pygame.time.delay(1000)
        screen.fill((0, 0, 0))


    pygame.quit()


if __name__ == "__main__":
    main()
