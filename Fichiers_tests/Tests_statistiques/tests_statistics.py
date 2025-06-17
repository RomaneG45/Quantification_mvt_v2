import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

"""1 métrique est testée (UR) : la différence entre un enfant d'HABIT et 1 enfant de PARTNER est significative si la p-value est > 0.05"""

# Chargement des données
df = pd.read_csv("C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Tests_statistic/tableau_metriques.csv")

# Pivot pour avoir les deux groupes côte à côte par paire
df_pivot = df.pivot(index="paire_id", columns="groupe", values="use_ratio")
df_pivot.columns = ['Therapie_A', 'Therapie_B']

# Visualisation de la distribution des différences
df_pivot['diff'] = df_pivot['Therapie_A'] - df_pivot['Therapie_B']
sns.histplot(df_pivot['diff'], kde=True)
plt.title("Distribution des différences entre les deux thérapies")
plt.xlabel("Différence Use Ratio (A - B)")
plt.show()

# Test de normalité (Shapiro-Wilk)
stat, p_normality = stats.shapiro(df_pivot['diff'])
print(f"Test de normalité (Shapiro-Wilk) p = {p_normality:.4f}")

# Choix du test statistique
if p_normality > 0.05:
    print("Données normales → test t apparié")
    stat, p_value = stats.ttest_rel(df_pivot['Therapie_A'], df_pivot['Therapie_B'])
else:
    print("Données non normales → test de Wilcoxon")
    stat, p_value = stats.wilcoxon(df_pivot['Therapie_A'], df_pivot['Therapie_B'])

print(f"Statistique = {stat:.4f}, p-value = {p_value:.4f}")
