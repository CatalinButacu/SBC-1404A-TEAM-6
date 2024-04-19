# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:25:34 2024

@author: Catalin.BUTACU
"""

import clips

env = clips.Environment() #crearea unei variabile de tip clips

env.clear() #clear echivalent celui din Clips
env.load("main.clp") #load la fisier (fisierul sa fie mai intai incarcat in colab)
env.reset() #reset echivalent celui din Clips
env.run() #run echivalent celui din Clips

facts = env.eval("(get-fact-list *)") #salvarea bazei de fapte intr-o variabila

print('######### Baza de fapte #########')
print(facts) #afisarea bazei de fapte
print('######### Afisare tip baza de fapte #########')
print(type(facts))
print('######### Afisarea bazei de fapte #########')

for fact in facts:
    print(fact)
