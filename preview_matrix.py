import pandas as pd

item_similarity_matrix = pd.read_pickle('item_similarity_matrix.pkt')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(item_similarity_matrix)

subcategory_similarity_matrix = pd.read_pickle('subcategory_similarity_matrix.pkt')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(subcategory_similarity_matrix)

user_similarity_matrix = pd.read_pickle('user_similarity_matrix.pkt')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(user_similarity_matrix)