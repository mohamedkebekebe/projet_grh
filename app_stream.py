import mysql.connector
import streamlit as st
import pandas as pd

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="gestion_rh",
    password="Cyvjy@7224",
    database="gestion de ressources humaines"
)
cursor = conn.cursor()

# Fonction pour exécuter une requête et retourner un DataFrame
def execute_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return pd.DataFrame(result, columns=columns)

# Interface avec Streamlit
st.title("Gestion des Ressources Humaines")

menu = ["Liste des employés avec poste et département", 
        "Salaire moyen par département", 
        "Nombre d'employés par département", 
        "Historique des paiements", 
        "Employés en congé",
        "salaire par contrat"]

choice = st.sidebar.selectbox("Menu", menu)

# Affichage des résultats en fonction du choix
if choice == "Liste des employés avec poste et département":
    query = """
    SELECT* from employe;
    """
    df = execute_query(query)
    st.write("Liste des employés avec leur poste et département")
    st.dataframe(df)

elif choice == "Salaire moyen par département":
    query = """
    SELECT departement.nom_departement, AVG(poste.salaire_associe) AS salaire_moyen
    FROM employe
    JOIN poste ON employe.id_poste = poste.id_poste
    JOIN departement ON employe.id_departement = departement.id_departement
    GROUP BY departement.nom_departement;
    """
    df = execute_query(query)
    st.write("Salaire moyen par département")
    st.dataframe(df)
    st.bar_chart(df.set_index('nom_departement'))

elif choice == "Nombre d'employés par département":
    query = """
    SELECT departement.nom_departement, COUNT(employe.id_employe) AS nombre_employes
    FROM employe
    JOIN departement ON employe.id_departement = departement.id_departement
    GROUP BY departement.nom_departement;
    """
    df = execute_query(query)
    st.write("Nombre d'employés par département")
    st.dataframe(df)

elif choice == "salaire par contrat":
    query = """
     SELECT SUM(salaire_base) AS MASSE_SALARIALE , type_contrat FROM contrat GROUP BY (type_contrat);
    """
    df = execute_query(query)
    st.write("salaire par contrat")
    st.dataframe(df)

   

elif choice == "Historique des paiements":
    query = """
    SELECT employe.nom, employe.prenom, payement.date_paiement, payement.montant
    FROM employe
    JOIN payement ON employe.id_employe = payement.id_employe;
    """
    df = execute_query(query)
    st.write("Historique des paiements des employés")
    st.dataframe(df)

elif choice == "Employés en congé":
    query = """
    SELECT employe.nom, employe.prenom, conge.type_conge, conge.date_debut, conge.date_fin
    FROM employe
    JOIN conge ON employe.id_employe = conge.id_employe;
    """
    df = execute_query(query)
    st.write("Liste des employés en congé")
    st.dataframe(df)

# Fermer le curseur et la connexion
cursor.close()
conn.close()
