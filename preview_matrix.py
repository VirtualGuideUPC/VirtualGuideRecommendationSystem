import pandas as pd

subcategory_similarity_matrix = pd.read_pickle('subcategory_similarity_matrix.pkt')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(subcategory_similarity_matrix)