from cProfile import label
from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from fonction import handle_rome, scrapper_formation

app = Flask(__name__)

#-----------------------------------------Préparation model et dataset---------------------------------------------------------

df_cluster_rome = pd.read_csv('df_cluster_rome_encode.csv')

model =  SentenceTransformer("dangvantuan/sentence-camembert-large")

df_cluster_rome['encoding_label'] = (df_cluster_rome['Libellé ROME'].head(100)).apply(lambda x : model.encode(x))

#-----------------------------------------------Page d'acceuil-----------------------------------------------------------------

@app.route('/', methods=['POST', 'GET'])
def table():

    return render_template('table.html')

#-----------------------------------------------Page recherche-----------------------------------------------------------------

@app.route('/handle_data', methods=['POST'])
def handle_data():

  projectpath = request.form['camenBERT']
  requete_code = model.encode(projectpath)
  laliste = []

  for i in list(df_cluster_rome['encoding_label'].head(100)):
    laliste.append(i) 

  score_cos = cosine_similarity([requete_code],laliste)
  score_cos = score_cos.tolist()

  d = {'sentence': df_cluster_rome['Libellé ROME'].head(100), 'score': score_cos[0]}
  df = pd.DataFrame(data=d)
  df = df.sort_values(by=['score'], ascending=False)

  return render_template('recherche.html', recherche_text=df.sentence.iloc[0:4].tolist())

#-----------------------------------------------Page formations----------------------------------------------------------------

@app.route('/search_rome', methods=['GET'])
def search_rome():

  label = request.args['label']
  data = pd.read_csv('df_cluster_rome_encode.csv', usecols=['code_ROME','Libellé ROME'])
  data = data[data['Libellé ROME']==label]

  return render_template('formation.html', rome_text=handle_rome(data['code_ROME'].iloc[0]))

#-----------------------------------------------Page detail sur formation------------------------------------------------------

@app.route('/search_formation', methods=['GET'])
def search_formation():

  formation = request.args['formation']

  return render_template('formation_detail.html', formation_text=scrapper_formation(formation))

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))