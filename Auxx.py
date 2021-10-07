import pandas as pd


# Funciones Auxiliares
def load_dataset(file):
    dataframe = pd.read_csv(file)
    return dataframe


######################## PRE PROCESSING ##########################
'''
    Construir las siguientes matrices, donde valores inexistentes son NaN:
    Matriz que represente las calificaciones de todos los usuarios para cada sitio turístico.
    Matriz que represente las preferencias de todos los usuarios para cada subcategoría de sitio turístico.
    Matriz que represente la relación de todas las subcategorías con cada usuario.
    '''


def buildMatrices(item, subcategory, user):
    item_matrix = item.pivot_table(index=['user_id'], columns=['item_id'], values='item_rating')
    subcategory_matrix = subcategory.pivot_table(index=['user_ids'], columns=['subCategory_ids'],
                                                 values='subCategory_ratings')
    user_matrix = user.pivot_table(index=['subCategory_ids'], columns=['user_ids'],
                                   values='subCategory_ratings')
    return item_matrix, subcategory_matrix, user_matrix


# Limpiar ruido (campos nulos y columnas con números de valores menor a un umbral).
def cleanNoise(item, subcategory, user):
    item_matrix = item.dropna(thresh=0, axis=1).fillna(0)
    subcategory_matrix = subcategory.dropna(thresh=0, axis=1).fillna(0)
    user_matrix = user.dropna(thresh=0, axis=1).fillna(0)
    return item_matrix, subcategory_matrix, user_matrix


######################## TRAINING ###############################
# MATRIZ DE SIMILITUD (Correlación de Pearson)
def computeSimilarityMatrices(item, subcategory, user):
    item_similarity_matrix = item.corr(method='pearson')
    subcategory_similarity_matrix = subcategory.corr().fillna(0)
    user_similarity_matrix = user.corr(method='pearson')

    # GUARDAR MATRIZ EN CSV
    item_similarity_matrix.to_pickle('item_similarity_matrix.pkt')
    subcategory_similarity_matrix.to_pickle('subcategory_similarity_matrix.pkt')
    user_similarity_matrix.to_pickle('user_similarity_matrix.pkt')

    return item_similarity_matrix, subcategory_similarity_matrix, user_similarity_matrix


################## QUERIES ################## QUERIES ################## QUERIES ################## QUERIES

# Lugares Turísticos

# Recomendar sitios turísticos a un usuario, en base a su registro histórico de ratings sobre sitios turísticos
# get_similar_places INPUT:
'''
# Usuario - fake data
# Definir ratings de los lugares turisticos del usuario 
user_places_ratings = [
    (1, 5),
    (485, 3),
    (389, 2),
    (456, 4),
    (245, 3),
    (367, 5),
    (563, 1),
]

get_similar_places(usuario1, item_similarity_matrix, 10, False)
'''


def get_similar_places(user_data, item_similarity_matrix, size, places, tabulate=False):

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(item_similarity_matrix)
        print(item_similarity_matrix.shape)

    similar_items = pd.DataFrame()
    for item_id, user_rating in user_data:
        print(item_id)
        similar_score = item_similarity_matrix[item_id] * (user_rating - 2.5)
        similar_score = similar_score.sort_values(ascending=False)
        similar_items = similar_items.append(similar_score)
    similar_items_data = similar_items.sum().sort_values(ascending=False)
    indices = similar_items_data.to_frame().index.values.tolist()
    values = similar_items_data.to_frame().values

    recommendation_list = []

    if tabulate == True:
        for i, value in enumerate(values[:size]):
            recommendation_list.append([indices[i], places.iloc[indices[i] - 1, 5], float(value)])
        rec_dataframe = pd.DataFrame(recommendation_list)
        rec_dataframe.columns = ['ID Lugar Turístico', 'Nombre Lugar Turístico', 'Puntaje']
        return rec_dataframe

    else:
        for i, value in enumerate(values[:size]):
            recommendation_list.append(indices[i])
        return recommendation_list


# Subcategorías

# Recomendar subcategorías a un usuario en base al registro de sus preferencias sobre subcategorías.
# get_similar_subcategories INPUT:
'''
# Usuario - fake data
# Definir ratings de los lugares turisticos del usuario 
user_subcategories = [
  10, 22, 3, 9, 2, 11
]

get_similar_subcategories(user_subcategories, subcategory_similarity_matrix, 20, False)
'''


def get_similar_subcategories(user_data, subcategory_similarity_matrix, size, subcategories, tabulate=False):
    similar_items = pd.DataFrame()
    for subcategory_id in user_data:
        similar_score = subcategory_similarity_matrix[subcategory_id]  # *(user_rating-2.5)
        similar_score = similar_score.sort_values(ascending=False)
        similar_items = similar_items.append(similar_score)
    similar_items_data = similar_items.sum().sort_values(ascending=False)
    indices = similar_items_data.to_frame().index.values.tolist()
    values = similar_items_data.to_frame().values

    recommendation_list = []

    if tabulate == True:
        for i, value in enumerate(values[:size]):
            recommendation_list.append([indices[i], subcategories.iloc[indices[i] - 1, 1]])
        rec_dataframe = pd.DataFrame(recommendation_list)
        rec_dataframe.columns = ['ID Subcategoría', 'Nombre Subcategoría']
        return rec_dataframe

    else:
        for i, value in enumerate(values[:size]):
            recommendation_list.append(indices[i])
        return recommendation_list


# Usuarios

# Retorna usuarios con gustos similares en base a sus SubCategorías
# get_similar_subcategories INPUT:
'''
get_similar_users(149, user_similarity_matrix, 10)
'''


def get_similar_users(user_id, user_similarity_matrix, size):
    similar_score = user_similarity_matrix[user_id]
    similar_score = similar_score.sort_values(ascending=False)
    # print(similar_score)
    similar_items = pd.DataFrame(similar_score)
    indices = similar_items.index.values.tolist()

    return indices[:size]


if __name__ == '__main__':

    # FLUJO 1
    # Cargar Datasets
    df_itemDataset = load_dataset('itemDataset.csv')
    df_subCategoryDataset = load_dataset('subCategoryDataset.csv')

    # Pre Processing
    user_ratings_matrix, subCategory_ratings_matrix, users_by_subcategory_matrix = buildMatrices(df_itemDataset,
                                                                                                 df_subCategoryDataset,
                                                                                                 df_subCategoryDataset)

    user_ratings_matrix, subCategory_ratings_matrix, users_by_subcategory_matrix = cleanNoise(user_ratings_matrix,
                                                                                                 subCategory_ratings_matrix,
                                                                                                 users_by_subcategory_matrix)

    # Training
    item_similarity_matrix, subcategory_similarity_matrix, user_similarity_matrix = computeSimilarityMatrices(user_ratings_matrix,
                                                                                                              subCategory_ratings_matrix,
                                                                                                              users_by_subcategory_matrix)

    ###
    # FLUJO 2
    # Cargar matrices de similitud
    item_similarity_matrix = pd.read_pickle('item_similarity_matrix.pkt')
    subcategory_similarity_matrix = pd.read_pickle('subcategory_similarity_matrix.pkt')
    user_similarity_matrix = pd.read_pickle('user_similarity_matrix.pkt')
    ###

    # QUERIES -> datasets para visualizar NOMBRES

    # Dataset para visualizar queries (verbose)
    # Dataset con los nombres de todos los sitios turisticos por ID
    places = load_dataset('all.csv')
    # Dataset con los nombres de todos las subcategorías por ID
    subcategories = pd.read_csv('subCategories.csv')

    # QUERIES

    # RECOMENDAR LUGARES TURISTICOS basandose en rating historico del usuario
    # API debe tener servicio -> user_places_ratings = getUserRatingHistoryById(userId)
    user_places_ratings = [
        (1, 4)
    ]
    recommended_places = get_similar_places(user_places_ratings, item_similarity_matrix, 5, places, False)
    print("Lugares turísticos recomendados al usuario 'userID':", '\n', recommended_places, '\n')





    # RECOMENDAR SUBCATEGORIAS a un usuario en base al registro de sus preferencias sobre subcategorías.
    # API debe tener servicio -> user_subcategories = getUserSubCategoriesById(userId)
    user_subcategories = [
        10, 22, 3, 9, 11
    ]
    recommended_subCategories = get_similar_subcategories(user_subcategories, subcategory_similarity_matrix, 5,
                                                          subcategories, False)
    print("Subcategorías de posible interés al usuario 'userID':", '\n', recommended_subCategories, '\n')






    '''
    # RECOMENDAR USUARIOS similares a un usuario en base a preferencias de subcategorías
    similar_users = get_similar_users(149, user_similarity_matrix, 10)
    print("Ids de usuarios similares a 'userID':", '\n', similar_users, '\n')

    # Fake Data: historial de ratings de lugares turísticos
    historicalRatings = [
        [
            (123, 5),
            (12, 4),
            (399, 5),
            (222, 1)
        ],
        [
            (23, 5),
            (245, 4),
            (23, 4),
            (100, 1),
            (900, 3)
        ],
        [
            (890, 4),
            (898, 4),
            (664, 3),
            (899, 5)
        ]
    ]


    # NUEVO QUERY: tiene como entrada la lista de usuarios similares. Se obtiene una recomendacion de lugares en base a las recomendaciones
    # brindadas a los usuarios similares
    def getSimilarUsersRecommendations(users):
        # API Service: historicalRatings = getHistoricalRatingsFromUsers(<userIDs[]>)

        recommendation_list = []
        for historicalRating in historicalRatings:
            single_prediction = get_similar_places(historicalRating, item_similarity_matrix, 3, places)
            for id in single_prediction[:2]:
                recommendation_list.append(id)

        return recommendation_list


    result = getSimilarUsersRecommendations(similar_users)
    print(result)
    '''
