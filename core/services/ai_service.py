import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


class AiService:
    def __init__(self):
        # Cargar modelos y encoders al inicializar la clase
        self.kmeans_loaded = joblib.load('ai_models/art/kmeans_model.pkl')
        self.encoders = joblib.load('ai_models/art/encoders.pkl')
        self.label_encoder_gender = self.encoders['gender_encoder']
        self.label_encoder_country = self.encoders['country_encoder']
        self.xgboost_model = joblib.load('ai_models/art/xgboost_model.pkl')
        self.pipeline_rev_loaded = joblib.load(
            'ai_models/rev/pipeline_rev.pkl')
        self.pipeline_tic_loaded = joblib.load(
            'ai_models/rev/pipeline_tic.pkl')
        self.model_all_mini = SentenceTransformer('all-MiniLM-L6-v2')

    def processPopularity(self, data):
        # data es un diccionario con las claves: 'Gender', 'Age', 'Country', 'Followers', 'Genres'
        # 'Genres' debe ser una lista de géneros
        new_data = pd.DataFrame(data)

        # Convertir los géneros a listas únicas y en minúsculas
        new_data['Genres'] = new_data['Genres'].apply(
            lambda x: list(set([genre.strip().lower() for genre in x])))

        # Generar embeddings para los géneros nuevos
        def get_embeddings(genre_list):
            if len(genre_list) == 0:
                # Vector de ceros si no hay géneros
                return np.zeros(384, dtype=np.float32)
            else:
                embeddings = self.model_all_mini.encode(genre_list)
                return np.mean(embeddings, axis=0).astype(np.float32)

        new_data['Genres_embeddings'] = new_data['Genres'].apply(
            get_embeddings)

        # Convertir los embeddings a una matriz
        new_embeddings_matrix = np.vstack(
            new_data['Genres_embeddings'].values).astype(np.float32)

        # Predecir el clúster usando el modelo KMeans
        predicted_cluster = self.kmeans_loaded.predict(new_embeddings_matrix)

        # Asignar el clúster predicho
        new_data['Genre_clusters'] = predicted_cluster

        # Eliminar columnas temporales
        new_data = new_data.drop(
            columns=['Genres', 'Genres_embeddings'], axis=1)

        # Función para transformar nuevos valores con LabelEncoder
        def safe_transform(encoder, value, default_value=-1):
            if value in encoder.classes_:
                return encoder.transform([value])[0]
            else:
                print(
                    f"Valor no visto: {value}. Asignando valor predeterminado {default_value}.")
                return default_value

        # Aplicar los encoders a los nuevos datos
        new_data['Gender_encoded'] = new_data['Gender'].apply(
            lambda x: safe_transform(self.label_encoder_gender, x))
        new_data['Country_encoded'] = new_data['Country'].apply(
            lambda x: safe_transform(self.label_encoder_country, x))

        # Preparar los datos de entrada para el modelo XGBoost
        X_new = new_data[['Gender_encoded', 'Age',
                          'Country_encoded', 'Followers', 'Genre_clusters']]

        # Hacer la predicción de popularidad
        popularity_prediction = self.xgboost_model.predict(X_new)
        popularity_score = int(round(popularity_prediction[0], 0))

        print(f'Predicción de Popularidad: {popularity_score} / 100')

        return popularity_score

    def processTickets(self, data, popularity):
        # data es un diccionario con las claves: 'City', 'Country', 'Venue'
        # Agregamos la popularidad predicha al conjunto de datos
        data['Popularity'] = popularity
        nueva_entrada = pd.DataFrame(data)

        # Predecir Revenue
        prediccion_rev = self.pipeline_rev_loaded.predict(nueva_entrada)
        revenue_prediction = int(round(prediccion_rev[0], 2))
        print(f'Predicción de Revenue: {revenue_prediction} USD')

        # Predecir Tickets vendidos
        prediccion_tic = self.pipeline_tic_loaded.predict(nueva_entrada)
        tickets_prediction = int(round(prediccion_tic[0], 2))
        print(f'Predicción de Tickets a vender: {tickets_prediction}')

        # Calcular el precio por ticket
        if tickets_prediction != 0:
            price_per_ticket = revenue_prediction / tickets_prediction
        else:
            price_per_ticket = 0
        print(
            f"El precio por ticket promedio debe de ser: {price_per_ticket:.2f} USD")

        return {
            'Revenue': revenue_prediction,
            'TicketsSold': tickets_prediction,
            'PricePerTicket': round(price_per_ticket, 2)
        }
