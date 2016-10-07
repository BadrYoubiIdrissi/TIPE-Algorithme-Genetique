import tkinter as tk

from Source.Population import Population
from Source.Node import Node
import matplotlib.pyplot as plt
import numpy as np

class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        # On initialise la grille principale
        self.grid()
        # On laisse l'utilisateur changer les dimensions de la fenetre
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Le panneau du formulaire de création de la population
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=0, column=0)
        self.mainFrame.grid()

        self.popManagementForm = tk.Frame(self.mainFrame)
        self.popManagementForm.grid(row=0, column=0, padx=10, pady=10)
        self.popManagementForm.grid()

        self.popSizeEntry = {}
        self.popSizeEntry['text'] = tk.Label(self.popManagementForm, text="Enter population size : ")
        self.popSizeEntry['text'].grid(row=0, column=0, sticky="S", padx=10, pady=10)

        self.populationSize = tk.StringVar()
        self.popSizeEntry['entry'] = tk.Entry(self.popManagementForm, textvariable=self.populationSize)
        self.popSizeEntry['entry'].grid(row=0, column=1, padx=10, pady=10)
        self.popSizeEntry['entry'].bind("<Return>", self.onCreatePopulation)
        
        self.evolveButton = tk.Button(self.popManagementForm, text="Evolve", state = "disabled", command = self.onEvolve)
        self.evolveButton.grid(row=1, column = 0, padx=10)

        self.showBestIndButton = tk.Button(self.popManagementForm, text="Show best individual", state="disabled", command=self.onShowBestIndividual)
        self.showBestIndButton.grid(row=1, column=1, padx=10)
        
        self.status = tk.StringVar()
        self.statusLabel = tk.Label(self, bg='#aaaaaa', textvariable=self.status, anchor="w")
        self.statusLabel.grid(row=1, column=0, sticky="SEW")

    def onCreatePopulation(self, event):
        def target(x):
            return x**5+x**2+1

        self.status.set("Creating population ...")
        self.update()
        self.population = Population(int(self.populationSize.get()))
        self.population.setTarget(target)
        self.population.genRand(2, 5)
        self.status.set("Done.")

        self.evolveButton.configure(state="active")
        self.showBestIndButton.configure(state="active")

        self.populationInfoFrame = tk.Frame(self.mainFrame)
        self.populationInfoFrame.grid(row=1, column=0)
        self.grid()

        self.popSizeLabel = {}
        self.popSizeLabel['text'] = tk.Label(self.populationInfoFrame, text="Current population size ", anchor="w")
        self.popSizeLabel['text'].grid(row=0,column=0, padx=10, pady=10)
        self.popSizeLabel['value'] = tk.Label(self.populationInfoFrame, textvariable = self.populationSize, anchor="w")
        self.popSizeLabel['value'].grid(row=0, column=1, padx=10, pady=10)

        self.popGeneration = tk.StringVar(value=str(self.population.generationCount))
        self.popGenerationLabel = {}
        self.popGenerationLabel['text'] = tk.Label(self.populationInfoFrame, text="Current generation ", anchor="w")
        self.popGenerationLabel['text'].grid(row=1,column=0, padx=10, pady = 10, sticky = "W")
        self.popGenerationLabel['value'] = tk.Label(self.populationInfoFrame, textvariable = self.popGeneration, anchor="w")
        self.popGenerationLabel['value'].grid(row=1, column=1, padx=10, pady=10, sticky="W")

        self.popBestFitness = tk.StringVar(value=str(self.population.bestCurrentFitness()))
        self.popBestFitnessLabel = {}
        self.popBestFitnessLabel['text'] = tk.Label(self.populationInfoFrame, text="Current best fitness", anchor="w")
        self.popBestFitnessLabel['text'].grid(row=2, column=0, padx=10, pady=10, sticky="W")
        self.popBestFitnessLabel['value'] = tk.Label(self.populationInfoFrame, textvariable=self.popBestFitness, anchor="w")
        self.popBestFitnessLabel['value'].grid(row=2, column=1, padx=10, pady=10, sticky="W")
        
        self.popAverage = tk.StringVar(value=str(self.population.totalFitness()/self.population.size))
        self.popAverageFitnessLabel = {}
        self.popAverageFitnessLabel['text'] = tk.Label(self.populationInfoFrame, text="Average fitness", anchor="w")
        self.popAverageFitnessLabel['text'].grid(row=3, column=0, padx=10, pady=10, sticky="W")
        self.popAverageFitnessLabel['value'] = tk.Label(self.populationInfoFrame, textvariable=self.popAverage, anchor="w")
        self.popAverageFitnessLabel['value'].grid(row=3, column=1, padx=10, pady=10, sticky="W")
        
        self.popWorstFitness = tk.StringVar(value=str(self.population.worstCurrentFitness()))

        self.popWorstFitnessLabel = {}
        self.popAverageFitnessLabel['text'] = tk.Label(self.populationInfoFrame, text="Current worst fitness", anchor="w")
        self.popAverageFitnessLabel['text'].grid(row=4, column=0, padx=10, pady=10, sticky="W")
        self.popAverageFitnessLabel['value'] = tk.Label(self.populationInfoFrame, textvariable=self.popWorstFitness, anchor="w")
        self.popAverageFitnessLabel['value'].grid(row=4, column=1, padx=10, pady=10, sticky="W")


    def onEvolve(self):
        self.status.set("Evolving...")
        self.update()
        self.population.evolve()
        self.popGeneration.set(str(self.population.generationCount))
        self.popBestFitness.set(str(self.population.bestCurrentFitness()))
        self.popWorstFitness.set(str(self.population.worstCurrentFitness()))
        self.popAverage.set(str(self.population.totalFitness()/self.population.size))
        print(self.population.bestCurrentFitness())
        self.status.set("Done.")
        self.update()

    def onShowBestIndividual(self):
        print(self.population.bestIndividual(self.population.currentGeneration))
        X = np.linspace(-1, 1, 100)
        Y = [self.population.target(x) for x in X]
        plt.plot(X, Y, label="Target", marker="o")
        self.population.bestIndividual(self.population.currentGeneration).plotGraph()
        plt.show()

app = App(None)
app.title("Genetic Programming")
app.mainloop()
