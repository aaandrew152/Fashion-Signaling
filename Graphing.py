'''
Graphing functions
'''
from matplotlib import pyplot as pl
import matplotlib.patches as mpatches

def get_sender_portion(population, strategy):
    num_senders = 0
    for sender in population:
        if sender == strategy:
            num_senders += 1
    portion = num_senders / len(population)
    return portion

def get_receiver_portion(population, strategy):
    num_receivers = 0
    for receiver in population:
        if receiver[strategy] == 1:
            num_receivers += 1
    portion = num_receivers / len(population)
    return portion 

def update_history(populations, history):
    for sender in range(2):
        for signal in range(3):
            portion = get_sender_portion(populations[sender], signal)
            history[sender][signal].append(portion)
    for receiver in range(2):
        for signal in range(4):
            portion = get_receiver_portion(populations[receiver+2], signal)
            history[receiver+2][signal].append(portion)
        
def plotting(time, plots, history):
    for sender in range(2):
        for signal in range(3):
            plots[sender].plot(range(time), history[sender][signal])
    for receiver in range(2):
        for signal in range(4):
            plots[receiver+2].plot(range(time), history[receiver+2][signal])
            
def prepare_plots():
    _, plots = pl.subplots(4, sharex=True, sharey=True, figsize=(18,10))
    
    plots[0].set_title("Low sender signal proportions")
    plots[1].set_title("High sender")
    plots[2].set_title("Low receiver acceptance")
    plots[3].set_title("High receiver")
    
    plots[0].set_ylabel("Proportions")
    plots[3].set_xlabel("Generations")
    
    no_signal_patch = mpatches.Patch(color='blue', label='Proportion accepting/sending no signal')
    normal_signal_patch = mpatches.Patch(color='green', label='Proportion accepting/sending normal signals')
    hidden_signal_patch = mpatches.Patch(color='red', label='Proportion accepting/sending hidden signals')
    invest_patch = mpatches.Patch(color='cyan', label='Proportion investing')
    
    pl.legend(handles=[no_signal_patch,normal_signal_patch,hidden_signal_patch,invest_patch],
              title='Legend', loc=3)
    
    return plots