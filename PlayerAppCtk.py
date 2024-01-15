from PlayerDb import PlayerDb  # Assuming PlayerDb is the modified class for basketball players
from PlayerGuiCtk import PlayerGuiCtk

def main():
    db = PlayerDb(init=False, dbName='PlayerDb.csv')  # Assuming PlayerDb is the modified class for basketball players
    app = PlayerGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
