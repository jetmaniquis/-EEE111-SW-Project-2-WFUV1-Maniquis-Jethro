from PlayerDb import PlayerDb  # Assuming PlayerDb is the modified class for football players
from PlayerGuiTk import PlayerGuiTk

def main():
    db = PlayerDb(init=False, dbName='PlayerDb.csv')  # Assuming PlayerDb is the modified class for football players
    app = PlayerGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()