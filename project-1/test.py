import tkinter as tk
from tkinter import messagebox
import random
import subprocess
from PIL import Image, ImageTk  # Import Pillow for more image formats

class GuessTheWordGame:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Word Game")
        
        # Set the window to full screen
        self.root.attributes('-fullscreen', True)
        
        # Load and set the background image
        self.bg_image = Image.open("img1.jpg")  # Replace with your image file
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))  # Resize image to fit the screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        
        # Add the background image to the canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Define lists of words with their types
        self.word_types = {
            "fruit": ["apple", "banana", "cherry"],
            "food": ["pizza", "burger", "maggi"],
            "social media": ["Facebook", "Twitter", "Instagram", "LinkedIn", "Snapchat"],
            "phone": ["iPhone", "Samsung", "OnePlus"],
            "number": ["one", "two", "three", "four", "five", "six"]
        }
        
        # Flatten the lists into a single list
        self.word_list = [word.lower() for words in self.word_types.values() for word in words]
        self.target_word = random.choice(self.word_list)  # Convert to lower case for consistency
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.hint_used = False  # Track if a hint has been used
        self.correct_guesses = 0  # Track how many words have been guessed correctly

        # Create and place widgets on the canvas with updated colors
        self.word_display = tk.Label(root, text=self.get_display_word(), font=('Helvetica', 16), bg='white', fg='black')
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 100, window=self.word_display)

        self.entry = tk.Entry(root, font=('Helvetica', 16), bg='white', fg='black', insertbackground='black')
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 160, window=self.entry)
        
        self.submit_button = self.create_button('Submit', self.submit_guess)
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 220, window=self.submit_button)
        
        self.hint_button = self.create_button('Hint', self.give_hint)
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 280, window=self.hint_button)

        self.quit_button = self.create_button('Quit', self.quit_game)
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 340, window=self.quit_button)

        self.attempts_label = tk.Label(root, text=f'Attempts left: {self.attempts_left}', font=('Helvetica', 16), bg='white', fg='black')
        self.canvas.create_window(self.root.winfo_screenwidth() // 2, 400, window=self.attempts_label)
        
        # Reveal the last letter as a hint
        self.reveal_last_letter()

        # Bind Enter key to submit guess
        self.root.bind('<Return>', self.submit_guess_from_key)

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, font=('Helvetica', 16), bg='white', fg='black',
                           bd=0, highlightthickness=0)  # Removed border (bd=0) and border thickness
        button.bind("<Enter>", self.on_hover)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_hover(self, event):
        event.widget.config(fg='blue')  # Change text to blue on hover

    def on_leave(self, event):
        event.widget.config(fg='black')  # Revert text color to black when cursor leaves

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.target_word])

    def submit_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha():
            messagebox.showerror("Invalid input", "Please enter only letters.")
            return

        new_guesses = set(guess) - self.guessed_letters  # Only process new guesses
        self.guessed_letters.update(new_guesses)

        if any(letter not in self.target_word for letter in new_guesses):
            self.attempts_left -= 1

        self.update_display()

    def submit_guess_from_key(self, event):
        self.submit_guess()

    def update_display(self):
        display_word = self.get_display_word()
        self.word_display.config(text=display_word)
        self.attempts_label.config(text=f'Attempts left: {self.attempts_left}')

        if '_' not in display_word:
            self.correct_guesses += 1  # Increment correct guesses
            if self.correct_guesses == 5:
                messagebox.showinfo("Congratulations!", "Password unlocked successfully!")
                
                self.quit_game()  # Quit the game after 5 correct guesses
                subprocess.run(['python', 'end.py'])
            else:
                messagebox.showinfo("Congratulations!", f"You have guessed the word correctly! {5 - self.correct_guesses} more to go!")
                self.reset_game()
        elif self.attempts_left <= 0:
            messagebox.showinfo("Game Over", "Wrong password, ship has been locked!")
            self.quit_game() 
            subprocess.run(['python', 'end1.py'])
            
    def reset_game(self):
        self.target_word = random.choice(self.word_list)  # Convert to lower case for consistency
        self.guessed_letters.clear()
        self.attempts_left = self.max_attempts
        self.hint_used = False  # Reset hint usage
        self.hint_button.config(state=tk.NORMAL)  # Enable the hint button again
        self.update_display()
        self.reveal_last_letter()

    def reveal_last_letter(self):
        last_letter = self.target_word[-1]
        self.guessed_letters.add(last_letter)
        self.word_display.config(text=self.get_display_word())

    def give_hint(self):
        if self.hint_used:
            messagebox.showinfo("No hints left", "You have already used your hint.")
            return
        
        # Find letters that are not yet guessed
        unguessed_letters = [letter for letter in self.target_word if letter not in self.guessed_letters]
        if not unguessed_letters:
            messagebox.showinfo("No hints", "All letters have already been guessed!")
            return

        # Pick a random letter from unguessed letters
        hint_letter = random.choice(unguessed_letters)
        self.guessed_letters.add(hint_letter)
        self.word_display.config(text=self.get_display_word())
        
        # Get the type of the word
        word_type = self.get_word_type(self.target_word)
        messagebox.showinfo("Hint", f"Here's a hint! The letter '{hint_letter}' is in the word. It is of type '{word_type}'.")
        
        # Disable further hints
        self.hint_used = True
        self.hint_button.config(state=tk.DISABLED)  # Disable the hint button

    def get_word_type(self, word):
        for word_type, words in self.word_types.items():
            if word in [w.lower() for w in words]:
                return word_type
        return "unknown"

    def quit_game(self):
        self.root.destroy()  # Close the application

# Create the main window
root = tk.Tk()
game = GuessTheWordGame(root)
root.mainloop()
