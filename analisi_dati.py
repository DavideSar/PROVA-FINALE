def main():
    file = None
    try:
        file = open("C:/Users/Esame/Desktop/ITS/Fondamenti di programmazione/PROVA FINALE/log_monitoraggio_25-07-2022.csv", "r")
    except:
        pass

    if file == None:
        print("Impossibile aprire file")
        return 1
    else:
        print("file opened, do your things here")

    file.close()
    return 0

if __name__ == "__main__":
    main()