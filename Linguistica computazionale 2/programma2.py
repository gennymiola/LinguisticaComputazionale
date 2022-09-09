# -*- coding: utf-8 -*-
import sys
import codecs
import nltk
import re 
from nltk import bigrams 
#analisi linguistica 
def AnalisiLinguistica(frasi):
	#inizializzo le liste vuote
	tokensTOT = []
	NamedEntityList = []
	tokensPOStot = []
	ListaLuoghi = []
	#divisione in frasi e analisi POS 
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensPOS = nltk.pos_tag(tokens)
		#analizzo il testo con NER
		analisi = nltk.ne_chunk(tokensPOS)
		for nodo in analisi: #scorro i nodi
			NE = ''
			if hasattr(nodo, 'label'):
				#verifico se il nodo intermedio è una persona
				if nodo.label() in ["PERSON"]:
					for partNE in nodo.leaves():
						NE = NE+''+partNE[0]
					#lo aggiungo alla lista dei nomi propri
					NamedEntityList.append(NE)
				#verifico se il nodo intermedio è un luogo
				if nodo.label() in ["GPE"]:
					for partNE in nodo.leaves():
						NE = NE+''+partNE[0]
					#lo aggiungo alla lista dei luoghi
					ListaLuoghi.append(NE)
		#restituisco i risultati
		tokensTOT = tokensTOT + tokens
		tokensPOStot = tokensPOStot + tokensPOS
	return tokensTOT, tokensPOStot, NamedEntityList, ListaLuoghi

#funzione per il calcolo della probabilità con modello di Markov
def Markov0(lunghezzacorpus, distribuzionedifrequenza, frase):
	probabilita=1.0
	for tok in frase:
		probabilitaToken = (distribuzionedifrequenza[tok]*1.0/lunghezzacorpus*1.0)
		probabilita = probabilita*probabilitaToken
	return probabilita

#uso la funzione analisilinguistica per trovare avere il POS del testo, la funzione restituisce il testo tokenizzato e le coppie (parola, POS)
def analisi(testodaanalizzare):
	tokenstot = []
	tokensPOStot = []
	for frase in testodaanalizzare:
		tokens = nltk.word_tokenize(frase)
		tokensPOS = nltk.pos_tag(tokens)
		tokenstot= tokenstot+tokens
		tokensPOStot = tokensPOStot + tokensPOS
	return tokenstot,tokensPOStot

#funzione per estrarre i verbi, sostantivi e nomi propri
def estraiPOS(testo):
	listaPOS = []
	listaSostantivi = []
	listaVerbi = []
	listaNomi = []
	for elemento in testo:
		listaPOS.append(elemento[1])
		#cerco i sostantivi
		if elemento[1]=="NN" or elemento[1]=="NNP" or elemento[1]=="NNS" or elemento[1]=="NNPS":
			listaSostantivi.append(elemento[0])
			#cerco i nomi propri
		if elemento[1]=="NNP":
			listaNomi.append(elemento[0])
			#cerco i verbi
		if elemento[1]=="VB" or elemento[1]=="VBZ" or elemento[1]=="VBP" or elemento[1]=="VBD" or elemento[1]=="VBN" or elemento[1]=="VBG" or elemento[1]=="MD":
			listaVerbi.append(elemento[0])
	return listaSostantivi, listaNomi, listaVerbi

def main(file1,file2):
	#leggo i due file
	fileInput1 = codecs.open(file1,'r','utf-8')
	fileInput2 = codecs.open(file2,'r','utf-8')
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#carico il tokenizzatore
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	#divido i testi in frasi
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)
	#chiamo la funzione analisilinguistica per ottenere la lista dei nomi propri e dei luoghi per le Metamorfosi
	TestoTokenizzato1, testoAnalizzatoPOS1, NamedEntityList1, ListaLuoghi1 = AnalisiLinguistica(frasi1)
	#chiamo la funzione analisilinguistica per ottenere la lista dei nomi propri e dei luoghi per Cuore di Tenebra
	TestoTokenizzato2, testoAnalizzatoPOS2, NamedEntityList2, ListaLuoghi2 = AnalisiLinguistica(frasi2)
	#calcolo la frequenza dei nomi propri delle Metamorfosi
	frequenzaNomipropri1 = nltk.FreqDist(NamedEntityList1)
	lenfrequenza1 = len(frequenzaNomipropri1)
	#ordino la frequenza dei nomi propri delle Metamorfosi e stampo i primi dieci più frequenti
	ordinaFreq1 = frequenzaNomipropri1.most_common(lenfrequenza1)
	print "I dieci nomi di persona più frequenti delle Metamorfosi sono", ordinaFreq1[0:10]
	#scorro i dieci nomi propri più frequenti delle Metamorfosi
	for elemento in ordinaFreq1[0:10]:
		listafrasi1 = []
		#creo un dizionario
		dizionario = {}
		#scorro tutte le frasi delle Metamorfosi, se uno dei dieci nomi propri è contenuto nella frase che sto scorrendo, aggiungo la frase alla lista delle frasi che contengono i 10 nomi propri più frequenti
		for frase in frasi1:
			if elemento[0] in frase:
				listafrasi1.append(frase)
				#creo un dizionario con chiave il nome proprio e valore la lista delle frasi associate a ciascun nome proprio
				dizionario[elemento[0]] = listafrasi1
				#stampo la lista delle frasi per ogni nome proprio
				print "il nome", elemento, "è contenuto in", frase
		#comincio tutte le analisi per ogni nome proprio delle Metamorfosi
		print "Analisi per il nome:", elemento
		#scorro le frasi nel dizionario
		for frase in dizionario:
			#ordino le frasi dalla più corta alla più lunga
			ordina = sorted(dizionario[frase], key=len, reverse=False)
			#stampo la prima frase (la più corta) e l'ultima (la più lunga) in cui compare ogni nome proprio
			print "la frase più corta in cui compare", elemento,"è:", ordina[0]
			print "la frase più lunga in cui compare", elemento,"è:", ordina[len(ordina)-1]
		#trovo i sostantivi, i nomi e i verbi 
		testoTokenizzato1, coppiePOS1 = analisi(listafrasi1)
		listaSostantivi1, listaNomi1, listaVerbi1 = estraiPOS(coppiePOS1)
		#calcolo la frequenza dei luoghi e stampo i primi dieci più frequenti
		frequenzaluoghi1 = nltk.FreqDist(ListaLuoghi1)
		lenfrequenzaluoghi1 = len(frequenzaluoghi1)
		ordinaFreqluoghi1 = frequenzaluoghi1.most_common(lenfrequenzaluoghi1)
		print "i dieci luoghi più frequenti per", elemento,"sono",ordinaFreqluoghi1[0:10]
		#calcolo la frequenza dei nomi e stampo i primi dieci più frequenti
		frequenzanomi1 = nltk.FreqDist(listaNomi1)
		lenfrequenzanomi1 = len(frequenzanomi1)
		ordinaFreqNomi1 = frequenzanomi1.most_common(lenfrequenzanomi1)
		print "le dieci persone più frequenti",elemento,"sono", ordinaFreqNomi1[0:10]
		#calcolo la frequenza dei sostantivi e stampo i primi dieci più frequenti
		frequenzasostantivi1 = nltk.FreqDist(listaSostantivi1)
		lenfrequenzasostantivi1 = len(frequenzasostantivi1)
		ordinaFreqSost1 = frequenzasostantivi1.most_common(lenfrequenzasostantivi1)
		print "i dieci sostantivi più frequenti per", elemento, "sono", ordinaFreqSost1[0:10]
		#calcolo la frequenza dei verbi e stampo i primi dieci più frequenti
		frequenzaverbi1 = nltk.FreqDist(listaVerbi1)
		lenfrequenzaverbi1 = len(frequenzaverbi1)
		ordinaFreqVerbi1 = frequenzaverbi1.most_common(lenfrequenzaverbi1)
		print "i dieci verbi più frequenti per",elemento,"sono", ordinaFreqVerbi1[0:10]
		#trovo le date i mesi e i giorni della settimana con le espressioni regolari 
		ListaDateMesiGiorni = []
		for line in listafrasi1: 
			ListaMatch = re.findall(r'[Ss]unday|[Ss]aturday|[Ff]riday|[Tt]hursday|[Ww]ednesday|[Tt]uesday|[Mm]onday|[Dd]icember|[Nn]ovember|[Oo]ctober|[Ss]eptember|[Aa]ugust|[Jj]uly|[Jj]une|[Mm]ay|[Aa]pril|[Mm]arch|[Ff]ebruary|[Jj]anuary|\s[0-3]?\d[-/][01]?\d[-/][0-2]?\d?\d?\d\s', line)
			for match in ListaMatch:
				ListaDateMesiGiorni.append(match)
				print "i mesi, i giorni e le date trovati per",elemento,"sono:", set(ListaDateMesiGiorni)
		#calcolo la lunghezza delle corpus delle Metamorfosi
		LunghezzaCorpus1 = len(TestoTokenizzato1)
		#calcolo la frequenza del corpus 
		frequenzaCorpus1 = nltk.FreqDist(TestoTokenizzato1)
		#scorro ogni frase fra quelle che contengono i dieci nomi propri più frequenti
		for frase in listafrasi1:
			#tokenizzo la frase
			tokensFrase1 = nltk.word_tokenize(frase)
			#se la lunghezza della frase è maggiore di 8 e minore di dodici, calcolo la probabilità di quella frase chiamando la funzione Markov0
			if len(tokensFrase1)>8 and len(tokensFrase1)<12:
				probabilita1 = Markov0(LunghezzaCorpus1, frequenzaCorpus1, tokensFrase1)
		print "la frase lunga minimo 8 token e massimo 12 con probabilità più alta per",elemento," è:' ",frase,"' e la sua probabilità è", probabilita1 
	#calcolo la frequenza dei nomi propri di Cuore di tenebra
	frequenzaNomipropri2 = nltk.FreqDist(NamedEntityList2)
	lenfrequenza2 = len(frequenzaNomipropri2)
	#ordino la frequenza dei nomi propri di Cuore di tenebra e stampo i primi dieci più frequenti
	ordinaFreq2 = frequenzaNomipropri2.most_common(lenfrequenza2)
	print "I dieci nomi di persona più frequenti di Cuore di tenebra sono", ordinaFreq2[0:10]
	#scorro i dieci nomi propri più frequenti di Cuore di Tenebra
	for elemento in ordinaFreq2[0:10]:
		#creo un dizionario
		dizionario2 = {}
		listafrasi2 = []
		#scorro tutte le frasi di Cuore di tenebra, se uno dei dieci nomi propri è contenuto nella frase che sto scorrendo, aggiungo la frase alla lista delle frasi che contengono i 10 nomi propri più frequenti
		for frase in frasi2:
			if elemento[0] in frase:
				listafrasi2.append(frase)
				#creo un dizionario con chiave il nome proprio e valore la lista delle frasi associate a ciascun nome proprio
				dizionario2[elemento[0]] = listafrasi2
				#stampo la lista delle frasi per ogni nome proprio
				print "il nome", elemento, "è contenuto in", frase
		#comincio tutte le analisi per ogni nome proprio di Cuore di tenebra
		print "Analisi per il nome:", elemento
		#scorro le frasi nel dizionario
		for frase in dizionario2:
			#ordino le frasi dalla più corta alla più lunga
			ordina = sorted(dizionario2[frase], key=len, reverse=False)
			#stampo la prima frase (la più corta) e l'ultima (la più lunga) in cui compare ogni nome proprio
			print "la frase più corta in cui compare", elemento,"è:", ordina[0]
			print "la frase più lunga in cui compare", elemento, "è:", ordina[len(ordina)-1]
		#trovo i sostantivi, i nomi e i verbi e stampo i primi dieci più frequenti
		testoTokenizzato2, coppiePOS2 = analisi(listafrasi2)
		listaSostantivi2, listaNomi2, listaVerbi2 = estraiPOS(coppiePOS2)
		#calcolo la frequenza dei luoghi e stampo i primi dieci più frequenti
		frequenzaluoghi2 = nltk.FreqDist(ListaLuoghi2)
		lenfrequenzaluoghi2 = len(frequenzaluoghi2)
		ordinaFreqluoghi2 = frequenzaluoghi2.most_common(lenfrequenzaluoghi2)
		print "i dieci luoghi più frequenti per",elemento,"sono", ordinaFreqluoghi2[0:10]
		#calcolo la frequenza dei nomi e stampo i primi dieci più frequenti
		frequenzanomi2 = nltk.FreqDist(listaNomi2)
		lenfrequenzanomi2 = len(frequenzanomi2)
		ordinaFreqNomi2 = frequenzanomi2.most_common(lenfrequenzanomi2)
		print "le dieci persone più frequenti per", elemento, "sono", ordinaFreqNomi2[0:10]
		#calcolo la frequenza dei sostantivi e stampo i primi dieci più frequenti
		frequenzasostantivi2 = nltk.FreqDist(listaSostantivi2)
		lenfrequenzasostantivi2 = len(frequenzasostantivi2)
		ordinaFreqSost2 = frequenzasostantivi1.most_common(lenfrequenzasostantivi2)
		print "i dieci sostantivi più frequenti per", elemento,"sono", ordinaFreqSost2[0:10]
		#calcolo la frequenza dei verbi e stampo i primi dieci più frequenti
		frequenzaverbi2 = nltk.FreqDist(listaVerbi2)
		lenfrequenzaverbi2 = len(frequenzaverbi2)
		ordinaFreqVerbi2 = frequenzaverbi2.most_common(lenfrequenzaverbi2)
		print "i dieci verbi più frequenti per",elemento,"sono", ordinaFreqVerbi2[0:10]
		#trovo le date i mesi e i giorni della settimana con le espressioni regolari 
		ListaDateMesiGiorni2 = []
		for line in listafrasi2:
			ListaMatch2 = re.findall(r'[Ss]unday|[Ss]aturday|[Ff]riday|[Tt]hursday|[Ww]ednesday|[Tt]uesday|[Mm]onday|[Dd]icember|[Nn]ovember|[Oo]ctober|[Ss]eptember|[Aa]ugust|[Jj]uly|[Jj]une|[Mm]ay|[Aa]pril|[Mm]arch|[Ff]ebruary|[Jj]anuary|\s[0-3]?\d[-/][01]?\d[-/][0-2]?\d?\d?\d\s', line)
			for match in ListaMatch2:
				ListaDateMesiGiorni2.append(match)
				print "i mesi e i giorni e le date per",elemento,"sono:", set(ListaDateMesiGiorni2)
		#calcolo la lunghezza del corpus di Cuore di tenebra
		LunghezzaCorpus2 = len(TestoTokenizzato2)
		#calcolo la frequenza del corpus
		frequenzaCorpus2 = nltk.FreqDist(TestoTokenizzato2)
		#scorro ogni frase fra quelle che contengono i dieci nomi propri più frequenti
		for frase in listafrasi2:
			#tokenizzo la frase
			tokensFrase2= nltk.word_tokenize(frase)
			#se la lunghezza della frase è maggiore di 8 e minore di dodici, calcolo la probabilità di quella frase chiamando la funzione Markov0
			if len(tokensFrase2)>8 and len(tokensFrase2)<12:
				probabilita2=Markov0(LunghezzaCorpus2, frequenzaCorpus2, tokensFrase2)
		print "la frase lunga minimo 8 token e massimo 12 con probabilità più alta per",elemento, "è:' ",frase,"' e la sua probabilità è", probabilita2


main(sys.argv[1], sys.argv[2])