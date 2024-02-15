from test_algo import *
"""
mesure d'ecart entre la distance_min et la distance_final
"""

def delta_distance(k):
    #k est le nombre de delta différent
    distances_finales=[]
    distances_min=[]

    gps_data = get_coord_gps()
    for l in range(k):
        casier =[random.choice(gps_data) for i in range(5)] #les adresses des casiers
        couple =[[random.choice(gps_data),random.choice(gps_data)] for i in range(10)] #un couple = une transacton acheteur vendeur, 10 transactions
        dispo = [2 for i in range(5)]

        temp_test = traite_file_test_distance(couple,dispo,casier)
        distances_finales.append(temp_test[1])
        distances_min.append(temp_test[0])
    return  distances_finales,distances_min


k = 10
itération = [i+1 for i in range(k)]
distances_final,distances_mini = delta_distance(k)
plt.title("comparaison des distances")
plt.plot(itération,distances_final,".",label="distance finale")
plt.plot(itération,distances_mini,".",label="distance minimal")
plt.xlabel("itération")
plt.ylabel("distance en m")
plt.legend()
plt.grid()
plt.show()
#moyenne des distances supplémentaire à parcourir pour chaque personne
moy = 0
for i in range(k):
    moy +=distances_final[i]-distances_mini[i]
moy = moy/(2*k)#chaque personne donc 2 par transaction
print("moyenne :",moy)