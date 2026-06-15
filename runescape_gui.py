import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

# API Endpoint (using a placeholder for user name)
API_URL = "https://apps.runescape.com/runemetrics/profile/profile?user={}&activities=20"

class RunescapeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Runescape stats By Mariapori")
        # Skill ID to Name Mapping (Based on user provided list)
        self.SKILL_MAP = {
            0: "Attack", 1: "Defence", 2: "Strength", 3: "Constitution", 4: "Ranged",
            5: "Prayer", 6: "Magic", 7: "Cooking", 8: "Woodcutting", 9: "Fletching",
            10: "Fishing", 11: "Firemaking", 12: "Crafting", 13: "Smithing", 14: "Mining",
            15: "Herblore", 16: "Agility", 17: "Thieving", 18: "Slayer", 19: "Farming",
            20: "Runecrafting", 21: "Hunter", 22: "Construction", 23: "Summoning", 24: "Dungeoneering",
            25: "Divination", 26: "Invention", 27: "Archaeology", 28: "Necromancy"
        }
        style = ttk.Style()
        style.theme_use('clam') # Modern theme

        # --- Input Frame (Account Name & Button) ---
        input_frame = ttk.Frame(master, padding="10")
        input_frame.pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Enter Account Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.account_entry = ttk.Entry(input_frame, width=30)
        self.account_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.account_entry.insert(0, "ExampleAccountName") # Pre-fill for testing

        self.fetch_button = ttk.Button(input_frame, text="Fetch Profile", command=self.fetch_player_data)
        self.fetch_button.grid(row=0, column=2, padx=15, pady=5, sticky='e')

        # --- Main Content Frames (Stats & Skills) ---
        main_content = ttk.Frame(master)
        main_content.pack(fill='both', expand=True, pady=10)

        # 1. Basic Stats Frame
        stats_frame = ttk.LabelFrame(main_content, text="Basic Profile Stats", padding="10")
        stats_frame.pack(fill='x', padx=5, pady=10)

        self.name_label = ttk.Label(stats_frame, text="Name: N/A", font=('Arial', 12))
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.rank_label = ttk.Label(stats_frame, text="Rank: N/A", font=('Arial', 12))
        self.rank_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.totalskill_label = ttk.Label(stats_frame, text="Total Skill: N/A", font=('Arial', 12))
        self.totalskill_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.totalxp_label = ttk.Label(stats_frame, text="Total XP: N/A", font=('Arial', 12))
        self.totalxp_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Use a grid layout for better alignment of stats
        ttk.Label(stats_frame, text="Combat Level:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.combatlevel_label = ttk.Label(stats_frame, text="N/A", font=('Arial', 12))
        self.combatlevel_label.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # 2. Skill Data Table (Treeview)
        ttk.Label(main_content, text="Skill Details", font=('Arial', 14, 'bold')).pack(pady=(10, 5))
        
        # Use a frame to contain the Treeview and Scrollbar for better layout control
        skill_container = ttk.Frame(main_content)
        skill_container.pack(fill='both', expand=True, padx=5, pady=10)

        self.skill_tree = ttk.Treeview(skill_container, columns=("Name", "Level", "XP"), show='headings')
        self.skill_tree.heading("Name", text="Skill Name")
        self.skill_tree.heading("Level", text="Level")
        self.skill_tree.heading("XP", text="Experience Points")

        # Set column widths and padding
        self.skill_tree.column("Name", width=300, anchor='w')
        self.skill_tree.column("Level", width=100, anchor='center')
        self.skill_tree.column("XP", width=150, anchor='e')

        # Scrollbar setup - Ensure the scrollbar is correctly linked and placed
        scrollbar = ttk.Scrollbar(skill_container)
        self.skill_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout for Treeview and Scrollbar within the container
        self.skill_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure grid weights so both widgets expand equally
        skill_container.grid_columnconfigure(0, weight=1)
        skill_container.grid_columnconfigure(1, weight=0) # Scrollbar doesn't need to expand horizontally
        skill_container.grid_rowconfigure(0, weight=1)

    def clear_stats(self):
        """Clears all displayed data."""
        self.name_label.config(text="Name: N/A")
        self.rank_label.config(text="Rank: N/A")
        self.totalskill_label.config(text="Total Skill: N/A")
        self.totalxp_label.config(text="Total XP: N/A")
        self.combatlevel_label.config(text="N/A")

        # Clear Treeview data
        for item in self.skill_tree.get_children():
            self.skill_tree.delete(item)

    def fetch_player_data(self):
        """Handles the API call, parsing, and GUI update."""
        account_name = self.account_entry.get().strip()
        if not account_name:
            messagebox.showerror("Error", "Please enter an account name.")
            return

        # Clear previous data before fetching new data
        self.clear_stats()
        
        url = API_URL.format(account_name)
        print(f"Fetching data from: {url}") # For debugging/logging

        try:
            # Set a timeout for robustness
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            self.process_and_display_data(data)

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("API Error", f"HTTP Error occurred: {e}. Check if the account name is correct or if the API endpoint changed.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Network Error", "Could not connect to the Runemetrics API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout Error", "The request timed out. The API might be slow or unreachable.")
        except json.JSONDecodeError:
            messagebox.showerror("Parsing Error", "Failed to decode JSON response from the API.")
        except Exception as e:
            messagebox.showerror("An Unexpected Error Occurred", f"An unexpected error occurred: {e}")

    def process_and_display_data(self, data):
        """Parses the raw JSON data and updates the GUI elements."""
        try:
            # 1. Basic Stats Population
            name = data.get('name', 'N/A')
            rank = data.get('rank', 'N/A')
            
            total_skill = data.get('totalskill', 'N/A')
            total_xp = data.get('totalxp', 'N/A')
            combat_level = data.get('combatlevel', 'N/A')

            self.name_label.config(text=f"Name: {name}")
            self.rank_label.config(text=f"Rank: {rank}")
            self.totalskill_label.config(text=f"Total Skill: {total_skill}")
            self.totalxp_label.config(text=f"Total XP: {total_xp}")
            self.combatlevel_label.config(text=str(combat_level))

            # 2. Skill Table Population
            for skill in data.get('skillvalues', []):
                skill_id = skill.get('id')
                if skill_id is None or not isinstance(skill_id, int):
                    continue

                skill_name = self.SKILL_MAP.get(skill_id, f"Unknown Skill ID {skill_id}")
                level = skill.get('level', 'N/A')
                xp = skill.get('xp', 'N/A')
                
                # Insert into Treeview
                self.skill_tree.insert('', tk.END, values=(skill_name, level, xp))

        except Exception as e:
            messagebox.showerror("Data Processing Error", f"Error processing data structure: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RunescapeGUI(root)
    # Start the Tkinter event loop
    root.mainloop()