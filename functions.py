def temps_moyen(intervalle: str) -> float:
    intervalle = intervalle.replace("h", '')
    intervalle = intervalle.replace(" -", '').split(' ')
    a = int(intervalle[0])
    b = int(intervalle[1])
    return (a+b)/2