from test_algo import *
"""
temps total dans le cas de notre application
"""

def moyenne_temps(k):
    #k est le nombre de delta différent

    process_time = []
    gps_data = get_coord_gps()
    for l in range(k):
        casier =[random.choice(gps_data) for i in range(9)] #les adresses des casiers
        couple =[[random.choice(gps_data),random.choice(gps_data)] for i in range(10)] #un couple = une transacton acheteur vendeur, 10 transactions
        dispo = [20 for i in range(9)]

        start = time.perf_counter()
        traite_file_test_distance(couple,dispo,casier)
        end = time.perf_counter()-start
        process_time.append(end)

    return  process_time


k = 10
itération = [i+1 for i in range(k)]
process_time = moyenne_temps(k)
plt.title("temps pour le cas de notre application")
plt.plot(itération,process_time,".",)
plt.xlabel("itération")
plt.ylabel("temps en seconde")
plt.grid()
plt.show()