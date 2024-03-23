import sqlite3 # imports sqlite3 modules/ allows us to work with database.

class Dictionary:
    def __init__(self, db_name):
        # initialize the Dictionary class with the db name.
        self.connection = sqlite3.connect(db_name) # connects to db
        self.cursor = self.connection.cursor() # allows us to interact with db
        self.create_tables() # calls the below table to create required tables in db

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                                id INTEGER PRIMARY KEY,
                                word TEXT UNIQUE
                            )''')
        # used to execute prepared statements
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS meanings (  
                                id INTEGER PRIMARY KEY,
                                word_id INTEGER,
                                meaning TEXT,
                                FOREIGN KEY (word_id) REFERENCES words(id)
                            )''')
        self.connection.commit() # saves changes made by execute method

    def add_word(self, word, meanings):
        # Add the word to the 'words' table
        self.cursor.execute('''INSERT INTO words (word) VALUES (?)''', (word,))
        word_id = self.cursor.lastrowid   # gets the last inserted row id

        # Add meanings to the 'meanings' table
        for meaning in meanings:
            self.cursor.execute('''INSERT INTO meanings (word_id, meaning) VALUES (?, ?)''', (word_id, meaning))

        self.connection.commit()

    def lookup_word(self, word):
        self.cursor.execute('''SELECT meaning FROM meanings WHERE word_id = (SELECT id FROM words WHERE word = ?)''', (word,))
        meanings = self.cursor.fetchall() # fetch all rows from result of the query
        return [meaning[0] for meaning in meanings] # returns list of all meanings, 0 is accessing the first element of each tuple.
    

def main():
    dictionary = Dictionary('dictionary.db') #  creates an instance of each dicttionary

    while True:
        # 1. will add word to the dictionary
        # 2. looks up word
        # 3. Quits
        choice = input("Enter your choice: ")

        if choice == '1':
            print("ADD WORD TO DICTIONARY.")
            word = input("Enter the word: ")
            print("ADD MEANING TO THE WORD.")
            meanings = input("Enter the meanings: ").split(',')
            dictionary.add_word(word, meanings) # call s the add_word method to add the word in the dictionary
            print(f"'{word}' added to dictionary.")

        # line 60 Calls lookup_word method to find meanings of the word
        elif choice == '2': 
            print("LOOK UP MEANING")
            word = input("Enter a word to look up: ")
            meanings = dictionary.lookup_word(word) 
            if meanings:
                print(f"Meanings of '{word}': {', '.join(meanings)}")
            else:
                print(f"'{word}' not found in the dictionary.")

        elif choice == '3':
            print("QUIT IT")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() # Call the main function if the script is executed directly