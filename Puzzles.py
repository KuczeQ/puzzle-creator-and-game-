import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import random
from tkinter import messagebox

class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puzzles")
        
        self.puzzle_image = None
        self.puzzle_size = 100
        self.puzzle_cols = 0
        self.puzzle_rows = 0
        self.puzzle_pieces = []
        self.empty_idx = None  
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        
        self.select_image_button = tk.Button(self.root, text="choose image", command=self.select_image)
        self.select_image_button.pack()
        
        self.shuffle_button = tk.Button(self.root, text="shuffle", command=self.shuffle_puzzle, state=tk.DISABLED)
        self.shuffle_button.pack()
        
        self.canvas.bind("<Button-1>", self.move_piece)
        
        self.root.mainloop()
    
    def select_image(self):
        image_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_file:
            self.puzzle_image = Image.open(image_file)
            self.puzzle_cols = int(self.puzzle_image.width / self.puzzle_size)
            self.puzzle_rows = int(self.puzzle_image.height / self.puzzle_size)
            self.init_puzzle_pieces()
            self.redraw_puzzle()
            self.shuffle_button.config(state=tk.NORMAL)
    
    def init_puzzle_pieces(self):
        for row in range(self.puzzle_rows):
            for col in range(self.puzzle_cols):
                puzzle_piece = self.puzzle_image.crop((col * self.puzzle_size, row * self.puzzle_size,
                                                       (col + 1) * self.puzzle_size, (row + 1) * self.puzzle_size))
                puzzle_piece = ImageTk.PhotoImage(puzzle_piece)
                self.puzzle_pieces.append(puzzle_piece)
                
                self.canvas.create_image(col * self.puzzle_size, row * self.puzzle_size,
                                         anchor=tk.NW, image=puzzle_piece)
        
        self.empty_idx = len(self.puzzle_pieces) - 1  
    
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
        if idx < len(self.puzzle_pieces) and self.puzzle_pieces[idx] is not None:
            puzzle_piece = self.puzzle_pieces[idx]
            self.puzzle_pieces[idx] = None
            self.puzzle_pieces[self.empty_idx] = puzzle_piece
            self.empty_idx = idx
            self.redraw_puzzle()
            if self.check_solution():
                messagebox.showinfo('Congratulations', 'The puzzle has been completed correctly!')
    
    def check_solution(self):
        for idx, puzzle_piece in enumerate(self.puzzle_pieces):
            if puzzle_piece is not None and idx != len(self.puzzle_pieces) - 1:
                expected_piece = self.puzzle_image.crop((idx % self.puzzle_cols * self.puzzle_size,
                                                         idx // self.puzzle_cols * self.puzzle_size,
                                                         (idx % self.puzzle_cols + 1) * self.puzzle_size,
                                                         (idx // self.puzzle_cols + 1) * self.puzzle_size))
                if puzzle_piece.width != expected_piece.width or puzzle_piece.height != expected_piece.height:
                    return False
                pixels1 = puzzle_piece.get()  
                pixels2 = expected_piece.get()  
                if pixels1 != pixels2:
                    return False
        return True

app = PuzzleApp()
