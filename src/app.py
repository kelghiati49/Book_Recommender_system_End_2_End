import pickle
import streamlit as st
import numpy as np
import base64

def add_bg(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jfif;base64,{encoded}");
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("src/background.jfif")


st.header("Book Recommender System Using Machine Learning")
model = pickle.load(open('artifacts\model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
final_ratings = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))


selected_books = st.selectbox(
    "Type or select a book",
    books_name
)

# define the fnc that fetches the url of suggested books 
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_ratings['title']==name)[0][0]
        ids_index.append(ids) #we have suggested books ids in dataset

    for idx in ids_index:
        url = final_ratings.iloc[idx]['Image-URL-L']
        poster_url.append(url)
    return poster_url
 

# define the recommendation function
def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0] #get the index of the book in the pivot table
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=7)
    
    poster_url = fetch_poster(suggestion) # fnc to fetch book suggested url from the dataset
    
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
           book_list.append(j)
    return book_list, poster_url


if st.button('Show Recommendation'):
   recommended_books, poster_url = recommend_books(selected_books)
   col1, col2, col3, col4, col5= st.columns(5)

   with col1:
    st.text(recommended_books[1])  # index 0 : is the book selected by user
    st.image(poster_url[1])

   with col2:
    st.text(recommended_books[2])  
    st.image(poster_url[2])

   with col3:
    st.text(recommended_books[3]) 
    st.image(poster_url[3])

   with col4:
    st.text(recommended_books[4])  
    st.image(poster_url[4])

   with col5:
    st.text(recommended_books[5]) 
    st.image(poster_url[5])