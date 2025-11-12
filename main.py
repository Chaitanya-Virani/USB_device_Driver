import pygame
import random
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BG_COLOR = (18, 18, 25)
GRID_COLOR = (40, 40, 50)
TEXT_COLOR = (200, 200, 200)
HIGHLIGHT = (0, 255, 150)
FAIL_COLOR = (255, 50, 50)

BLOCK_SIZE = 40
GRID_W, GRID_H = 10, 10
GRID_OFFSET_X, GRID_OFFSET_Y = 50, 100

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OS Project: RAM Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 20)
header_font = pygame.font.SysFont('Arial Black', 36)

# --- GAME STATE ---
# 0 means empty. Positive integers are Process IDs.
ram_grid = [0] * (GRID_W * GRID_H)
# Maps Process ID to its color: { pid: (r,g,b) }
process_colors = {}
next_pid = 1
message = "Ready. Spawn a process!"
msg_color = TEXT_COLOR
animating = False

# --- CORE OS FUNCTIONS ---

def spawn_process():
    global next_pid, message, msg_color
    size = random.randint(4, 12)  # Random process size
    color = (random.randint(50, 230), random.randint(50, 230), random.randint(50, 230))

    # FIRST-FIT ALGORITHM
    # Find first sequence of '0's long enough for 'size'
    free_streak = 0
    start_index = -1
    
    for i in range(len(ram_grid)):
        if ram_grid[i] == 0:
            if free_streak == 0: start_index = i
            free_streak += 1
            if free_streak == size:
                # ALLOCATE
                for j in range(start_index, start_index + size):
                    ram_grid[j] = next_pid
                process_colors[next_pid] = color
                message = f"Spawned PID {next_pid} (Size: {size})"
                msg_color = HIGHLIGHT
                next_pid += 1
                return
        else:
            free_streak = 0
    
    # If loop finishes without returning, allocation failed
    message = f"OUT OF MEMORY! Need {size} contiguous blocks."
    msg_color = FAIL_COLOR

def kill_random_process():
    global message, msg_color
    active_pids = list(set(ram_grid))
    if 0 in active_pids: active_pids.remove(0)
    
    if not active_pids: return

    pid_to_kill = random.choice(active_pids)
    # Deallocate
    for i in range(len(ram_grid)):
        if ram_grid[i] == pid_to_kill:
            ram_grid[i] = 0
    
    del process_colors[pid_to_kill]
    message = f"Process {pid_to_kill} terminated. Gaps created."
    msg_color = TEXT_COLOR

def start_compaction():
    # Generator that yields frames for animation
    global ram_grid, animating, message, msg_color
    animating = True
    message = "Compacting Memory..."
    msg_color = HIGHLIGHT
    
    # Bubble sort-esque animation: slide non-zero blocks left one by one
    changed = True
    while changed:
        changed = False
        for i in range(len(ram_grid) - 1):
            # If current is empty (0) and next is occupied (>0), swap them
            if ram_grid[i] == 0 and ram_grid[i+1] != 0:
                ram_grid[i], ram_grid[i+1] = ram_grid[i+1], ram_grid[i]
                changed = True
                yield # Pause here to render this frame
                
    animating = False
    message = "Compaction Complete. Free space merged."
    msg_color = HIGHLIGHT

compaction_gen = None # Holds the active generator

# --- UI COMPONENTS ---
SPAWN_BTN = pygame.Rect(550, 150, 250, 60)
KILL_BTN = pygame.Rect(550, 240, 250, 60)
COMPACT_BTN = pygame.Rect(550, 400, 250, 80)

def draw_button(rect, text, base_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, (255,255,255), rect, 3, border_radius=12)
    
    txt_surf = font.render(text, True, (255,255,255) if rect.collidepoint(mouse_pos) else BG_COLOR)
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)

# --- MAIN LOOP ---
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not animating:
            if SPAWN_BTN.collidepoint(event.pos):
                spawn_process()
            if KILL_BTN.collidepoint(event.pos):
                kill_random_process()
            if COMPACT_BTN.collidepoint(event.pos):
                compaction_gen = start_compaction()
                animating = True

    # 2. Updates & Animation
    if animating and compaction_gen:
        try:
            next(compaction_gen)
            # Slow down animation slightly for visual effect
            pygame.time.delay(20) 
        except StopIteration:
            animating = False
            compaction_gen = None

    # Calculate Stats
    used_blocks = sum(1 for b in ram_grid if b != 0)
    total_blocks = len(ram_grid)
    usage_percent = int((used_blocks / total_blocks) * 100)

    # 3. Drawing
    screen.fill(BG_COLOR)
    
    # Header
    title = header_font.render("RAM Tetris", True, HIGHLIGHT)
    screen.blit(title, (50, 30))
    
    # Draw Grid
    for i in range(GRID_W * GRID_H):
        row = i // GRID_W
        col = i % GRID_W
        x = GRID_OFFSET_X + (col * (BLOCK_SIZE + 2))
        y = GRID_OFFSET_Y + (row * (BLOCK_SIZE + 2))
        
        pid = ram_grid[i]
        color = GRID_COLOR if pid == 0 else process_colors.get(pid, (255,255,255))
        
        pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), border_radius=5)
        
        # Optional: Draw PID on block if it's big enough
        if pid != 0:
            # Only draw PID on the first block of the sequence to avoid clutter
            if i == 0 or ram_grid[i-1] != pid:
                pid_txt = font.render(str(pid), True, (0,0,0))
                screen.blit(pid_txt, (x+5, y+5))

    # Draw UI Panel
    draw_button(SPAWN_BTN, "Spawn Process (+)", HIGHLIGHT, (150, 255, 200))
    draw_button(KILL_BTN, "Kill Random (-)", FAIL_COLOR, (255, 150, 150))
    
    # Compact button (disabled look if animating)
    c_color = (100,100,100) if animating else (50, 150, 255)
    draw_button(COMPACT_BTN, "DEFRAGMENT RAM", c_color, (100, 200, 255))

    # Status Text
    usage_txt = header_font.render(f"Usage: {usage_percent}%", True, TEXT_COLOR)
    screen.blit(usage_txt, (550, 100))
    
    msg_surf = font.render(message, True, msg_color)
    screen.blit(msg_surf, (50, 550))

    pygame.display.flip()
    clock.tick(60)