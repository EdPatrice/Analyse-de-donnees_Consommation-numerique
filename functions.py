def temps_moyen(intervalle: str) -> float:
    intervalle = intervalle.replace("h", '')
    intervalle = intervalle.replace(" -", '').split(' ')
    a = int(intervalle[0])
    b = int(intervalle[1])
    return (a+b)/2

# fonction de convertion en minutes
def convert (time_str) : 
    try : 
        if "<" in time_str:
            return 0.5
        start, end = time_str.split('-') 
        start_h = int(start.replace('h', '')) 
        end_h = int(end.replace('h','')) # on enlève le 'h' et on convertit en int
        duration = (start_h + end_h)/2 # calcul de la durée en heures
        return duration 
    except :
        return 0