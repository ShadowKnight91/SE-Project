import streamlit as st
import pandas as pd
import mysql.connector

# Connect to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pointbreak1!",
        database="movieawardceremony"
    )
    return connection

# Create a cursor object to execute SQL queries
def add_new_movie():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Add New Movie")
    movie_title = st.text_input("Enter Movie Title:")
    release_year = st.number_input("Enter Release Year:", min_value=1800, max_value=9999, step=1, format="%d", key="release_year")
    genre = st.text_input("Enter Genre:")
    director = st.text_input("Enter Director:")
    producerID = st.text_input("Enter Producer ID:")

    if st.button("Add Movie"):
        if movie_title and release_year and genre and director and producerID:
            # Build the SQL query based on provided fields
            sql_query = "INSERT INTO movies (title, release_year, genre, director, producerid) VALUES (%s, %s, %s, %s, %s)"
            values = (movie_title, release_year, genre, director, int(producerID))

            # Execute the SQL query with the values
            cursor.execute(sql_query, values)
            connection.commit()
            st.success("Movie added successfully!")

        else:
            st.error("Movie Title, Release Year, Genre, Director, and Producer ID are required fields!")

    cursor.close()
    connection.close()



def add_new_actor():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Add New Actor")
    actor_name = st.text_input("Enter Actor Name:")
    birth_date = st.date_input("Enter Birth Date:")
    gender = st.selectbox("Select Gender:", ["Male", "Female", "Other"])
    contact_information = st.text_input("Enter Contact Information:")
    biography = st.text_area("Enter Biography:")

    if st.button("Add Actor"):
        if actor_name and birth_date:
            # Build the SQL query based on provided fields
            sql_query = "INSERT INTO actors (ActorName, DateOfBirth, Gender, ContactInformation, Biography) VALUES (%s, %s, %s, %s, %s)"
            values = (actor_name, birth_date, gender, contact_information, biography)

            # Execute the SQL query with the values
            cursor.execute(sql_query, values)
            connection.commit()
            st.success("Actor added successfully!")

        else:
            st.error("Actor Name and Birth Date are required fields!")

    cursor.close()
    connection.close()


def add_new_director():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Add New Director")
    director_name = st.text_input("Enter Director Name:")
    birth_date = st.date_input("Enter Date of Birth:")
    gender = st.selectbox("Select Gender:", ["Male", "Female", "Other"])
    contact_info = st.text_input("Enter Contact Information:")
    
    if st.button("Add Director"):
        if director_name and birth_date and gender and contact_info is not None:
            # Build the SQL query based on provided fields
            sql_query = "INSERT INTO Directors (DirectorName, DateOfBirth, Gender, ContactInformation) VALUES (%s, %s, %s, %s)"
            values = (director_name, birth_date, gender, contact_info)

            # Execute the SQL query with the values
            cursor.execute(sql_query, values)
            connection.commit()
            st.success("Director added successfully!")

        else:
            st.error("All fields are required!")

    cursor.close()
    connection.close()


def add_new_song():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Add New Song")
    song_title = st.text_input("Enter Song Title:")
    singer = st.text_input("Enter Singer:")
    music_director = st.text_input("Enter Music Director:")
    lyrics_by = st.text_input("Enter Lyrics By:")
    
    if st.button("Add Song"):
        if song_title and singer and music_director and lyrics_by  is not None:
            # Build the SQL query based on provided fields
            sql_query = "INSERT INTO Songs (SongTitle, Singer, MusicDirector, LyricsBy) VALUES (%s, %s, %s, %s)"
            values = (song_title, singer, music_director, lyrics_by)

            # Execute the SQL query with the values
            cursor.execute(sql_query, values)
            connection.commit()
            st.success("Song added successfully!")

        else:
            st.error("All fields are required!")

    cursor.close()
    connection.close()


def vote_for_category():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Vote for Category")

    category = st.selectbox("Select Category:", ["Movie", "Actor", "Director", "Producer", "Song"], key="category_selectbox")

    if category == "Movie":
        cursor.execute("SELECT Title FROM Movies")
        movie_titles = [result[0] for result in cursor.fetchall()]

        selected_movie = st.selectbox("Select Movie:", movie_titles, key="movie_selectbox")

        if selected_movie:
            user_id = st.text_input("Enter User ID:")
            user_id = user_id.strip()

            if user_id:
                cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
                result = cursor.fetchone()
                st.write(f"User ID: {user_id}")
                if not result:
                    st.error(f"User with ID {user_id} does not exist.")
                    return

                cursor.execute("SELECT * FROM user_votes WHERE user_id=%s AND category='Movie'", (user_id,))
                existing_vote = cursor.fetchone()

                if existing_vote:
                    st.warning(f"User has already voted for this category")
                else:
                    vote_count = 1  # Since a user can vote exactly once in a category
                    cursor.execute("INSERT INTO votes (user_id, category, item_name, vote_count) VALUES (%s, %s, %s, %s)",
                                   (user_id, category, selected_movie, vote_count))

                    # Increment the vote count in the Movies table
                    cursor.execute("UPDATE Movies SET Votes = Votes + 1 WHERE Title = %s", (selected_movie,))
                    cursor.execute("INSERT INTO user_votes (user_id, category) VALUES (%s, %s)",
                                   (user_id, category))
                    connection.commit()

                    st.success(f"Vote recorded successfully for Movie: {selected_movie}")

    elif category == "Actor":
        cursor.execute("SELECT ActorName FROM Actors")
        actor_names = [result[0] for result in cursor.fetchall()]

        selected_actor = st.selectbox("Select Actor:", actor_names, key="actor_selectbox")

        if selected_actor:
            user_id = st.text_input("Enter User ID:")
            user_id = user_id.strip()

            if user_id:
                cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
                result = cursor.fetchone()
                st.write(f"User ID: {user_id}")
                if not result:
                    st.error(f"User with ID {user_id} does not exist.")
                    cursor.close()
                    connection.close()
                    return

                cursor.execute("SELECT * FROM user_votes WHERE user_id=%s AND category='Actor'", (user_id,))
                existing_vote = cursor.fetchone()

                if existing_vote:
                    st.warning(f"User has already voted for this category")
                else:
                    vote_count = 1
                    cursor.execute("INSERT INTO votes (user_id, category, item_name, vote_count) VALUES (%s, %s, %s, %s)",
                                   (user_id, category, selected_actor, vote_count))
                    cursor.execute("UPDATE Actors SET ActorVotes = ActorVotes + 1 WHERE ActorName = %s", (selected_actor,))
                    connection.commit()
                    cursor.execute("INSERT INTO user_votes (user_id, category) VALUES (%s, %s)", (user_id, category))
                    connection.commit()
                    st.success(f"Vote recorded successfully for Actor: {selected_actor}")

    elif category == "Director":
        cursor.execute("SELECT DirectorName FROM Directors")
        director_names = [result[0] for result in cursor.fetchall()]

        selected_director = st.selectbox("Select Director:", director_names, key="director_selectbox")

        if selected_director:
            user_id = st.text_input("Enter User ID:")
            user_id = user_id.strip()

            if user_id:
                cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
                result = cursor.fetchone()
                st.write(f"User ID: {user_id}")
                if not result:
                    st.error(f"User with ID {user_id} does not exist.")
                    cursor.close()
                    connection.close()
                    return

                cursor.execute("SELECT * FROM user_votes WHERE user_id=%s AND category='Director'", (user_id,))
                existing_vote = cursor.fetchone()

                if existing_vote:
                    st.warning(f"User has already voted for this category")
                else:
                    vote_count = 1
                    cursor.execute("INSERT INTO votes (user_id, category, item_name, vote_count) VALUES (%s, %s, %s, %s)",
                                   (user_id, category, selected_director, vote_count))
                    cursor.execute("UPDATE Directors SET DirectorVotes = DirectorVotes + 1 WHERE DirectorName = %s", (selected_director,))
                    connection.commit()
                    cursor.execute("INSERT INTO user_votes (user_id, category) VALUES (%s, %s)", (user_id, category))
                    connection.commit()
                    st.success(f"Vote recorded successfully for Director: {selected_director}")

    elif category == "Producer":
        cursor.execute("SELECT ProducerName FROM Producers")
        producer_names = [result[0] for result in cursor.fetchall()]

        selected_producer = st.selectbox("Select Producer:", producer_names, key="producer_selectbox")

        if selected_producer:
            user_id = st.text_input("Enter User ID:")
            user_id = user_id.strip()

            if user_id:
                cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
                result = cursor.fetchone()
                st.write(f"User ID: {user_id}")
                if not result:
                    st.error(f"User with ID {user_id} does not exist.")
                    cursor.close()
                    connection.close()
                    return

                cursor.execute("SELECT * FROM user_votes WHERE user_id=%s AND category='Producer'", (user_id,))
                existing_vote = cursor.fetchone()

                if existing_vote:
                    st.warning(f"User has already voted for this category.")
                else:
                    vote_count = 1
                    cursor.execute("INSERT INTO votes (user_id, category, item_name, vote_count) VALUES (%s, %s, %s, %s)",
                                   (user_id, category, selected_producer, vote_count))
                    cursor.execute("UPDATE Producers SET Pvotes = Pvotes + 1 WHERE ProducerName = %s", (selected_producer,))
                    connection.commit()
                    cursor.execute("INSERT INTO user_votes (user_id, category) VALUES (%s, %s)", (user_id, category))
                    connection.commit()
                    st.success(f"Vote recorded successfully for Producer: {selected_producer}")

    elif category == "Song":
        cursor.execute("SELECT SongTitle FROM Songs")
        song_titles = [result[0] for result in cursor.fetchall()]

        selected_song = st.selectbox("Select Song:", song_titles, key="song_selectbox")

        if selected_song:
            user_id = st.text_input("Enter User ID:")
            user_id = user_id.strip()

            if user_id:
                cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
                result = cursor.fetchone()
                st.write(f"User ID: {user_id}")
                if not result:
                    st.error(f"User with ID {user_id} does not exist.")
                    cursor.close()
                    connection.close()
                    return

                cursor.execute("SELECT * FROM user_votes WHERE user_id=%s AND category='Song'", (user_id,))
                existing_vote = cursor.fetchone()

                if existing_vote:
                    st.warning(f"User has already voted for this category")
                else:
                    vote_count = 1
                    cursor.execute("INSERT INTO votes (user_id, category, item_name, vote_count) VALUES (%s, %s, %s, %s)",
                                   (user_id, category, selected_song, vote_count))
                    cursor.execute("UPDATE Songs SET Votes = Votes + 1 WHERE SongTitle = %s", (selected_song,))
                    connection.commit()
                    cursor.execute("INSERT INTO user_votes (user_id, category) VALUES (%s, %s)", (user_id, category))
                    connection.commit()
                    st.success(f"Vote recorded successfully for Song: {selected_song}")

    st.write("All Votes")
    cursor.execute("SELECT * FROM votes")
    votes_data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]

    # Create a DataFrame with column names and votes data
    df = pd.DataFrame(votes_data, columns=column_names)

    # Display the DataFrame without index and header
    st.table(df.to_records(index=False))

    cursor.close()
    connection.close()
    

def generate_voting_report():
    connection = get_db_connection()
    cursor = connection.cursor()

    st.write("Generating Voting Report")

    categories = ["Movie", "Actor", "Director", "Producer", "Song"]

    for category in categories:
        st.write(f"Report for {category}")
        
        # Get a list of unique item names in this category
        cursor.execute("SELECT DISTINCT item_name FROM votes WHERE category=%s", (category,))
        items = [item[0] for item in cursor.fetchall()]

        max_votes = 0
        winning_items = []

        for item in items:
            # Get the total vote count for this item in this category
            cursor.execute("""
                SELECT item_name, SUM(vote_count) AS total_votes
                FROM votes
                WHERE category=%s AND item_name=%s
                GROUP BY item_name
            """, (category, item))
            result = cursor.fetchone()

            if result:
                _, total_votes = result
                st.write(f"{item}: Total Votes = {total_votes}")

                if total_votes > max_votes:
                    max_votes = total_votes
                    winning_items = [item]
                elif total_votes == max_votes:
                    winning_items.append(item)

        # Get the total number of participants for this category
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM votes WHERE category=%s", (category,))
        total_participants = cursor.fetchone()[0]

        st.write(f"Total Participants: {total_participants}")

        if winning_items:
            st.write(f"Winning Item(s): {', '.join(winning_items)}")

    cursor.close()
    connection.close()


def non_admin_page():
    choice = "home"
    menu = [
        "Home",
        "Vote for Category"
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Vote for Category":
        vote_for_category()
        
def first_page():
    choice = "home"
    menu = [
        "Home",
        "Add Movie",
        "Add Actor",
        "Add Director",
        "Add Song",
        "Generate Voting Report"
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Movie Award Ceremony Management")
        st.write("Manage movies, actors, directors, producers, songs, users, and more!")

    elif choice == "Add Movie":
        add_new_movie()

    elif choice == "Add Actor":
        add_new_actor()

    elif choice == "Add Director":
        add_new_director()

    elif choice == "Add Song":
        add_new_song()

    elif choice == "Generate Voting Report":
        generate_voting_report()


def main():
    custom_css = """
        <style>
            .stApp {
                background-color: #BC8F8F;  # You can change the color as needed
            }
        </style>
    """

    # Inject custom CSS with the `st.markdown()` function
    st.markdown(custom_css, unsafe_allow_html=True)
    username = ""
    password = ""
    login_placeholder = st.empty()

    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.is_admin = False

    if not st.session_state.login:
        st.title("User Login")
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key='password_input')

        if st.button("Login"):
            if username == 'admin' and password == '123':
                st.session_state.login = True
                st.session_state.is_admin = True
                login_placeholder.empty()
            elif username == 'user' and password == '123':
                st.session_state.login = True
                login_placeholder.empty()
            else:
                st.error("Invalid username or password. Please try again.")

    if st.session_state.login:
        if st.session_state.is_admin:
            first_page()
        else:
            non_admin_page()


if __name__ == "__main__":
    main()