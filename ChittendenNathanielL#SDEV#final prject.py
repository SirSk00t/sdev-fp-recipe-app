






import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('recipes.db')
c = conn.cursor()

# Create the recipes table
c.execute('''CREATE TABLE IF NOT EXISTS recipes
             (id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT, instructions TEXT, category TEXT)''')

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

# Create the main application window
root = tk.Tk()
root.title("Recipe Organizer")

# Create frames for different sections
frame_main = tk.Frame(root)
frame_main.pack()

frame_add = tk.Frame(root)
frame_search = tk.Frame(root)
frame_view = tk.Frame(root)

# Function to switch frames
def show_frame(frame):
    frame_main.pack_forget()
    frame_add.pack_forget()
    frame_search.pack_forget()
    frame_view.pack_forget()
    frame.pack()

# Main menu buttons
btn_add = tk.Button(frame_main, text="Add Recipe", command=lambda: show_frame(frame_add))
btn_search = tk.Button(frame_main, text="Search Recipes", command=lambda: show_frame(frame_search))
btn_view = tk.Button(frame_main, text="View All Recipes", command=lambda: show_frame(frame_view))
btn_exit = tk.Button(frame_main, text="Exit", command=root.quit)

btn_add.pack()
btn_search.pack()
btn_view.pack()
btn_exit.pack()

# Add Recipe screen elements
tk.Label(frame_add, text="Recipe Name").pack()
entry_name = tk.Entry(frame_add)
entry_name.pack()

tk.Label(frame_add, text="Ingredients").pack()
entry_ingredients = tk.Entry(frame_add)
entry_ingredients.pack()

tk.Label(frame_add, text="Instructions").pack()
entry_instructions = tk.Entry(frame_add)
entry_instructions.pack()

tk.Label(frame_add, text="Category").pack()
entry_category = tk.Entry(frame_add)
entry_category.pack()

def save_recipe():
    name = entry_name.get()
    ingredients = entry_ingredients.get()
    instructions = entry_instructions.get()
    category = entry_category.get()
    
    if name and ingredients and instructions and category:
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute("INSERT INTO recipes (name, ingredients, instructions, category) VALUES (?, ?, ?, ?)",
                  (name, ingredients, instructions, category))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Recipe added successfully!")
        entry_name.delete(0, tk.END)
        entry_ingredients.delete(0, tk.END)
        entry_instructions.delete(0, tk.END)
        entry_category.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

tk.Button(frame_add, text="Save", command=save_recipe).pack()
tk.Button(frame_add, text="Cancel", command=lambda: show_frame(frame_main)).pack()

# Search Recipes screen elements
tk.Label(frame_search, text="Search").pack()
entry_search = tk.Entry(frame_search)
entry_search.pack()

listbox_results = tk.Listbox(frame_search)
listbox_results.pack()

def search_recipes():
    query = entry_search.get()
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM recipes WHERE name LIKE ? OR ingredients LIKE ? OR category LIKE ?",
              ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = c.fetchall()
    conn.close()
    
    listbox_results.delete(0, tk.END)
    for result in results:
        listbox_results.insert(tk.END, result)

listbox_results.bind("<Double-1>", lambda x: show_recipe_details(listbox_results.get(listbox_results.curselection())[0]))

tk.Button(frame_search, text="Search", command=search_recipes).pack()
tk.Button(frame_search, text="Back", command=lambda: show_frame(frame_main)).pack()

def show_recipe_details(recipe_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,))
    recipe = c.fetchone()
    conn.close()
    
    messagebox.showinfo("Recipe Details", f"Name: {recipe[1]}\n\nIngredients: {recipe[2]}\n\nInstructions: {recipe[3]}\n\nCategory: {recipe[4]}")

# View All Recipes screen elements
listbox_all_recipes = tk.Listbox(frame_view)
listbox_all_recipes.pack()

def view_all_recipes():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM recipes")
    results = c.fetchall()
    conn.close()
    
    listbox_all_recipes.delete(0, tk.END)
    for result in results:
        listbox_all_recipes.insert(tk.END, result)

listbox_all_recipes.bind("<Double-1>", lambda x: show_recipe_details(listbox_all_recipes.get(listbox_all_recipes.curselection())[0]))

tk.Button(frame_view, text="Refresh", command=view_all_recipes).pack()
tk.Button(frame_view, text="Back", command=lambda: show_frame(frame_main)).pack()

# Run the main application loop
root.mainloop()
