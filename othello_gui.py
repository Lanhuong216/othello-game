import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import subprocess
import threading
import socket
import copy
import timeit
import time
import importlib
from board import Board, move_string

def get_local_ip():
    """ Get local IP address. """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def show_1player_menu():
    """ Show 1 player menu (engine selection). """
    # Clear current frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Title
    label = tb.Label(main_frame, text="1 Player Mode", font=TITLE_FONT, bootstyle="info")
    label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Back button
    back_btn = tb.Button(main_frame, text="← Back", command=show_main_menu, bootstyle="secondary")
    back_btn.grid(row=0, column=2, sticky="e", pady=(0, 20))
    
    engines = ["human", "minimax", "alpha", "random", "greedy"]
    black_var = tb.StringVar(value="human")
    white_var = tb.StringVar(value="minimax")
    
    tb.Label(main_frame, text="Black Engine:").grid(row=1, column=0, sticky="w", pady=6)
    tb.Combobox(main_frame, textvariable=black_var, values=engines, state="readonly", width=20).grid(row=1, column=1, sticky="ew", pady=6)
    
    tb.Label(main_frame, text="White Engine:").grid(row=2, column=0, sticky="w", pady=6)
    tb.Combobox(main_frame, textvariable=white_var, values=engines, state="readonly", width=20).grid(row=2, column=1, sticky="ew", pady=6)
    
    ab_b_var = tb.BooleanVar()
    ab_w_var = tb.BooleanVar()
    tb.Checkbutton(main_frame, text="Black Alpha-Beta", variable=ab_b_var).grid(row=3, column=0, sticky="w", pady=6)
    tb.Checkbutton(main_frame, text="White Alpha-Beta", variable=ab_w_var).grid(row=3, column=1, sticky="w", pady=6)
    
    verbose_var = tb.BooleanVar(value=True)
    tb.Checkbutton(main_frame, text="Verbose Output", variable=verbose_var).grid(row=4, column=0, sticky="w", pady=6)
    
    time_var = tb.IntVar(value=300)
    tb.Label(main_frame, text="Time Limit (s):").grid(row=5, column=0, sticky="w", pady=6)
    tb.Entry(main_frame, textvariable=time_var, width=20).grid(row=5, column=1, sticky="ew", pady=6)
    
    level_b_var = tb.IntVar(value=4)
    level_w_var = tb.IntVar(value=4)
    tb.Label(main_frame, text="Black Level:").grid(row=6, column=0, sticky="w", pady=6)
    tb.Entry(main_frame, textvariable=level_b_var, width=20).grid(row=6, column=1, sticky="ew", pady=6)
    tb.Label(main_frame, text="White Level:").grid(row=7, column=0, sticky="w", pady=6)
    tb.Entry(main_frame, textvariable=level_w_var, width=20).grid(row=7, column=1, sticky="ew", pady=6)
    
    dup_var = tb.IntVar(value=1)
    tb.Label(main_frame, text="Repeat Count:").grid(row=8, column=0, sticky="w", pady=6)
    tb.Entry(main_frame, textvariable=dup_var, width=20).grid(row=8, column=1, sticky="ew", pady=6)
    
    status_var = tb.StringVar(value="Idle")
    tb.Label(main_frame, textvariable=status_var, bootstyle="secondary").grid(
        row=9, column=0, columnspan=2, pady=(12, 4))
    
    def launch_1player():
        black = black_var.get()
        white = white_var.get()
        time_limit = time_var.get()
        level_b = level_b_var.get()
        level_w = level_w_var.get()
        
        # Open game window
        show_game_window(
            black_engine=black,
            white_engine=white,
            game_time=time_limit,
            level_b=level_b,
            level_w=level_w,
            ab_b=ab_b_var.get(),
            ab_w=ab_w_var.get(),
            verbose=verbose_var.get()
        )
    
    tb.Button(main_frame, text="▶ Play Game", command=launch_1player, bootstyle="primary").grid(
        row=10, column=0, columnspan=2, pady=14, ipadx=10, ipady=4)
    
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)

def show_2player_menu():
    """ Show 2 player menu (network mode). """
    # Clear current frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Title
    label = tb.Label(main_frame, text="2 Players Mode (Network)", font=TITLE_FONT, bootstyle="info")
    label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Back button
    back_btn = tb.Button(main_frame, text="← Back", command=show_main_menu, bootstyle="secondary")
    back_btn.grid(row=0, column=2, sticky="e", pady=(0, 20))
    
    # Color selection
    color_var = tb.StringVar(value="black")
    tb.Label(main_frame, text="Your Color:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=10)
    
    color_frame = tb.Frame(main_frame)
    color_frame.grid(row=1, column=1, sticky="ew", pady=10)
    
    tb.Radiobutton(color_frame, text="Black (Server)", variable=color_var, value="black", 
                   bootstyle="info-toolbutton").pack(side="left", padx=10)
    tb.Radiobutton(color_frame, text="White (Client)", variable=color_var, value="white", 
                   bootstyle="info-toolbutton").pack(side="left", padx=10)
    
    # Network settings
    host_var = tb.StringVar(value="10.229.53.168")
    port_var = tb.IntVar(value=12345)
    
    tb.Label(main_frame, text="Server IP:").grid(row=2, column=0, sticky="w", pady=6)
    host_entry = tb.Entry(main_frame, textvariable=host_var, width=25)
    host_entry.grid(row=2, column=1, sticky="ew", pady=6)
    
    tb.Label(main_frame, text="Port:").grid(row=3, column=0, sticky="w", pady=6)
    port_entry = tb.Entry(main_frame, textvariable=port_var, width=25)
    port_entry.grid(row=3, column=1, sticky="ew", pady=6)
    
    # Info label
    info_text = tb.StringVar()
    info_label = tb.Label(main_frame, textvariable=info_text, bootstyle="secondary", wraplength=400)
    info_label.grid(row=4, column=0, columnspan=2, pady=10)
    
    def update_info():
        """ Update info text based on color selection. """
        if color_var.get() == "black":
            local_ip = get_local_ip()
            info_text.set(f"Server Mode - Your IP: {local_ip}\nShare this IP with your opponent.\nWaiting for client to connect...")
            host_entry.config(state="disabled")
        else:
            info_text.set(f"Client Mode - Connecting to server at {host_var.get()}:{port_var.get()}")
            host_entry.config(state="normal")
    
    color_var.trace("w", lambda *args: update_info())
    update_info()
    
    verbose_var = tb.BooleanVar(value=True)
    tb.Checkbutton(main_frame, text="Verbose Output", variable=verbose_var).grid(row=5, column=0, sticky="w", pady=6)
    
    time_var = tb.IntVar(value=300)
    tb.Label(main_frame, text="Time Limit (s):").grid(row=6, column=0, sticky="w", pady=6)
    tb.Entry(main_frame, textvariable=time_var, width=25).grid(row=6, column=1, sticky="ew", pady=6)
    
    status_var = tb.StringVar(value="Idle")
    tb.Label(main_frame, textvariable=status_var, bootstyle="secondary").grid(
        row=7, column=0, columnspan=2, pady=(12, 4))
    
    # Button text changes based on color selection
    button_text_var = tb.StringVar(value="▶ Join")
    start_button = tb.Button(main_frame, textvariable=button_text_var, bootstyle="success")
    start_button.grid(row=8, column=0, columnspan=2, pady=14, ipadx=10, ipady=4)
    
    def update_button_text():
        """ Update button text based on color selection. """
        if color_var.get() == "black":
            button_text_var.set("▶ Join")
            start_button.config(bootstyle="success")
        else:
            button_text_var.set("▶ Start Game")
            start_button.config(bootstyle="success")
    
    color_var.trace("w", lambda *args: update_button_text())
    update_button_text()
    
    def launch_2player():
        color = color_var.get()
        host = host_var.get()
        port = port_var.get()
        time_limit = time_var.get()
        
        if color == "black":
            # Server mode - Join button
            status_var.set("Setting up server...")
            # Open game window immediately for server
            show_game_window(
                black_engine="network_server",
                white_engine="network_receiver",
                game_time=time_limit,
                network_mode=True,
                is_server=True,
                host='0.0.0.0',
                port=port
            )
        else:
            # Client mode - Start Game button
            status_var.set("Connecting to server...")
            # Open game window for client (will connect when initializing)
            show_game_window(
                black_engine="network_receiver",
                white_engine="network_client",
                game_time=time_limit,
                network_mode=True,
                is_server=False,
                host=host,
                port=port
            )
    
    start_button.config(command=launch_2player)
    
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2)
    main_frame.columnconfigure(2, weight=1)

def show_main_menu():
    """ Show main menu with 1player and 2players options. """
    # Clear current frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Title
    label = tb.Label(main_frame, text="Othello Game Launcher", font=TITLE_FONT, bootstyle="info")
    label.grid(row=0, column=0, columnspan=2, pady=(20, 40))
    
    # 1 Player button
    btn_1player = tb.Button(main_frame, text="1 Player", command=show_1player_menu, 
                            bootstyle="primary", width=20)
    btn_1player.grid(row=1, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
    
    # 2 Players button
    btn_2players = tb.Button(main_frame, text="2 Players (Network)", command=show_2player_menu, 
                            bootstyle="success", width=20)
    btn_2players.grid(row=2, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
    
    # Info label
    info_label = tb.Label(main_frame, text="Select game mode to start", bootstyle="secondary")
    info_label.grid(row=3, column=0, columnspan=2, pady=(30, 0))
    
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

# === Game Window Constants ===
CELL_SIZE = 60
PIECE_RADIUS = 25
BOARD_SIZE = 8
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE

def draw_board(canvas):
    """ Draw the board grid. """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='#2cb87b', width=2)

def update_ui(canvas, board):
    """ Update the board display. """
    canvas.delete("piece")
    canvas.delete("hint")
    
    # Board is accessed as board[x][y] where x is column (0-7), y is row (0-7)
    # Board y=0 is bottom row, canvas y=0 is top row, so we need to flip
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell = board[col][row]  # board[x][y]
            canvas_x = col * CELL_SIZE + CELL_SIZE // 2
            canvas_y = (7 - row) * CELL_SIZE + CELL_SIZE // 2  # Flip y coordinate
            
            if cell == 1:  # White piece
                canvas.create_oval(
                    canvas_x - PIECE_RADIUS, canvas_y - PIECE_RADIUS,
                    canvas_x + PIECE_RADIUS, canvas_y + PIECE_RADIUS,
                    fill='white', outline='black', width=2, tags="piece"
                )
            elif cell == -1:  # Black piece
                canvas.create_oval(
                    canvas_x - PIECE_RADIUS, canvas_y - PIECE_RADIUS,
                    canvas_x + PIECE_RADIUS, canvas_y + PIECE_RADIUS,
                    fill='black', outline='white', width=2, tags="piece"
                )

def update_hint(canvas, legal_moves):
    """ Update hint circles for legal moves. """
    canvas.delete("hint")
    
    for x, y in legal_moves:
        # Convert board coordinates to canvas coordinates
        # Board y=0 is bottom, canvas y=0 is top, so flip y
        canvas_x = x * CELL_SIZE + CELL_SIZE // 2
        canvas_y = (7 - y) * CELL_SIZE + CELL_SIZE // 2
        canvas.create_oval(
            canvas_x - 16, canvas_y - 16,
            canvas_x + 16, canvas_y + 16,
            outline='yellow', width=1, tags="hint"
        )

def execute_move_with_animation(board, move, color, canvas, game_root, update_ui_func):
    """ Execute move with animation: place new piece, delay, then flip pieces. """
    # Get all pieces that need to be flipped using board's internal method
    flips = set()
    directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    for direction in directions:
        flip_list = board._get_flips(move, direction, color)
        if flip_list:
            flips.update(flip_list)
    
    # Step 1: Place the new piece immediately (it's already in flips, but we place it first)
    board[move[0]][move[1]] = color
    update_ui_func()
    game_root.update()
    
    # Step 2: Delay 0.5 seconds
    time.sleep(0.5)
    
    # Step 3: Flip all pieces that need to be flipped (the new piece is already placed)
    for x, y in flips:
        board[x][y] = color
    
    # Step 4: Update display
    update_ui_func()
    game_root.update()

def show_game_window(black_engine, white_engine, game_time=300, level_b=4, level_w=4,
                     ab_b=False, ab_w=False, verbose=False, network_mode=False,
                     is_server=False, host='localhost', port=12345):
    """ Show interactive game window. """
    
    # Create game window
    game_root = tb.Window(themename="darkly")
    game_root.title("Othello Game")
    game_root.geometry(f"{WINDOW_SIZE + 300}x{WINDOW_SIZE + 100}")
    
    # Main frame
    main_game_frame = tb.Frame(game_root, padding=10)
    main_game_frame.pack(fill="both", expand=True)
    
    # Left side - Board
    board_frame = tb.Frame(main_game_frame)
    board_frame.pack(side="left", padx=10)
    
    canvas = tk.Canvas(board_frame, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='#2cb87b')
    canvas.pack()
    
    draw_board(canvas)
    
    # Right side - Info panel
    info_frame = tb.Frame(main_game_frame)
    info_frame.pack(side="right", fill="both", expand=True, padx=10)
    
    # Game state
    game_state = {
        'board': Board(),
        'time_left': {-1: game_time, 1: game_time},
        'current_color': -1,  # Black starts
        'move_num': 0,
        'waiting_for_move': False,
        'selected_move': None,
        'legal_moves': [],
        'engines': {},
        'game_thread': None,
        'game_running': True,
        'paused': False
    }
    
    # Status labels
    status_label = tb.Label(info_frame, text="Game Starting...", font=("Arial", 14, "bold"))
    status_label.pack(pady=10)
    
    black_score_label = tb.Label(info_frame, text="Black: 2", font=("Arial", 12))
    black_score_label.pack(pady=5)
    
    white_score_label = tb.Label(info_frame, text="White: 2", font=("Arial", 12))
    white_score_label.pack(pady=5)
    
    time_label = tb.Label(info_frame, text="", font=("Arial", 10))
    time_label.pack(pady=5)
    
    legal_moves_label = tb.Label(info_frame, text="", font=("Arial", 9), wraplength=200)
    legal_moves_label.pack(pady=5)
    
    # Pause button
    pause_button = tb.Button(info_frame, text="⏸ Pause", command=lambda: toggle_pause(), bootstyle="warning")
    pause_button.pack(pady=10)
    
    # Pause overlay (initially hidden)
    overlay_frame = tk.Frame(game_root, bg='black', highlightthickness=0)
    overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
    overlay_frame.lower()  # Put behind other widgets
    
    overlay_content = tb.Frame(overlay_frame, padding=50)
    overlay_content.place(relx=0.5, rely=0.5, anchor='center')
    
    pause_label = tb.Label(overlay_content, text="PAUSED", font=("Arial", 36, "bold"), bootstyle="warning")
    pause_label.pack(pady=20)
    
    continue_button = tb.Button(overlay_content, text="▶ Continue", command=lambda: toggle_pause(), 
                               bootstyle="success", width=15)
    continue_button.pack(pady=20)
    
    overlay_frame.place_forget()  # Hide initially
    
    def toggle_pause():
        """ Toggle pause state. """
        game_state['paused'] = not game_state['paused']
        if game_state['paused']:
            pause_button.config(text="▶ Resume", state="disabled")
            overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
            overlay_frame.lift()  # Bring to front
            status_label.config(text="Game Paused")
        else:
            pause_button.config(text="⏸ Pause", state="normal")
            overlay_frame.place_forget()
            player_name = {-1: "Black", 1: "White"}
            status_label.config(text=f"{player_name[game_state['current_color']]}'s turn")
        game_root.update()
    
    # Initialize engines
    def init_engines():
        try:
            if network_mode:
                # For network mode, update status
                if is_server:
                    status_label.config(text="Waiting for client to connect...")
                else:
                    status_label.config(text=f"Connecting to {host}:{port}...")
                game_root.update()
            
            engines_b = importlib.import_module(f"engines.{black_engine}")
            engines_w = importlib.import_module(f"engines.{white_engine}")
            
            # Network receivers need connection manager to be initialized first
            # So we initialize network_server/network_client before network_receiver
            engine_b = None
            engine_w = None
            
            # Step 1: Initialize network_server or network_client first (they create connection)
            if black_engine in ["network_server", "network_client"]:
                if black_engine == "network_server":
                    engine_b = engines_b.engine(host='0.0.0.0', port=port)
                    if network_mode:
                        status_label.config(text="Server ready! Waiting for client...")
                        game_root.update()
                else:
                    engine_b = engines_b.engine(host=host, port=port)
            elif white_engine in ["network_server", "network_client"]:
                # Initialize white engine first if it's network_server/client
                if white_engine == "network_server":
                    engine_w = engines_w.engine(host='0.0.0.0', port=port)
                else:
                    engine_w = engines_w.engine(host=host, port=port)
                    if network_mode:
                        status_label.config(text="Connected! Game starting...")
                        game_root.update()
            
            # Step 2: Initialize the remaining engine (could be network_receiver or other)
            if engine_b is None:
                engine_b = engines_b.engine()
            
            if engine_w is None:
                engine_w = engines_w.engine()
            
            game_state['engines'][-1] = engine_b
            game_state['engines'][1] = engine_w
            
            # Configure engines
            engines_list = {"greedy", "human", "random", "network_receiver", "network_server", "network_client"}
            if ab_b and black_engine not in engines_list:
                game_state['engines'][-1].alpha_beta = True
            if ab_w and white_engine not in engines_list:
                game_state['engines'][1].alpha_beta = True
            
            if level_b and black_engine not in engines_list:
                game_state['engines'][-1].ply_maxmin = game_state['engines'][-1].ply_alpha = level_b
            if level_w and white_engine not in engines_list:
                game_state['engines'][1].ply_maxmin = game_state['engines'][1].ply_alpha = level_w
                
        except Exception as e:
            status_label.config(text=f"Error: {e}")
            game_state['game_running'] = False
    
    # Handle canvas click
    def on_canvas_click(event):
        if not game_state['waiting_for_move']:
            return
        
        col = event.x // CELL_SIZE
        canvas_row = event.y // CELL_SIZE
        # Convert canvas row to board row (flip y coordinate)
        board_row = 7 - canvas_row
        
        move = (col, board_row)
        if move in game_state['legal_moves']:
            game_state['selected_move'] = move
            game_state['waiting_for_move'] = False
    
    canvas.bind("<Button-1>", on_canvas_click)
    
    # Update display
    def update_display():
        board = game_state['board']
        update_ui(canvas, board)
        
        black_count = board.count(-1)
        white_count = board.count(1)
        black_score_label.config(text=f"Black: {black_count}")
        white_score_label.config(text=f"White: {white_count}")
        
        time_left = game_state['time_left']
        time_label.config(text=f"Time - Black: {time_left[-1]:.1f}s, White: {time_left[1]:.1f}s")
        
        # Only show hints when it's the player's turn (waiting for their move)
        if game_state['legal_moves']:
            if game_state['waiting_for_move']:
                # Show hints only when waiting for player's move
                update_hint(canvas, game_state['legal_moves'])
                moves_str = ', '.join([chr(ord('a') + x) + str(y + 1) for x, y in sorted(game_state['legal_moves'])])
                legal_moves_label.config(text=f"Legal moves: {moves_str}")
            else:
                # Hide hints when it's opponent's turn
                canvas.delete("hint")
                legal_moves_label.config(text="Opponent's turn")
        else:
            canvas.delete("hint")
            legal_moves_label.config(text="No legal moves")
    
    # Game loop
    def game_loop():
        board = game_state['board']
        time_left = game_state['time_left']
        
        for move_num in range(60):
            if not game_state['game_running']:
                break
            
            # Wait if paused
            while game_state['paused'] and game_state['game_running']:
                game_root.update()
                time.sleep(0.1)
            
            if not game_state['game_running']:
                break
            
            moves = []
            for color in [-1, 1]:
                if not game_state['game_running']:
                    break
                
                # Wait if paused
                while game_state['paused'] and game_state['game_running']:
                    game_root.update()
                    time.sleep(0.1)
                
                if not game_state['game_running']:
                    break
                
                legal_moves = board.get_legal_moves(color)
                if not legal_moves:
                    continue
                
                game_state['current_color'] = color
                game_state['legal_moves'] = legal_moves
                game_state['waiting_for_move'] = False
                game_state['selected_move'] = None
                
                player_name = {-1: "Black", 1: "White"}
                status_label.config(text=f"{player_name[color]}'s turn")
                game_root.update()
                
                # Check if human player or network player
                engine_name = black_engine if color == -1 else white_engine
                is_human_turn = (engine_name == "human")
                is_network_turn = (engine_name in ["network_server", "network_client"])
                is_network_receiver = (engine_name == "network_receiver")
                
                if is_human_turn or is_network_turn:
                    # Human player or network player - wait for click on GUI
                    game_state['waiting_for_move'] = True
                    move = None
                    while game_state['waiting_for_move'] and game_state['game_running']:
                        # Don't accept moves when paused
                        if game_state['paused']:
                            game_root.update()
                            time.sleep(0.1)
                            continue
                        game_root.update()
                        if game_state['selected_move']:
                            move = game_state['selected_move']
                            game_state['waiting_for_move'] = False
                            
                            # If network player, send move through network
                            if is_network_turn and move:
                                try:
                                    engine = game_state['engines'][color]
                                    if hasattr(engine, 'conn') and engine.conn:
                                        engine.conn.send_move(move)
                                        x, y = move
                                        move_str = chr(ord('a') + x) + str(y + 1)
                                        status_label.config(text=f"Sent: {move_str}")
                                        game_root.update()
                                    else:
                                        status_label.config(text="Error: No connection")
                                        game_state['game_running'] = False
                                except Exception as e:
                                    status_label.config(text=f"Error sending: {e}")
                                    game_state['game_running'] = False
                            break
                        game_root.after(50)  # Small delay to prevent busy waiting
                    
                    if not game_state['game_running']:
                        break
                    
                    if move is None:
                        continue
                elif is_network_receiver:
                    # Network receiver - wait for opponent's move from network
                    status_label.config(text=f"Waiting for opponent's move...")
                    game_root.update()
                    try:
                        engine = game_state['engines'][color]
                        if hasattr(engine, 'conn') and engine.conn:
                            # Wait for move, checking pause periodically
                            move = None
                            timeout = 300
                            start_time = time.time()
                            while move is None and (time.time() - start_time) < timeout:
                                if not game_state['game_running']:
                                    break
                                if game_state['paused']:
                                    game_root.update()
                                    time.sleep(0.1)
                                    continue
                                # Check if move is available
                                if engine.conn.move_received.is_set():
                                    with engine.conn.lock:
                                        move = engine.conn.opponent_move
                                        engine.conn.opponent_move = None
                                        engine.conn.move_received.clear()
                                    break
                                game_root.update()
                                time.sleep(0.1)
                            
                            if move is None:
                                # Timeout or connection lost
                                raise TimeoutError("Timeout waiting for opponent move")
                            if move:
                                x, y = move
                                move_str = chr(ord('a') + x) + str(y + 1)
                                status_label.config(text=f"Received: {move_str}")
                                game_root.update()
                            else:
                                status_label.config(text="No move received")
                                continue
                        else:
                            status_label.config(text="Error: No connection")
                            game_state['game_running'] = False
                            break
                    except TimeoutError:
                        status_label.config(text="Timeout waiting for opponent")
                        game_state['game_running'] = False
                        break
                    except Exception as e:
                        status_label.config(text=f"Error: {e}")
                        game_state['game_running'] = False
                        break
                else:
                    # AI player - wait if paused
                    while game_state['paused'] and game_state['game_running']:
                        game_root.update()
                        time.sleep(0.1)
                    
                    if not game_state['game_running']:
                        break
                    
                    start_time = timeit.default_timer()
                    try:
                        move = game_state['engines'][color].get_move(
                            copy.deepcopy(board), color, move_num,
                            time_left[color], time_left[-color]
                        )
                    except Exception as e:
                        status_label.config(text=f"Error: {e}")
                        game_state['game_running'] = False
                        break
                    end_time = timeit.default_timer()
                    time_left[color] -= round(end_time - start_time, 1)
                
                if time_left[color] < 0:
                    status_label.config(text=f"{player_name[color]} ran out of time!")
                    game_state['game_running'] = False
                    break
                
                if move and move in legal_moves:
                    # Execute move with animation
                    execute_move_with_animation(board, move, color, canvas, game_root, update_display)
                    moves.append(move)
                    
                    if verbose:
                        move_str = chr(ord('a') + move[0]) + str(move[1] + 1)
                        status_label.config(text=f"{player_name[color]} played {move_str}")
            
            if not moves:
                break
        
        # Game over
        black_count = board.count(-1)
        white_count = board.count(1)
        if black_count > white_count:
            status_label.config(text=f"Black wins! ({black_count}-{white_count})")
        elif white_count > black_count:
            status_label.config(text=f"White wins! ({white_count}-{black_count})")
        else:
            status_label.config(text=f"Tie! ({black_count}-{white_count})")
        
        game_state['game_running'] = False
        update_display()
    
    # Initial display
    update_display()
    
    # Start game - initialize engines in thread to avoid blocking UI
    def init_and_start():
        init_engines()
        if game_state['game_running']:
            update_display()
            # Start game loop
            game_loop()
    
    # Run initialization and game in thread
    game_state['game_thread'] = threading.Thread(target=init_and_start, daemon=True)
    game_state['game_thread'].start()
    
    # Close handler
    def on_closing():
        game_state['game_running'] = False
        # Close network connections if any
        if network_mode:
            try:
                if -1 in game_state['engines'] and hasattr(game_state['engines'][-1], 'conn'):
                    game_state['engines'][-1].conn.close()
                if 1 in game_state['engines'] and hasattr(game_state['engines'][1], 'conn'):
                    game_state['engines'][1].conn.close()
            except:
                pass
        game_root.destroy()
    
    game_root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Update display periodically
    def periodic_update():
        if game_state['game_running']:
            update_display()
            game_root.after(100, periodic_update)
    
    periodic_update()
    
    game_root.mainloop()

# === Main GUI Setup ===
root = tb.Window(themename="darkly")
root.title("Othello Game Launcher")
root.geometry("500x600")

TITLE_FONT = ("Courier New", 20, "bold")
main_frame = tb.Frame(root, padding=30)
main_frame.pack(fill="both", expand=True)

# Show main menu initially
show_main_menu()

root.mainloop()

