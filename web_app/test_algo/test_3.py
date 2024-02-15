from test_algo import *
"""
test dans le cas de base de l'algo de backtracking
"""

def test_3():
    correction = True
    gps_data = get_coord_gps()
    for k in range(1,10):
        casier =[random.choice(gps_data) for i in range(k)] #les adresses des casiers
        couple =[[random.choice(gps_data),random.choice(gps_data)] for i in range(10)] #un couple = une transacton acheteur vendeur, 10 transactions
        dispo = [20 for i in range(k)]#plus de disponibilite pour chaque casier que de transaction 

        temp_test = traite_file_test_distance(couple,dispo,casier)
        if not(temp_test[0]==temp_test[1]):
            correction = False#le test échoue, on stop avant la fin pour économiser des appels api
            assert correction
    
    assert correction

