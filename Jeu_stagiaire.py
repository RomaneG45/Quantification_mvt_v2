import random

# Nombre mystère choisi entre 1 et 100
nombre_secret = random.randint(1, 100)
tentatives = 0

print("Bienvenue dans le jeu du 'Plus ou Moins' ! 🎲")
print("J'ai choisi un nombre entre 1 et 100. Devine-le...")

while True:
    try:
        guess = int(input("Ta proposition : "))
        tentatives += 1

        if guess < nombre_secret:
            print("C'est plus 🔼")
        elif guess > nombre_secret:
            print("C'est moins 🔽")
        else:
            print(f"Bravo 🎉 ! Tu as trouvé en {tentatives} tentative(s) !")
            break
    except ValueError:
        print("Entre un nombre valide, s'il te plaît !")
