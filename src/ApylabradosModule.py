
class Pawns():
    def __init__(self):
        self.letters = []
    def addPawn(self,c):
        self.letters.append(c)

    def addPawns(self,c,n): 
        for _ in range(n):
            self.addPawn(c)
    def createBag(self):
        import pandas as pd
        bag = pd.read_csv("bag_of_pawns-220320-111432.csv")
        for l in bag.itertuples():
            self.addPawns(l[1],l[2])
  
    def takeRandomPawn(self):
        import numpy as np
        l = np.random.choice(self.letters)
        self.letters.remove(l)
        return l
    def getFrequency(self):  
        """
        muestra la frecuencia de cada aparicion de cada ficha
        """
        fr = FrequencyTable()
        for n in self.letters:
            fr.update(n)
        return fr
    def showPawns(self):
        """
        muestra la fichas y el numero de veces que aparece cada ficha
        """
        fre_show = self.getFrequency()
        fre_show.showFrequency()

    def takePawn(self,c):
        """
        toma el valor c y la elimina de la bolas
        """
        self.letters.remove(c)
    
    def getTotalPawns(self):
        """
        devuenve cuantos letras quedan en la bolsa
        """
        return len(self.letters)
    ##  Clase 12
    points = {"A":1,"B":3,"C":3,"D":2,"E":1,"F":4,"G":2,"H":4,"I":1,"J":8,"K":5,"L":1,"M":3,"N":1,"O":1,"P":3,"Q":10,"R":1
              ,"S":1,"T":1,"U":1,"V":4,"W":4,"X":8,"Y":4,"Z":4}
    @staticmethod
    def getPoints(c):
        """
        devuelve los puntos de la ficha c
        """
        return Pawns.points[c]
    @staticmethod
    def showPawnsPoints():
        """
        Muestra la puntuacion de cada ficha
        """
        print("puntuacion de cada ficha")
        count = 0
        end = "  "
        for key in Pawns.points:
            print(f"{key}:"," " if Pawns.points[key]<9 else "",Pawns.points[key],end=end)
            count += 1
            end = "\n" if count %3 ==2 else " "
class Word(): 
    def __init__(self):
        self.word = []
    def __str__(self):
        r = ""
        for i in self.word:
            r +=i
        return r

    def areEqual(self,w):
        return self.word == w.word
    def isEmpty(self):
        if self.word == []:
            return True
        else:
            return False
    @classmethod
    def readWord(cls):
        palabra = input().strip()
        w = cls()
        for u in palabra.upper():
            w.word.append(u)
        return w
    
    def readWordFromFile(f):
        w = Word()
        file_word = f.readline()
        for i in file_word[:-1]:
            w.word.append(i)
        return w
    def getFrequency(self):
        """
        muestra la frecuencia de cada aparicion de cada letra que tiene la palabra
        """
        fr = FrequencyTable()
        for n in self.word:
            fr.update(n)
        return fr
    def getLengthWord(self):
        """
        devuelve la longutud de la palabra 
        """
        return len(self.word)
class Dictionary():
    
    filpath = "dictionary-220320-112137.txt"
    @staticmethod
    def validateWord(word):
        with open(Dictionary.filpath,mode="r") as f:
            w = Word.readWordFromFile(f)
            while (not w.isEmpty() and not word.areEqual(w)):
                w = Word.readWordFromFile(f)
            if w.isEmpty() and not word.areEqual(w):
                print("la palabra no se encuentra")
                return False
            else:
                return True
    @staticmethod
    def showWords(pawns):
        """
        muestra todas las posibles palabras que se pueden formar con dichas letras.
        """
        tf_pawns = pawns.getFrequency()
        with open(Dictionary.filpath,mode="r") as f:
            word = Word.readWordFromFile(f)
            count =0
            end = " "
            while (not word.isEmpty()):
                tf_word = word.getFrequency()
                if FrequencyTable.isSubset(tf_word,tf_pawns):
                    print(word,",",end=end)
                    count +=1
                    end = "\n" if count %4 ==2 else " "
                word = Word.readWordFromFile(f)

    @staticmethod
    def showWordPlus(pawns,c):
        """
        y muestra todas las posibles palabras que contienen el caracter c y que se pueden formar las fichas de pawns.
        """
        tf_pawns = pawns.getFrequency()
        tf_pawns.update(c)
        with open(Dictionary.filpath,mode="r") as f:
            word = Word.readWordFromFile(f)
            count =0
            end = " "
            while (not word.isEmpty()):
                if c in word.word:
                    tf_word = word.getFrequency()
                    if FrequencyTable.isSubset(tf_word,tf_pawns):
                        print(word,end=end)
                        count +=1
                        end = "\n" if count %4 ==2 else " "
                word = Word.readWordFromFile(f)

class FrequencyTable():
    import numpy as np
    def __init__(self):
        self.letters = [chr(x) for x in range(ord("A"),ord("Z")+1)]
        self.frequencies =[0 for _ in range(len(self.letters))]
        
    def showFrequency(self):
        for i in range(len(self.letters)):
            if self.frequencies[i] != 0:
                print(f"{self.letters[i]}: {self.frequencies[i]}")
    @staticmethod
    def isSubset(c1,c2):
        for u  in range(len(c1.frequencies)):
            if c1.frequencies[u] > c2.frequencies[u]:
                return False
        return True
    def update(self,c):
        """
        actualizar la frecuenda de la letra c agrega
        """
        idx = self.letters.index(c)
        self.frequencies[idx] += 1
    def delete(self,c):
        """
        actualizar la frecuenda de la letra c quita
        """
        idx = self.letters.index(c)
        self.frequencies[idx] -= 1
class Board():
    
    def __init__(self):
        self.board = [[" " for i in range(15)] for j in range(15)]
        self.totalWords =0
        self.totalPawns  = 0
        self.multiplier = [[(1,"") for _ in range(15)] for _ in range(15)] ## listas de lista con for
    def setUpMultiplier(self):
        """
        Configura el multiplicador de cada casilla
        """
        import pandas as pd
        filepath = "./multiplier_boardcsv-220320-113459.txt"
        multiplier = pd.read_csv(filepath)
        for row in multiplier.itertuples(): # iteramos fila a fila
            self.multiplier[row[1]][row[2]] = (row[3],row[4]) # asignamos 
    def showBoard(self):
        """
        Muestra el tablero
        """
        """
        long = len(self.board)
        print("\n", end=" ")
        for i in range(long):
            print(f"{0 if i <=9 else ''}{i}",end= "  ")
        print("\n+"+"---+"*long)
        for j in range(long):
            print("|",end=" ")
            for c in range(long):
                print(self.board[j][c]+" |",end =" ")
            print(f"{0 if j<=9 else ''}{j}",end=" ")
            print("\n+"+"---+"*long)
        """
        import pandas as pd 
        import numpy as np
        import matplotlib.pyplot as plt
            
        def genera_vetix(center_x,center_y):
            vertex = np.array([[center_x-0.5,center_y-0.5],[center_x-0.5,center_y+0.5],
                             [center_x+0.5,center_y+0.5],[center_x+0.5,center_y-0.5]])
            return vertex
        
        filepath = "./xycolor_board-220320-113241.csv"
        xycolor = pd.read_csv(filepath)
        
        # trasformacion lineal de [-1,16] a [0,1]
        def transformacion(x):
            return (x+1)/17
        # definimos la figura del tablero
        fig = plt.figure(figsize= [10,10])
        ax = fig.add_subplot(1,1,1)
        ## Dibujamos la rectas verticale y Horizontales
        for x in range(16):
            ax.plot([x,x],[0,15],'')
        for y in range(16):
            ax.plot([0,15],[y,y],'k')
        ## defuni los limites del plot
        ax.set_xlim([-1,16])
        ax.set_ylim([-1,16])
        ## escalamos para que la parrilla ocupe todo el espacio
        ax.set_position([0,0,1,1])
        # me desago del los ejes
        ax.set_axis_off()
        for row in xycolor.itertuples():
            poly = plt.Polygon(genera_vetix(row[1],row[2]),color=row[3])
            ax.add_artist(poly)
        for i in range(len(self.board)):
            # numeros de arriba
            ax.text(transformacion(i+0.5),transformacion(15.5),str(i),
                   verticalalignment = "center",horizontalalignment="center",
                   fontsize=20,fontweight="bold",transform=ax.transAxes)
            # nemeros de la derecha
            ax.text(transformacion(15.5),transformacion(i+0.5),str(14-i),
                   verticalalignment = "center",horizontalalignment="center",
                   fontsize=20,fontweight="bold",transform=ax.transAxes)
            # letras
            for j in range(len(self.board)):
                ax.text(transformacion(j+0.5),transformacion(14-i+0.5),self.board[i][j],
                   verticalalignment = "center",horizontalalignment="center",
                   fontsize=15,transform=ax.transAxes)
        ax.text(transformacion(0),transformacion(-0.5),f"score:{Board.score}",
                   verticalalignment = "center",horizontalalignment="left",
                   fontsize=24,fontweight="bold",transform=ax.transAxes)    
        deal7pawns()
        pawns_pos = 4
        for pawn in player_pawns.letters:
            circle = plt.Circle((pawns_pos, -0.6), 0.4, color = "#BF3EFF")
            ax.add_artist(circle)
            ax.text(transformacion(pawns_pos),transformacion(-0.6),pawn,
                   verticalalignment = "center",horizontalalignment="center",
                   fontsize=15,transform=ax.transAxes)
            pawns_pos +=1.5
        plt.show()
    score = 0           
    def placeWord(self,player_pawns,word,x,y,direction):
        
        """
        colocamos la palabre en el tablero y eliminamos la ficha de la bolsa
        """
        """
        for letter in word.word:
            if letter != self.board[x][y]:
                player_pawns.takePawn(letter)
                self.totalPawns +=1
                self.board[x][y] = letter
                Board.score += Pawns.getPoints(letter)
            if direction == "V":
                x += 1
            if direction == "H":
                y +=1
        self.totalWords +=1
        """
        word_points = 0
        word_multiplier = 1
        for letter in word.word:
            if letter != self.board[x][y]:
                player_pawns.takePawn(letter)
                self.totalPawns +=1
                self.board[x][y] = letter
                if self.multiplier[x][y][1] != "w" : # multiplicador de pawn o nada
                    word_points += Pawns.getPoints(letter) * self.multiplier[x][y][0]
                else: # multiplicador de word
                    word_points += Pawns.getPoints(letter)
                    word_multiplier *=  self.multiplier[x][y][0]
               
            if direction == "V":
                x += 1
            if direction == "H":
                y +=1
        Board.score += word_points * word_multiplier
        self.totalWords +=1
    def isPossible(self,word,x,y,direction):
        """
        esta comprobara si es posible pone la palabra en el tablero
        """
        mengs = ""
        x0 = x
        y0 = y
        # primera condicion: La primera palabra debe tener al menos una ficha situada en la casilla central
        if self.totalWords == 0:
            mengs = "la Palabra no pasa por la casilla central"
            if direction == "V":
                if y0 != 7:
                    return (False,mengs)
                elif x0+word.getLengthWord()-1<7 or x0>7:
                    return (False,mengs)
            if direction == "H":
                if x0 != 7:
                    return (False,mengs)
                elif y0+word.getLengthWord()-1<7 or y0 > 7:
                    return (False,mengs)
        # seg_condicion: La palabra no puede salirse de los límites del tablero.
        else:
            if x0 > 15 or x0 <0 or y0<0 or y0>15:
                mengs = "La cordenadas se salen del tablero"
                return (False,mengs)
            if direction == "V" and  (x0+word.getLengthWord()-1 >=15):
                return (False,mengs)
            if direction == "H" and  (y0+word.getLengthWord()-1 >=15):
                return (False,mengs)
            # tree_condicion: Todas las palabras, a excepción de la primera, deben usar una ficha ya existente en el tablero.
            x = x0
            y = y0
            ls = []
            for u in word.word:
                if self.board[x][y] == " ":
                    ls.append(u)
                    
                if direction =="V":
                    x +=1
                if direction == "H":
                    y +=1
            if len(ls) == word.getLengthWord():
                mengs = "No se esta untilizando ninguna letra del tablero"
                return (False,mengs)
            # four_condition: No se puede situar una ficha en una casilla ya ocupada por otra ficha diferente.
            x = x0
            y = y0
        
            for i in word.word:
                if self.board[x][y] != " " and i != self.board[x][y]:
                    mengs = "una casilla ya esta opuda por otra letra"
                    return (False,mengs)
                if direction == "V":
                    x+=1
                if direction == "H":
                    y +=1
            #five_condition: Hay que colocar al menos una nueva ficha en el tablero
            x = x0
            y = y0
            ls = []
            for u in word.word:
                if self.board[x][y] == u:
                    ls.append(u)
                if direction =="V":
                    x +=1
                if direction == "H":
                    y +=1
            if len(ls) == word.getLengthWord():
                mengs = "No se esta usando ninguna ficha nueva en el tablero"
                return (False,mengs)
            #six_condition: No puede haber una ficha al principio o al final de la palabra que se vaya a colocar sobre el tablero si ésta no pertenece a la palabra
            x,y = x0,y0
            mengs = "existe ficha adicionales al inicio o al final de la palabra"
            if direction =="V" and ((x!=0 and self.board[x-1][y] != " ") or (x+word.getLengthWord() != 14 and self.board[x+word.getLengthWord()][y] != " " )):
                return (False,mengs)
            if direction =="H" and ((y!=0 and self.board[x][y-1] != " ") or (y+word.getLengthWord()!=14 and self.board[x][y+word.getLengthWord()] != " " )):
                return (False,mengs)
        mengs = "la palabra se puede situal correctamente"
        return (True,mengs)
    
    def getPawns(self,word,x,y,direction):
        """
        devuelve la letras necesaria para crear la palabra proporcionada
        """
        need_letters = Word()
        isposible,mengs = self.isPossible(word,x,y,direction)
        if not isposible:
            print(mengs)
        else:
            for c in word.word:
                if self.board[x][y] !=c:
                    need_letters.word.append(c)
                if direction == "V":
                    x +=1
                if direction == "H":
                    y +=1
        return need_letters
    def showWordPlacement(self,pawns,word):
        """
        dada la ficha de jugado y la palabra determinaremos cual puede ser su colocacion 
        """
        for direction in ["V","H"]:
            print("vertical" if direction =="V" else "Horizontal")
            for i in range(15):
                for j in range(15):
                    if self.isPossible(word,i,j,direction)[0]==True:
                        needed_pawns = self.getPawns(word,i,j,direction)
                        if FrequencyTable.isSubset(needed_pawns.getFrequency(),pawns.getFrequency()):
                            print(f"x: {i}, y: {j}")
## clase 13 end
### funcion de start
def startGame():
    """
    inicia todas la variables y comienza el juego
    """
    # valirables booleanas end, show_helpe, show_helpe_plus
    global end
    end = False
    global show_help
    show_help = True
    global show_help_plus
    show_help_plus =True
    # Creo la bolsa de fichas del juego
    global bag_of_pawns
    bag_of_pawns = Pawns()
    bag_of_pawns.createBag()
    # Creo la fichas del juego
    global player_pawns
    player_pawns = Pawns()
    #creo el tablero del juego e inicializamos puntuacion en 0
    global board 
    board = Board()
    board.score = 0
    board.setUpMultiplier()
    
    
    welcome()
    instrucciones()
    deal7pawns()
    board.showBoard()
    legend()
    
## la funcion del del texto de Bienvendida
def welcome():
    """
    Muestra el mensage de Bienvenida
    """
    filepath = "./welcome_megs.txt"
    with open(filepath,mode="r") as f:
        print(f.read())
def instrucciones():
    """
    Muestra la reglas del Juego
    """
    filepath = "./instrucciones_megs.txt"
    with open(filepath,mode="r") as f:
        print(f.read())
def deal7pawns():
    """
    Reparte 7  fichas al jugador 
    """
    while (player_pawns.getTotalPawns() <7):
        player_pawns.addPawn(bag_of_pawns.takeRandomPawn())
   # print("Estas son tus fichas")
   # player_pawns.showPawns()
        
def showOption():
    """
    Muestra la opciones en caso de que todavía no haya palabras introducidas
    """
    global show_help
    filepath = "./option_megs.txt"
    print("¿Que deseas hacer ? ","" if show_help else "(introduce SHOWHELP para ver las opciones)")
    
    if show_help :
        with open(filepath,mode="r") as f:
            print(f.read())
            
        show_help = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help = True
        showOption()
    elif ans == "ENTERWORD":
        introduceNewWord() ## valta definir
    elif ans ==  "MYPAWNS":
        print("Estas son tus fichas")
        player_pawns.showPawns()
        showOption()
    elif ans == "MYSCORE":
        print(f"tu puntuacion es: {Board.score}")
        showOption()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOption()
    elif ans == "HELPWORD":
        helpWithWords()
        showOption()
    elif ans == "HELPLEGEND":
        legend()
        showOption()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOption()
def showOptionsPlus():
    """
    muestra opciones cuando se proporciona una palabra para colocar en el tablero
    """
    global show_help_plus
    filepath = "./option_plus_megs.txt"
    print("¿Que deseas hacer ? ","" if show_help_plus else "(introduce SHOWHELP para ver las opciones)")
    
    if show_help_plus :
        with open(filepath,mode="r") as f:
            print(f.read())
            
        show_help_plus = False
    ans = input().upper()
    if ans == "SHOWHELP":
        show_help_plus = True
        showOptionsPlus()
    elif ans == "ENTERPOSITION":
        introduceCoordinatesAndDirection()
    elif ans == "ENTERWORD":
        introduceNewWord() ## valta definir
    elif ans ==  "MYPAWNS":
        print("Estas son tus fichas")
        player_pawns.showPawns()
        showOptionsPlus()
    elif ans == "MYSCORE":
        print(f"tu puntuacion es: {Board.score}")
        showOptionsPlus()
    elif ans == "PAWNSPOINTS":
        Pawns.showPawnsPoints()
        showOptionsPlus()
    elif ans == "HELPWORD":
        helpWithWords()
        showOptionsPlus()
    elif ans == "HELPPOS":
        helpWithPosition()
        showOptionsPlus()
    elif ans == "HELPLEGEND":
        legend()
        showOptionsPlus()
    elif ans == "QUITGAME":
        endGame()
    else:
        showOptionsPlus()
        
        
def helpWithWords():
    """
    Muestra la posibles palabras que se pueden formar con la fichas del jugador
    y las que ya estan colocadas en el tablero
    """
    print("Estas son tus posibles palabras a formar: ")
    if board.totalWords == 0:
        Dictionary.showWords(player_pawns)
    else:
        board_letters = []
        for i in range(15):
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    Dictionary.showWordPlus(player_pawns,board.board[i][j])
                    
def helpWithPosition():
    """
    Muestra las posibles posiciones de la palabra en el tablero
    """
    print("estas son la posibles posiciones de tu palabra")
    board.showWordPlacement(player_pawns,new_word)
                
def introduceNewWord():
    """
    permite indroducir una palabra por consola y comprueba si existe en el diccionario
    teniendo encuenta la ficha del jugador y la posicion
    """
    print("Introduce tu palabra:")
    global new_word
    new_word = Word.readWord()
    new_word_ft = new_word.getFrequency()
    player_pawns_ft = player_pawns.getFrequency()
    isInDictionary = Dictionary.validateWord(new_word)
    
    if board.totalWords ==0:
        newWordIsSubset = FrequencyTable.isSubset(new_word_ft,player_pawns_ft)
    else:
        board_letters = []
        forceBreak = False
        for i in range(15):
            if forceBreak:
                break
            for j in range(15):
                if board.board[i][j] != " " and board.board[i][j] not in board_letters:
                    board_letters.append(board.board[i][j])
                    player_pawns_plus = player_pawns_ft
                    player_pawns_plus.update(board.board[i][j])
                    newWordIsSubset = FrequencyTable.isSubset(new_word_ft,player_pawns_plus)
                    player_pawns_plus.delete(board.board[i][j])
                                        
                    if newWordIsSubset:
                        forceBreak = True
                        break
    if not isInDictionary or not newWordIsSubset:
        if not newWordIsSubset:
            print("NO puedes formar la palabra con tus fichas")
            showOption()
    else:
        showOptionsPlus()

def introduceCoordinatesAndDirection():
    """
    permite introducir  coordenada y a direccion de una palabra luego compruba si dicha
    palabra se puede ubicar
    """
    x = int(input("Indroduce coordenada de la fila: "))                
    y = int(input("Indroduce coordenada de la columna: "))                    
    direction = input("Indroduce la direccion: ").upper()                   
    if direction != "V" and direction != "H":
        print("recuerda que solo tienes dos opciones V (vertical) H (horizontal)")
        showOptionsPlus()
    posible, mengs = board.isPossible(new_word,x,y,direction)
    if not posible:
        print(mengs)
        showOptionsPlus()
    else:
        needed_pawns = board.getPawns(new_word,x,y,direction)
        if FrequencyTable.isSubset(needed_pawns.getFrequency(),player_pawns.getFrequency()):
            board.placeWord(player_pawns,new_word,x,y,direction)
            board.showBoard()
            print(f"puntos: {Board.score}")
        else:
            print("La fichas que dispones No son sufucientes")
            showOptionsPlus()
def legend():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    def genera_vetix(center_x,center_y):
            vertex = np.array([[center_x-0.5,center_y-0.5],[center_x-0.5,center_y+0.5],
                             [center_x+0.5,center_y+0.5],[center_x+0.5,center_y-0.5]])
            return vertex
    def transformacionX(x):
            return x/16
    def transformacionY(x):
            return (x+1)/3
    fig = plt.figure(figsize = [10,2])
    ax = fig.add_subplot(1,1,1)
    
    ax.set_xlim(0,16)
    ax.set_ylim(-1,2)
    ## escalamos para que la parrilla ocupe toda 
    ax.set_position([0,0,1,1])
    ## eliminamos los ejes
    ax.set_axis_off()
    
    color = ['#FFCCCC', '#B2FFCD', '#CCCEFF', '#CCF9FF']
    for i in range(4):
        poly = plt.Polygon(genera_vetix(1.5+4*i,0.5),color = color[i])
        ax.add_artist(poly)
    ax.text(transformacionX(3.5),transformacionY(0.5),"x3\nPalabra",
           verticalalignment = "center",horizontalalignment="center",
                   fontsize=25,transform=ax.transAxes)
    ax.text(transformacionX(7.5),transformacionY(0.5),"x2\nPalabra",
           verticalalignment = "center",horizontalalignment="center",
                   fontsize=25,transform=ax.transAxes)
    ax.text(transformacionX(11.5),transformacionY(0.5),"x3\nLetra",
           verticalalignment = "center",horizontalalignment="center",
                   fontsize=25,transform=ax.transAxes)
    ax.text(transformacionX(15.5),transformacionY(0.5),"x2\nLetra",
           verticalalignment = "center",horizontalalignment="center",
                   fontsize=25,transform=ax.transAxes)
    plt.show()
def endGame():
    """
    finaliza partida
    """
    print("Fin del Juego")
    global end
    end = True