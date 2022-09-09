#-*- coding: utf-8 -*-
import sys
import codecs
import nltk
import math
from nltk import bigrams

#utilizzo la funzione OrdinaDiz per ordinare i dieci bigrammi di POS con probabilità condizionata massima e forza associativa massima
#la funzione prende in input un dizionario e restituisce una lista di coppie (bigramma, probabilità condizionata) ordinate per probabilità condizionata oppure (bigramma, forza di associazione) ordinate per forza di associazione 
def OrdinaDiz(diz):
	return sorted(diz.items(), key=lambda x: x[1], reverse=True)

#definisco la funzione per trovare il numero delle parole nel testo 
def numeroparole(tokensTOT):
	numeroTOT = 0.0
	#calcolo la lunghezza delle parole
	for parola in tokensTOT:
		numeroTOT = numeroTOT + len(parola)
	return numeroTOT

#uso la funzione analisilinguistica per trovare avere il POS del testo, la funzione restituisce il testo tokenizzato e le coppie (parola, POS)
def analisilinguistica(frasi):
	tokenstot = []
	tokensPOStot = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensPOS = nltk.pos_tag(tokens)
		tokenstot= tokenstot+tokens
		tokensPOStot = tokensPOStot + tokensPOS
	return tokenstot,tokensPOStot

#uso la funzione POS per ottenere la lista degli elementi POS, la lista dei Sostantivi e la lista dei Verbi
def POS(testoanalisi):
	listaelementiPOS = []
	listaSostantivi = []
	listaVerbi = []
	for elemento in testoanalisi:
		#scorro gli elementi del testo e definisco il loro POS
		listaelementiPOS.append(elemento[1])
		if elemento[1]=="NN" or elemento[1]=="NNP" or elemento[1]=="NNS" or elemento[1]=="NNPS":
			#inserisco l'elemento sostantivo nella listaSostantivi
			listaSostantivi.append(elemento[0])
		if elemento[1]=="VB" or elemento[1]=="MD" or elemento[1]=="VBD" or elemento[1]=="VBZ" or elemento[1]=="VBP" or elemento[1]=="VBG" or elemento[1]=="VBN":
			#inserisco l'elemento verbo nella listaVerbi
			listaVerbi.append(elemento[0])
	return listaelementiPOS, listaSostantivi, listaVerbi

#uso la funzione StampaProbCondizionataMax per trovare la probabilità condizionata massima
def StampaProbCondizionataMax(bigrammi1, bigrammidiversi1, coppiePOS1):
	#definisco un dizionario
	DizBigrammi={}
	for bigramma in bigrammidiversi1:
		#calcolo la probabilità condizionata con il rapporto fra la frequenza del bigramma e la frequenza del primo elemento del bigramma 
		probCond=(bigrammi1.count(bigramma)*1.0)/(coppiePOS1.count(bigramma[0])*1.0)
		#utilizzo la struttura dati dizionario con chiave bigramma e con valore la probabilità condizionata
		DizBigrammi[bigramma]=probCond
	#chiamo la funzione che ordina il dizionario dal più grande al più piccolo
	listaOrdinata=OrdinaDiz(DizBigrammi)
	primi10=listaOrdinata[0:10]
	#restituisco i primi dieci bigrammi con probabilità condizionata massima
	return primi10

def StampaForzaAssociazioneMax(bigrammi1, bigrammidiversi1, coppiePOS1, tokensTotali):
	DizBig={}
	for bigramma in bigrammidiversi1:
		#calcolo la forza di associazione con il logaritimo in base due del rapporto fra la frequenza del bigramma per la cardinalità del corpus e la frequenza del primo elemento del bigramma per il secondo elemento del bigramma
		forzaass = (bigrammi1.count(bigramma)*tokensTotali*1.0)/(coppiePOS1.count(bigramma[0])*coppiePOS1.count(bigramma[1])*1.0)
		forzaAssociazione=math.log(forzaass, 2)
		#utilizzo la struttura dati dizionario con chiave bigramma e con valore forza di associazione 
		DizBig[bigramma]=forzaAssociazione
	#chiamo la funzione che ordina il dizionario dal più grande al più piccolo
	ordinabigrammi=OrdinaDiz(DizBig)
	stampoprimi10=ordinabigrammi[0:10]
	#restituisco i primi dieci bigrammi con probabilità condizionata massima
	return stampoprimi10

def main (file1, file2):
	#leggo i due file
	fileInput1 = codecs.open(file1,"r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#creo le due liste che conterranno il numero totale di tokens dei due testi
	tokensTOT = []
	tokens2TOT = []
	#carico il tokenizzatore
	sent_tokenizer = nltk.data.load ('tokenizers/punkt/english.pickle')
	#divido i due testi in frasi
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)
	#calcolo il numero delle frasi nelle metamorfosi
	x = len(frasi1)
	print "il numero delle frasi delle Metamorfosi è", x
	#calcolo il numero delle frasi in cuore di tenebra
	y = len(frasi2)
	print "il numero delle frasi di Cuore di tenebra è", y
	#calcolo numero dei tokens delle metamorfosi
	for frase in frasi1:
		tokens1 = nltk.word_tokenize(frase)
		tokensTOT = tokensTOT + tokens1
		numerotokens1 = len(tokensTOT)
	print "il numero dei tokens delle Metamorfosi è", numerotokens1 
	#calcolo numero dei tokens di cuore di tenebra
	for frase in frasi2:
		tokens2 = nltk.word_tokenize(frase)
		tokens2TOT = tokens2TOT + tokens2
		numerotokens2 = len(tokens2TOT)
	print "il  numero dei tokens di Cuore di tenebra è", numerotokens2
	#calcola la lunghezza media delle frasi in termini di tokens 
	lunghezzamedia_frasi1 = len(tokensTOT)/x
	print "lunghezza delle frasi in termini di tokens per le Metamorfosi",lunghezzamedia_frasi1
	lunghezzamedia_frasi2 = len(tokens2TOT)/y
	print "lunghezza delle frasi in termini di tokens per Cuore di tenebra", lunghezzamedia_frasi2
	#calcolo la lunghezza media delle parole in caratteri
	lunghezzaparole1 = numeroparole(tokensTOT)
	lunghezzaparole2 = numeroparole(tokens2TOT)
	print "lunghezza media delle parole in termini di caratteri per le Metamorfosi",lunghezzaparole1/len(tokensTOT)
	print "lunghezza media delle parole in termini di caratteri per Cuore di tenebra",lunghezzaparole2/len(tokens2TOT)
	#prendo tutti i tokens diversi dei due testi e calcolo la grandezza del vocabolario per entrambi
	vocabolario1 = set(tokensTOT)
	grandezzavocabolario1 = len(vocabolario1)
	vocabolario2 = set(tokens2TOT)
	grandezzavocabolario2 = len(vocabolario2)
	print "La grandezza del vocabolario delle Metamorfosi è", grandezzavocabolario1
	print "La grandezza del vocabolario di Cuore di Tenebra è", grandezzavocabolario2
	#calcolo la distribuzione degli hapax all'aumentare del corpus per porzioni incrementali di 1000 tokens per le metamorfosi
	aumento = 1000
	frequenza = 0
	lista = []
	listafinale = []
	#con un ciclo verico che la mia variabile sia sempre minore della lunghezza del testo
	while aumento<numerotokens1:
		#prendo una porzione del testo da 0 fino al valore della variabile
		lista = tokensTOT[0:aumento]
		listahapax = set(lista)
		#svuoto ogli volta la lista finale
		listafinale = []
		#scorro i token nella lista
		for tok in listahapax:
			#calcolo la frequenza dei token
			frequenza = lista.count(tok)
			#se la frequenza è 1 (sono hapax), li aggiungo alla lista finale
			if frequenza == 1:
				listafinale.append(tok)	
		print "il numero degli hapax delle Metamorfosi in", aumento, "tokens è", len(listafinale)
		aumento = aumento + 1000
		#aumento di nuovo la porzione di testo 
	#calcolo la distribuzione degli hapax all'aumentare del corpus per porzioni incrementali di 1000 tokens per cuore di tenebra
	aumento2 = 1000
	frequenza2 = 0
	lista2 = []
	listafinale2 = []
	#con un ciclo verico che la mia variabile sia sempre minore della lunghezza del testo
	while aumento2<numerotokens2:
		#prendo una porzione del testo da 0 fino al valore della variabile
		lista2 = tokens2TOT[0:aumento2]
		listahapax2 = set(lista2)
		#svuoto ogli volta la lista finale
		listafinale2 = []
		#scorro i token nella lista
		for tok in listahapax2:
			#calcolo la frequenza dei token
			frequenza2 = lista2.count(tok)
			#se la frequenza è 1 (sono hapax), li aggiungo alla lista finale
			if frequenza2 == 1:
				listafinale2.append(tok)
		print "il numero degli hapax di Cuore di tenebra in", aumento2, "tokens è", len(listafinale2)
		#aumento di nuovo la porzione di testo 
		aumento2 = aumento2 + 1000	
	#chiamo la funzione analisilinguistica per ottenere il POS dei due testi
	testoTokenizzato1, coppiePOS1 = analisilinguistica(frasi1)
	testoTokenizzato2, coppiePOS2 = analisilinguistica(frasi2)
	#chiamo la funzione POS per ottenere la lista dei verbi e dei sostantivi per ciascuno testo
	elementiPOS1,listaSostantivi1,listaVerbi1= POS(coppiePOS1)
	elementiPOS2,listaSostantivi2,listaVerbi2 = POS(coppiePOS2)
	#print "i sostantivi delle Metamorfosi sono", len(listaSostantivi1), "e i verbi", len(listaVerbi1)
	#print "i sostantivi di Cuore di tenebra sono", len(listaSostantivi2), "e i verbi", len(listaVerbi2)
	#faccio il rapporto tra sostantivi e verbi per le Metamorfosi
	rapportoSostantiviVerbi1 = len(listaSostantivi1)*1.0/len(listaVerbi1)*1.0
	print "Il rapporto tra sostantivi e verbi per le Metamorfosi è", rapportoSostantiviVerbi1
	#calcolo il rapporto tra sostantivi e verbi per Cuore di Tenebra
	rapportoSostantiviVerbi2 = len(listaSostantivi2)*1.0/len(listaVerbi2)*1.0
	print "Il rapporto tra sostantivi e verbi per Cuore di Tenebra è", rapportoSostantiviVerbi2
	#calcolo la frequenza dei POS delle metamorfosi
	frequenzaPOS1 = nltk.FreqDist(elementiPOS1)
	lunghezzafreq1 = len(frequenzaPOS1)
	#ordino la frequenza dei POS delle metamorfosi e stampo i 10 POS più frequenti
	ordinafreq1 = frequenzaPOS1.most_common(lunghezzafreq1)
	print "I dieci POS più frequenti delle Metamorfosi sono", ordinafreq1[0:10]
	#calcolo la frequenza dei POS di cuore di tenebra
	frequenzaaPOS2 = nltk.FreqDist(elementiPOS2)
	lunghezzafreq2 = len(frequenzaaPOS2)
	#ordino la frequenza dei POS di cuore di tenebra e stampo i 10 POS più frequenti
	ordinafreq2 = frequenzaaPOS2.most_common(lunghezzafreq2)
	print "I dieci POS più frequenti di Cuore di tenebra sono", ordinafreq1[0:10]
	#estraggo 10 bigrammi di POS per entrambi i testi 
	bigrammi1 = list(bigrams(coppiePOS1))
	bigrammi2 = list(bigrams(coppiePOS2))
	bigrammidiversi1 = set(bigrammi1)
	bigrammidiversi2 = set(bigrammi2)
	#calcolo la probabilità condizionata massima dei 10 bigrammi 
	Probabilitacondizionata1 = StampaProbCondizionataMax(bigrammi1, bigrammidiversi1, coppiePOS1)
	Probabilitacondizionata2 = StampaProbCondizionataMax(bigrammi2, bigrammidiversi2, coppiePOS2)
	print "La probabilità condizionata dei primi dieci bigrammi per le Metamorfosi è", Probabilitacondizionata1
	print "La probabilità condizionata dei primi dieci bigrammi per Cuore di tenebra è", Probabilitacondizionata2
	#calcolo la forza di associazione massima dei 10 bigrammi
	forzaAssociazione1 = StampaForzaAssociazioneMax(bigrammi1,bigrammidiversi1, coppiePOS1, len(tokensTOT))
	forzaAssociazione2 = StampaForzaAssociazioneMax(bigrammi2,bigrammidiversi2, coppiePOS2, len(tokens2TOT))
	print "La forza di associazione dei primi dieci bigrammi per le Metamorfosi è", forzaAssociazione1
	print "La forza di associazione dei primi dieci bigrammi per Cuore di tenebra è", forzaAssociazione2


	
main (sys.argv[1], sys.argv[2])