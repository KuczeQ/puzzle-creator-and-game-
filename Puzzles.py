import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import random


class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puzzles")
        
        self.puzzle_image = None
        self.initial_image = None
        self.puzzle_size = 100
        self.puzzle_cols = 0
        self.puzzle_rows = 0
        self.puzzle_pieces = []
        self.expected_pieces = []  
        self.empty_idx = None  
        
        self.canvas = tk.Canvas(self.root, width=0, height=0)  
        self.canvas.pack()
        
        self.select_image_button = tk.Button(self.root, text="Wybierz obraz", command=self.select_image)
        self.select_image_button.pack()
        
        self.shuffle_button = tk.Button(self.root, text="Przetasuj", command=self.shuffle_puzzle, state=tk.DISABLED)
        self.shuffle_button.pack()
        
        self.canvas.bind("<Button-1>", self.move_piece)
        
        self.selected_idx = None
        
        self.root.mainloop()
    
    def select_image(self):
        image_file = filedialog.askopenfilename(filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg")])
        if image_file:
            self.puzzle_image = Image.open(image_file)
            self.initial_image = self.puzzle_image.copy()
            self.puzzle_cols = int(self.puzzle_image.width / self.puzzle_size)
            self.puzzle_rows = int(self.puzzle_image.height / self.puzzle_size)
            self.init_puzzle_pieces()
            self.redraw_puzzle()
            self.shuffle_button.config(state=tk.NORMAL)
    
    def init_puzzle_pieces(self):
        self.canvas.config(width=self.puzzle_cols * self.puzzle_size, height=self.puzzle_rows * self.puzzle_size)
        for row in range(self.puzzle_rows):
            for col in range(self.puzzle_cols):
                puzzle_piece = self.puzzle_image.crop((col * self.puzzle_size, row * self.puzzle_size,
                                                       (col + 1) * self.puzzle_size, (row + 1) * self.puzzle_size))
                puzzle_piece = ImageTk.PhotoImage(puzzle_piece)
                self.puzzle_pieces.append(puzzle_piece)
                self.expected_pieces.append(puzzle_piece) 
                
                self.canvas.create_image(col * self.puzzle_size, row * self.puzzle_size,
                                         anchor=tk.NW, image=puzzle_piece)
        
        self.empty_idx = None
    
    def shuffle_puzzle(self):
        random.shuffle(self.puzzle_pieces)
        self.redraw_puzzle()
    
    def redraw_puzzle(self):
        self.canvas.delete("all")
        for idx, puzzle_piece in enumerate(self.puzzle_pieces):
            if puzzle_piece is not None:
                row = idx // self.puzzle_cols
                col = idx % self.puzzle_cols
                self.canvas.create_image(col * self.puzzle_size, row * self.puzzle_size,
                                         anchor=tk.NW, image=puzzle_piece)
    
    def move_piece(self, event):
        col = event.x // self.puzzle_size
        row = event.y // self.puzzle_size
        idx = row * self.puzzle_cols + col

        if self.selected_idx is None:
            self.selected_idx = idx
        else:
            if self.selected_idx != idx:
                if self.is_neighbor(idx, self.selected_idx):
                    try:
                        puzzle_piece = self.puzzle_pieces[idx]
                        self.puzzle_pieces[idx] = self.puzzle_pieces[self.selected_idx]
                        self.puzzle_pieces[self.selected_idx] = puzzle_piece
                        
                        if self.empty_idx == self.selected_idx:
                            self.empty_idx = idx
                        elif self.empty_idx == idx:
                            self.empty_idx = self.selected_idx
                            
                        self.selected_idx = None
                        self.redraw_puzzle()
                        
                        if self.check_solution():
                            messagebox.showinfo('Gratulacje', 'Układanka została ułożona poprawnie!')
                    except IndexError:
                        pass
                else:
                    self.selected_idx = idx
    
    def is_neighbor(self, idx1, idx2):
        row1, col1 = divmod(idx1, self.puzzle_cols)
        row2, col2 = divmod(idx2, self.puzzle_cols)
        return abs(row1 - row2) + abs(col1 - col2) == 1
    
    def check_solution(self):
        for idx, puzzle_piece in enumerate(self.puzzle_pieces):
            if puzzle_piece is not None and idx != len(self.puzzle_pieces) - 1:
                expected_piece = self.expected_pieces[idx] 
                if puzzle_piece != expected_piece:
                    return False

        return True


app = PuzzleApp()
