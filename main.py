from pyswip import Prolog
prolog = Prolog()
prolog.consult('laberinto.pl')

camino = []

def leer(nombre_archivo):
  return [line.splitlines() for line in (open(nombre_archivo, "r"))] 
  
def arreglar(lista):
  return [i[0].split() for i in lista] 

def get_laberinto(nombre_archivo):
  return arreglar(leer(nombre_archivo))

def buscar(x, y, matriz):
  if matriz[x][y] == 'f':
      #print ("Encontrado! %d,%d" % (x, y))
      camino.append(['f'])
      return True
  elif matriz[x][y] == '|':
      #print ('no puedo %d,%d' % (x, y))
      return False
  elif matriz[x][y] == '-':
      #print ('no puedo %d,%d' % (x, y))
      return False
  elif matriz[x][y] == '▄':
      #print ('ya estuve %d,%d' % (x, y))
      return False
  else: camino.append([matriz[x][y]])

  #print ('actual %d,%d' % (x, y))
  
  matriz[x][y] = '▄'
  if ((x < len(matriz)-1 and buscar(x+1, y,matriz)) or (y > 0 and buscar(x, y-1,matriz)) or (x > 0 and buscar(x-1, y,matriz)) or (y < len(matriz[0])-1 and buscar(x, y+1,matriz))):
    return True
  return False

def init(lista, matriz):
  if(buscar(lista[0], lista[1], matriz)):
    print("SOLUCIONADO!")
  else : print(":(")

def buscar_inicio(matriz,cont):
    if matriz == []:
        return (-1,-1)
    if "i" in matriz[0]: 
        return ([cont,matriz[0].index("i")])
    return buscar_inicio(matriz[1:],cont+1)

def generar_hechos(camino):
  for x in range(0 , len(camino) - 1):
    prolog.assertz("conecta(%s,%s)" % (camino[x][0], camino[x+1][0]))
  
lab = get_laberinto("laberinto-in.txt")
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in lab])) 

init(buscar_inicio(lab,0),lab)
generar_hechos(list(filter(lambda a: a != ['*'], camino)))
sol = list(prolog.query("sol"))
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in lab])) 
