import scipy.stats as stats
import numpy as np

# Données fictives (scores des métriques après Stage A et B)
stage_A = np.array([4, 1, 3, 4, 5])
stage_B = np.array([47, 51, 53, 49, 50])

# Définir la marge de non-infériorité
delta = -2  # Exemple : tolérance de 2 points

# Test t unilatéral
t_stat, p_value = stats.ttest_ind(stage_A, stage_B, alternative='less')  # Moins signifie non-infériorité

# Vérifier l'intervalle de confiance à 95%
IC_A = stats.t.interval(0.95, len(stage_A)-1, loc=np.mean(stage_A), scale=stats.sem(stage_A))
IC_B = stats.t.interval(0.95, len(stage_B)-1, loc=np.mean(stage_B), scale=stats.sem(stage_B))

# Résultat
print(f"IC Stage A : {IC_A}, IC Stage B : {IC_B}")
print(f"Valeur p du test de non-infériorité : {p_value}")

if np.mean(stage_A) - np.mean(stage_B) < delta and p_value < 0.05:
    print("Le Stage A est non inférieur au Stage B !")
else:
    print("Le Stage A pourrait être inférieur au Stage B.")
