import tkinter as tk
from tkinter import messagebox
import random
import itertools
import operator

class TwentyFourGame:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("24 Point Game")
        self.window.geometry("400x500")
        self.window.configure(bg='#f0f0f0')

        # Define operators for calculations
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        # Store current numbers and solution
        self.current_numbers = []
        self.current_solution = ""

        # Create and configure GUI elements
        self.setup_gui()
        
        # Generate initial numbers
        self.generate_new_numbers()

    def setup_gui(self):
        """Set up all GUI elements"""
        # Title Label
        title_label = tk.Label(self.window, text="24 Point Game", font=("Arial", 20, "bold"), bg='#f0f0f0')
        title_label.pack(pady=20)

        # Instructions
        instructions = "Make 24 using the four numbers below.\nYou can use +, -, *, / and parentheses."
        instruction_label = tk.Label(self.window, text=instructions, font=("Arial", 12), bg='#f0f0f0')
        instruction_label.pack(pady=10)

        # Numbers Frame
        self.numbers_frame = tk.Frame(self.window, bg='#f0f0f0')
        self.numbers_frame.pack(pady=20)
        self.number_labels = []

        # Create labels for numbers
        for i in range(4):
            label = tk.Label(self.numbers_frame, text="", font=("Arial", 24, "bold"), 
                           width=3, height=1, relief="raised", bg='white')
            label.pack(side=tk.LEFT, padx=10)
            self.number_labels.append(label)

        # Answer Entry
        self.answer_entry = tk.Entry(self.window, font=("Arial", 14), width=25)
        self.answer_entry.pack(pady=20)

        # Buttons Frame
        buttons_frame = tk.Frame(self.window, bg='#f0f0f0')
        buttons_frame.pack(pady=10)

        # Check Answer Button
        check_button = tk.Button(buttons_frame, text="Check Answer", command=self.check_answer,
                               font=("Arial", 12), bg='#4CAF50', fg='white')
        check_button.pack(side=tk.LEFT, padx=5)

        # New Numbers Button
        new_button = tk.Button(buttons_frame, text="New Numbers", command=self.generate_new_numbers,
                             font=("Arial", 12), bg='#2196F3', fg='white')
        new_button.pack(side=tk.LEFT, padx=5)

        # Reveal Answer Button
        reveal_button = tk.Button(buttons_frame, text="Reveal Answer", command=self.reveal_answer,
                                font=("Arial", 12), bg='#FFC107', fg='white')
        reveal_button.pack(side=tk.LEFT, padx=5)

    def generate_new_numbers(self):
        """Generate four new random numbers and find a solution"""
        # Generate 4 random numbers between 1 and 10
        self.current_numbers = [random.randint(1, 10) for _ in range(4)]
        
        # Update the display
        for i, label in enumerate(self.number_labels):
            label.config(text=str(self.current_numbers[i]))

        # Clear the answer entry
        self.answer_entry.delete(0, tk.END)
        
        # Find a solution
        self.find_solution()

    def evaluate_expression(self, nums, ops):
        """Evaluate an expression with given numbers and operators"""
        try:
            # First apply multiplication and division
            i = 0
            while i < len(ops):
                if ops[i] in ['*', '/']:
                    if ops[i] == '/' and nums[i+1] == 0:  # Check division by zero
                        return None
                    nums[i] = self.operators[ops[i]](nums[i], nums[i+1])
                    nums.pop(i+1)
                    ops.pop(i)
                else:
                    i += 1

            # Then apply addition and subtraction
            while ops:
                nums[0] = self.operators[ops[0]](nums[0], nums[1])
                nums.pop(1)
                ops.pop(0)

            return nums[0]
        except:
            return None

    def find_solution(self):
        """Find a solution that equals 24"""
        self.current_solution = ""
        numbers = self.current_numbers.copy()
        
        # Try all possible number combinations
        for nums in itertools.permutations(numbers):
            # Try all possible operator combinations
            for ops in itertools.product(['+', '-', '*', '/'], repeat=3):
                # Try different groupings
                # Case 1: ((a op1 b) op2 c) op3 d
                nums_copy = list(nums)
                result = self.evaluate_expression(nums_copy.copy(), list(ops))
                if result is not None and abs(result - 24) < 0.0001:
                    self.current_solution = f"(({nums[0]}{ops[0]}{nums[1]}){ops[1]}{nums[2]}){ops[2]}{nums[3]}"
                    return

                # Case 2: (a op1 b) op2 (c op3 d)
                nums_copy = list(nums)
                try:
                    left = self.operators[ops[0]](nums_copy[0], nums_copy[1])
                    right = self.operators[ops[2]](nums_copy[2], nums_copy[3])
                    result = self.operators[ops[1]](left, right)
                    if abs(result - 24) < 0.0001:
                        self.current_solution = f"({nums[0]}{ops[0]}{nums[1]}){ops[1]}({nums[2]}{ops[2]}{nums[3]})"
                        return
                except:
                    continue

    def check_answer(self):
        """Check if the user's answer evaluates to 24"""
        try:
            # Get user's answer and evaluate it
            answer = self.answer_entry.get()
            # Replace the numbers in the expression with their actual values
            for i, num in enumerate(self.current_numbers):
                answer = answer.replace(str(num), str(float(num)))
            result = eval(answer)
            
            # Check if the result is 24
            if abs(result - 24) < 0.0001:
                messagebox.showinfo("Correct!", "Well done! That's correct!")
            else:
                messagebox.showinfo("Incorrect", f"Your answer evaluates to {result:.2f}, not 24. Try again!")
        except:
            messagebox.showerror("Error", "Invalid expression! Please check your input.")

    def reveal_answer(self):
        """Show the solution"""
        if self.current_solution:
            messagebox.showinfo("Solution", f"One possible solution is:\n{self.current_solution} = 24")
        else:
            messagebox.showinfo("No Solution", "No solution found for these numbers!")

    def run(self):
        """Start the game"""
        self.window.mainloop()

if __name__ == "__main__":
    game = TwentyFourGame()
    game.run()
