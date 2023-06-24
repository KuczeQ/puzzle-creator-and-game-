from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import random

app = Flask(__name__)

@app.route('/puzzle', methods=['POST'])
def create_puzzle():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    image = Image.open(image_file)
    
    # Konwertowanie obrazka na macierz NumPy
    image_array = np.array(image)
    
    # Przetwarzanie obrazka na układankę
    puzzle = process_image(image_array)
    
    # Mieszanie puzzli
    random.shuffle(puzzle)
    
    # Konwersja puzzli z powrotem na obrazek
    processed_image = combine_puzzle(puzzle)
    
    # Zapisanie przetworzonego obrazka
    processed_image.save('processed_image.jpg')
    
    return jsonify({'message': 'Puzzle created', 'processed_image': 'processed_image.jpg'})

def process_image(image):
    # Pobranie rozmiarów obrazka
    height, width, _ = image.shape
    
    # Podział obrazka na fragmenty (puzzli)
    puzzle_size = 100  # Rozmiar każdego puzzla
    puzzle_rows = height // puzzle_size
    puzzle_cols = width // puzzle_size
    
    puzzle = []
    
    for row in range(puzzle_rows):
        for col in range(puzzle_cols):
            # Wyodrębnienie fragmentu obrazka (puzzla)
            puzzle_piece = image[row * puzzle_size: (row + 1) * puzzle_size,
                                 col * puzzle_size: (col + 1) * puzzle_size]
            
            # Dodanie puzzla do listy puzzli
            puzzle.append(puzzle_piece)
    
    return puzzle

def combine_puzzle(puzzle):
    puzzle_size = puzzle[0].shape[0]  # Rozmiar puzzla
    
    # Obliczenie wymiarów nowego obrazka na podstawie liczby puzzli
    puzzle_rows = int(np.sqrt(len(puzzle)))
    puzzle_cols = int(len(puzzle) / puzzle_rows)
    
    # Tworzenie pustego obrazka o rozmiarze wynikowym
    combined_image = Image.new('RGB', (puzzle_cols * puzzle_size, puzzle_rows * puzzle_size))
    
    for idx, puzzle_piece in enumerate(puzzle):
        # Obliczanie współrzędnych dla każdego puzzla
        row = idx // puzzle_cols
        col = idx % puzzle_cols
        
        # Obliczanie współrzędnych pikseli dla puzzla
        start_row = row * puzzle_size
        end_row = start_row + puzzle_size
        start_col = col * puzzle_size
        end_col = start_col + puzzle_size
        
        # Wstawianie puzzla do obrazka wynikowego
        combined_image.paste(Image.fromarray(puzzle_piece), (start_col, start_row))
    
    return combined_image

if __name__ == '__main__':
    app.run()
