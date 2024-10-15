import pandas as pd
import sqlite3
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Columns
# 'ISBN13', 'ISBN', 'Title', 'Author', 'Genre', 'Release_year',
#        'Average_rating', 'Numpages', 'Totalrating', 'Coverimg', 'Description'

conn = sqlite3.connect('instance\\books.db')

books_df = pd.read_sql_query('SELECT * FROM Books', conn)
books_df.drop_duplicates(subset=['ISBN13','Title'],inplace=True,keep='first')

user_df = pd.read_sql_query('SELECT * FROM User',conn)

recommend_year = books_df.sort_values(by='Release_year',ascending=False)
recommend_rating = books_df.sort_values(by='Average_rating',ascending=False)
recommend_rating = recommend_rating[recommend_rating['Totalrating'] >= 1750]

genre = ['Fiction','Non-Fiction','Mystery','Horror','Fantasy']
Fiction = books_df[(books_df['Genre'].isin(['Fiction'])) & (books_df['Average_rating'] == books_df['Average_rating'])].iloc[2:3]
non_fiction = books_df[(books_df['Genre'].isin(['Romance'])) & (books_df['Average_rating'] == books_df['Average_rating'])].head(1)
mystery = books_df[(books_df['Genre'].isin(['Mystery'])) & (books_df['Average_rating'] == books_df['Average_rating'])].head(1)
horror = books_df[(books_df['Genre'].isin(['Philosophy'])) & (books_df['Average_rating'] == books_df['Average_rating'])].head(1)
fantasy = books_df[(books_df['Genre'].isin(['Fantasy'])) & (books_df['Average_rating'] == books_df['Average_rating'])].head(1)

recommend_top = pd.concat([Fiction,non_fiction,mystery,horror,fantasy])

def recommedbooks(value):
    if value in books_df['Author'].values:
        book = books_df[books_df['Author'] == value]
        book = book.sort_values(by='Average_rating',ascending = False)
        return book
    elif value in books_df['Genre'].values:
        book = books_df[books_df['Genre'] == value]
        book.sort_values(by="Average_rating",ascending = False)
        return book
    else:
        closest_values = difflib.get_close_matches(value, books_df['Title'])
        matched_rows = books_df.loc[books_df['Title'].isin(closest_values)]
        return matched_rows

def search(search):
    pass

def recommend(user_id,num_result):
    user_row = user_df[user_df['id'] == user_id]
    if user_row.empty:
        return None
    user_genres = set(user_row.iloc[0]['genre'].split(', '))

    filtered_books = books_df[books_df['Genre'].apply(lambda x:any(item.lower() in x.lower() for item in user_genres))]

    if filtered_books.empty:
        return recommend_rating
    
    vectorizer = TfidfVectorizer(stop_words='english')
    title_vectors = vectorizer.fit_transform(filtered_books['Title'])
    similarity_scores = cosine_similarity(title_vectors, title_vectors)

    similar_books = []
    for i in range(len(filtered_books)):
        sorted_indices = similarity_scores[i].argsort()[::-1]
        similar_indices = [index for index in sorted_indices if index != i][:num_result]
        similar_books.append(similar_indices)

    results = []
    for i in range(len(filtered_books)):
        filtered_book = filtered_books.iloc[i]
        for index in similar_books[i]:
            similar_book = books_df.iloc[index]
            results.append({'Title': similar_book['Title'],
                            'Author': similar_book['Author'],
                            'Genre': similar_book['Genre'],
                            'Release_year': similar_book['Release_year'],
                            'Average_rating': similar_book['Average_rating'],
                            'Numpages': similar_book['Numpages'],
                            'Totalrating': similar_book['Totalrating'],
                            'Coverimg': similar_book['Coverimg'],
                            'Similarity_score': similarity_scores[i][index]})
    
    results.sort(key=lambda x: x['Similarity_score'], reverse=True)
    result = pd.DataFrame(results)
    return result

conn.close()

if __name__ == "__main__":
  print(books_df.isnull().sum())
