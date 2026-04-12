import fastf1

fastf1.Cache.enable_cache('cache') 

print("Chargement de la session de Bahreïn 2024...")
session = fastf1.get_session(2024, 'Bahrain', 'Q')
session.load()

print("Session chargée ! Récupération du tour de Max Verstappen...")
fast_ver = session.laps.pick_driver('VER').pick_fastest()

print(f"Temps du tour de Verstappen : {fast_ver['LapTime']}")