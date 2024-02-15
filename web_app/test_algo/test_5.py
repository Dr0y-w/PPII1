from test_algo import *
"""
mesure du temps d'exec 1
"""

def temps_5():
    gps_data = get_coord_gps()
    process_time = []
    for k in range(1,10):
        casier =[random.choice(gps_data) for i in range(k)] #les adresses des casiers
        couple =[[random.choice(gps_data),random.choice(gps_data)] for i in range(10)] #un couple = une transacton acheteur vendeur, 10 transactions
        dispo = [20 for i in range(k)]#plus de disponibilite pour chaque casier que de transaction
        
        start = time.perf_counter()
        temp_test = traite_file_test_distance(couple,dispo,casier)
        end = time.perf_counter()-start
        process_time.append(end)
    return process_time

itération = [i+1 for i in range(1,10)]
process_time = temps_5()
plt.title("temps d'exécution de l'algorithme de backtracking en fonction du nombre de casier")
plt.plot(itération,process_time,".")
plt.xlabel("nombre de casier")
plt.ylabel("temps en seconde")
plt.legend()
plt.grid()
plt.show()