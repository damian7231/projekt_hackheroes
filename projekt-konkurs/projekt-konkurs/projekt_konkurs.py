#program oblicza jak najdokładniejsze prawdopodobieństwo wystąpienia danej choroby zadając przy tym jak najmniejszą ilość pytań użytkownikowi
import mysql.connector

#połączenie się z interesującą nas bazą danych
connection = mysql.connector.connect(user = 'root', password = 'root', host = '127.0.0.1', database = 'choroby', auth_plugin = 'mysql_native_password')

query = 'SELECT * FROM `chorobska` WHERE 1'

cursor = connection.cursor()
cursor.execute(query)

#lista wszystkich objawów
wszystkie_objawy = []
#lista występowań poszczególnych objawów po określeniu objawu
czeste_objawy = {}
#lista tych występować po określeniu objawu
czeste_objawy_lista = []
#lista zrobiona z całych list prawdopodobnych chorób 
prawdopodobne_choroby = []
#prawdopodobieństwo określenia danej choroby
procent_prawdopodobne_choroby = {}
#odrzucone objawy z danej choroby
wykorzystane_prawdopodobne_choroby = {}
#lista chorób z największą ilością trafnych objawów 
najtrafniejsze_choroby = []
#lista pogrupowanych objawów które okazały się prawdziwe bądź fałszywe
trafne_objawy = {}
#zmienna mówiąca o znalezieniu choroby
stop = True

#przeniesienie objawów z tablicy
for (row) in cursor:
	for i in range(2, len(row)):
		if wszystkie_objawy.count(row[i]) == 0:
			wszystkie_objawy.append(row[i])

#wyświetlenie dostępnych objawów
print("Wszystkie objawy w bazie danych to:")
print(wszystkie_objawy)

#pobranie od użytkownika objawu który znajduje się w bazie
while (True):
	objaw = input('\nZ wyżej wymienionych podaj dolegliwość która ci najbardziej doskwiera: ')
	if (wszystkie_objawy.count(objaw) > 0):
		break
	print('Nie posiadamy w bazie takiego objawu, spróbuj wprowadzić jeszcze raz')

cursor.execute(query)

#stworzenie słowników z występowaniem chorób, prawdopodopobieństwem choroby oraz ilości takich samych objawów 
for (row) in cursor:
	if row.count(objaw) > 0:
		procent_prawdopodobne_choroby.update({row[1] : 1})
		wykorzystane_prawdopodobne_choroby.update({row[1] : 0})
		dodaj = []
		for i in range(len(row)):
			dodaj.append(row[i])
			if(czeste_objawy.get(row[i]) == None and row[i] != objaw and i > 1):
				czeste_objawy.update({row[i] : 1})
				czeste_objawy_lista.append(row[i])
			elif(i > 1 and row[i] != objaw):
				czeste_objawy[row[i]] = czeste_objawy[row[i]] + 1
		prawdopodobne_choroby.append(dodaj)

#stworzenie pętli której warunkiem wyjścia jest osiągnięcie przez chorobę maksymalnego prawdopodobieństwa, bądź koniec powtarzających się możliwych objawów w liście
while (stop):
	#zbadanie najczęstrzego objawu
	najwieksza = 0
	for i in range(len(czeste_objawy_lista)):
		if(najwieksza < czeste_objawy[czeste_objawy_lista[i]]):
			najwieksza = czeste_objawy[czeste_objawy_lista[i]]
			najwiekszy = czeste_objawy_lista[i]
	
	#warunek sprawdzający czy istnieją jeszcze powtórzenia możliwych objawów
	if(najwieksza == 1):
		break
	#sprawdzenie czy objaw jest prawidłowy
	print('\nCzy posiadasz taki objaw jak: ', najwiekszy)
	posiada = input('Jeśli nie wpisz "n" bądź "N" natomiast jeśli tak dowolny inny znak: ')
	if(posiada == 'n' or posiada == 'N'):
		#usunięcie fałszywego objawu z listy
		del czeste_objawy[najwiekszy]
		del czeste_objawy_lista[czeste_objawy_lista.index(najwiekszy)]

		#pętla odrzucająca fałszywe objawy i choroby
		for i in range(len(prawdopodobne_choroby)):
			if prawdopodobne_choroby[i].count(najwiekszy) > 0:
				if(wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] == 1):
					#usunięcie mało prawdopodobnej choroby ze słownika
					del wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]
					for j in range(2,len(prawdopodobne_choroby[i])):
						if(czeste_objawy.get(prawdopodobne_choroby[i][j]) != None):
							if(czeste_objawy[prawdopodobne_choroby[i][j]] == 1):
								#usunięcie prawdobodobych objawów z listy gdy okażą się one nieprawdziwe
								del czeste_objawy[prawdopodobne_choroby[i][j]]
								del czeste_objawy_lista[czeste_objawy_lista.index(prawdopodobne_choroby[i][j])]
							else:
								#zmniejszeje wartości zapisanej w słowniku mówiącej o ilośici występowania prawdopodobnej choroby
								czeste_objawy[prawdopodobne_choroby[i][j]] -= 1
						
				else:
					#zwiększenie wartości słownika gdy ilość fałszywych objawów nie jest ona na tyle duża aby wykluczyć daną chorobę
					wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] += 1
	else:
		#usunięcie sprawdzonych już objawów
		del czeste_objawy[najwiekszy]
		del czeste_objawy_lista[czeste_objawy_lista.index(najwiekszy)]
		#zwiększenie prawdopodobieństwa dla chorób których objawy okazały się być prawdziwe
		for i in range(len(prawdopodobne_choroby)):
			if(prawdopodobne_choroby[i].count(najwiekszy) > 0):
				procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] += 1
for i in range(len(prawdopodobne_choroby)):
	if(wykorzystane_prawdopodobne_choroby.get(prawdopodobne_choroby[i][1]) != None):
		#sprawdzenie czy podana choroba ma maksymalną ilość trafnych objawów
		if(procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] == 5):
			stop = False
		#sprawdzenie czy nie zostały sprawdzone już wszystkie objawy z choroby
		if(procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] == 4 and wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]):
			del wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]


#stworzenie pętli której warunkiem wyjścia jest osiągnięcie przez chorobę maksymalnego prawdopodobieństwa, bądź koniec możliwych objawów
while(stop):
	licznik = 3
	if(len(wykorzystane_prawdopodobne_choroby) < 3):
		licznik = len(wykorzystane_prawdopodobne_choroby)
	for j in range(licznik):
		najwieksza = 0
		#sprawdzenie choroby posiadającej najwięcej trafnych objawów
		for i in range(len(prawdopodobne_choroby)):
			if(wykorzystane_prawdopodobne_choroby.get(prawdopodobne_choroby[i][1]) != None):
				if(najtrafniejsze_choroby.count(prawdopodobne_choroby[i][1]) == 0 and procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] > najwieksza):
					#ustalenie najprawdopodobniejszej choroby
					najwieksza = procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]
					najwiekszy = prawdopodobne_choroby[i][1]
		#dodanie najprawdopodobniejszych chorób do listy
		najtrafniejsze_choroby.append(najwiekszy)
	#warunek sprawdzający czy pozostały jakiekolwiek choroby do zweryfikowania
	if(len(najtrafniejsze_choroby) == 0):
		break
	licznik = 0
	#pętla sprawdzające najbardziej prawdopodobne choroby
	while licznik < len(najtrafniejsze_choroby):
		for i in range(len(prawdopodobne_choroby)):
			if(prawdopodobne_choroby[i].count(najtrafniejsze_choroby[licznik]) > 0):
				for j in range(2, len(prawdopodobne_choroby[i])):
					#przedstawienie użytkownikowi objawu oraz warto do niego przypisanej
					if(czeste_objawy_lista.count(prawdopodobne_choroby[i][j]) > 0):
						print('')
						print(prawdopodobne_choroby[i][j], ': ', 1 + licznik * 2)
						if(czeste_objawy[prawdopodobne_choroby[i][j]] == 1):
							#usunięcie użytych elementów z listy w przypadku gdy nie występują one w innych chorobach
							del czeste_objawy[prawdopodobne_choroby[i][j]]
							del czeste_objawy_lista[czeste_objawy_lista.index(prawdopodobne_choroby[i][j])]
						else:
							#zmniejszenie ilości występowania danego objawu
							czeste_objawy[prawdopodobne_choroby[i][j]] -= 1
						break
					#usunięcie z listy choroby w której sprawdzono wszystkie objawy
					elif(j == 6):
						del najtrafniejsze_choroby[licznik]
				break
		licznik += 1
	while(len(najtrafniejsze_choroby) > 0):
		print('')
		suma = int(input('Powyżej zostały rozpisane objawy wraz z cyframi, jeśli jakiś objaw cię dotyczy dodaj cyfrę przy nim stojącą do sumy oraz ją wypisz, jeśli żaden wpisz 0: '))
		#sprawdzanie czy suma podana przez użytkownika określająca objawy jest prawidłowa
		if(suma == 0 or suma == 1):
			break
		elif((suma == 3 or suma == 4) and len(najtrafniejsze_choroby) > 1):
			break
		elif((suma == 5 or suma == 6 or suma == 8 or suma == 9) and len(najtrafniejsze_choroby) == 3):
			break
		print('podana przez ciebie suma jest nieprawidłowa spróbuj ponownie')
	#sprawdzenie przez podaną przez użytkownika cyfrę które objawy są prawidłowe
	if(suma >= 5):
		trafne_objawy.update({najtrafniejsze_choroby[2] : 1})
	if(suma >= 3 and suma != 5 and suma != 6):
		trafne_objawy.update({najtrafniejsze_choroby[1] : 1})
	if(suma > 0 and suma != 3 and suma != 5 and suma != 8):
		trafne_objawy.update({najtrafniejsze_choroby[0] : 1})
	
	for licznik in range(len(najtrafniejsze_choroby)):
		if (trafne_objawy.get(najtrafniejsze_choroby[licznik]) != None):
			#dodawanie prawdopodobieństwa chorbie w przypadku potwierdzenia jej objawu
			procent_prawdopodobne_choroby[najtrafniejsze_choroby[licznik]] += 1
		else:
			#potwierdzenie bądź zwiększenie prawdopodobieństwa na fałszywość danej choroby
			if(wykorzystane_prawdopodobne_choroby[najtrafniejsze_choroby[licznik]] == 1):
				del wykorzystane_prawdopodobne_choroby[najtrafniejsze_choroby[licznik]]
			else:
				wykorzystane_prawdopodobne_choroby[najtrafniejsze_choroby[licznik]] += 1

	for i in range(len(prawdopodobne_choroby)):
		if(wykorzystane_prawdopodobne_choroby.get(prawdopodobne_choroby[i][1]) != None):
			#sprawdzenie czy podana choroba ma maksymalną ilość trafnych objawów
			if(procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] == 5):
				stop = False
			#sprawdzenie czy nie zostały sprawdzone już wszystkie objawy z choroby
			if(procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] == 4 and wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]):
				del wykorzystane_prawdopodobne_choroby[prawdopodobne_choroby[i][1]]
	najtrafniejsze_choroby.clear()
	trafne_objawy.clear()

#wyświetlenie końcowego prawdopodobieństwa 
print('\nPrawdopodobieństwo występowania danych chorób:')
for i in range(len(prawdopodobne_choroby)):
	if(procent_prawdopodobne_choroby.get(prawdopodobne_choroby[i][1]) != None):
		print(prawdopodobne_choroby[i][1], ': ', procent_prawdopodobne_choroby[prawdopodobne_choroby[i][1]] * 15, '%')
input('\nAby zakończyć naciśnij klawisz ENTER')

	

