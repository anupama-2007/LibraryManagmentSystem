
import streamlit as st

# -------------------------------
# Book Class
# -------------------------------
class Book:

    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_issued = False

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"[{self.book_id}] '{self.title}' by {self.author} - Status: {status}"


# -------------------------------
# Library Class
# -------------------------------
class Library:

    def __init__(self):
        self.books = {}

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            return False, "Book ID already exists!"

        self.books[book_id] = Book(book_id, title, author)
        return True, "Book added successfully!"

    def view_books(self):
        return self.books.values()

    def issue_book(self, book_id):
        if book_id not in self.books:
            return False, "Book ID not found!"

        if self.books[book_id].is_issued:
            return False, "This book is already issued!"

        self.books[book_id].is_issued = True
        return True, "Book issued successfully!"

    def return_book(self, book_id):
        if book_id not in self.books:
            return False, "Book ID not found!"

        if not self.books[book_id].is_issued:
            return False, "This book was not marked as issued!"

        self.books[book_id].is_issued = False
        return True, "Book returned successfully!"


# -------------------------------
# Streamlit Configuration
# -------------------------------
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# -------------------------------
# Initialize Library
# -------------------------------
if "library" not in st.session_state:

    library = Library()

    initial_books = [
        ("101", "The Alchemist", "Paulo Coelho"),
        ("102", "Atomic Habits", "James Clear"),
        ("103", "To Kill a Mockingbird", "Harper Lee"),
        ("104", "1984", "George Orwell"),
        ("105", "The Great Gatsby", "F. Scott Fitzgerald"),
        ("106", "Pride and Prejudice", "Jane Austen"),
        ("107", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling"),
        ("108", "The Hobbit", "J.R.R. Tolkien"),
    ]

    for book_id, title, author in initial_books:
        library.add_book(book_id, title, author)

    st.session_state.library = library


library = st.session_state.library


# -------------------------------
# Application Header
# -------------------------------
st.title("📚 Library Management System")
st.write("Manage books, issue books, and track returned books.")

st.divider()


# -------------------------------
# Dashboard
# -------------------------------
total_books = len(library.books)
issued_books = sum(
    1 for book in library.books.values() if book.is_issued
)
available_books = total_books - issued_books

col1, col2, col3 = st.columns(3)

col1.metric("📚 Total Books", total_books)
col2.metric("✅ Available Books", available_books)
col3.metric("📕 Issued Books", issued_books)

st.divider()


# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select an Option",
    [
        "Home",
        "Add Book",
        "View Books",
        "Issue Book",
        "Return Book"
    ]
)


# -------------------------------
# Home
# -------------------------------
if menu == "Home":

    st.subheader("Welcome to the Library!")

    st.write("""
    This Library Management System allows you to:

    - Add new books to the library.
    - View all available and issued books.
    - Issue books to readers.
    - Return previously issued books.
    """)

    st.info("Select an option from the sidebar to get started.")


# -------------------------------
# Add Book
# -------------------------------
elif menu == "Add Book":

    st.subheader("➕ Add a New Book")

    with st.form("add_book_form"):

        book_id = st.text_input("Enter Book ID")
        title = st.text_input("Enter Book Title")
        author = st.text_input("Enter Author Name")

        submit = st.form_submit_button("Add Book")

        if submit:

            book_id = book_id.strip()
            title = title.strip()
            author = author.strip()

            if not book_id or not title or not author:
                st.error("Please fill in all the fields.")

            else:
                success, message = library.add_book(
                    book_id, title, author
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)


# -------------------------------
# View Books
# -------------------------------
elif menu == "View Books":

    st.subheader("📖 Library Catalog")

    if not library.books:
        st.warning("No books available in the library.")

    else:

        search = st.text_input("🔍 Search by Book ID, Title or Author")

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Available", "Issued"]
        )

        book_data = []

        for book in library.view_books():

            status = "Issued" if book.is_issued else "Available"

            if status_filter != "All" and status != status_filter:
                continue

            if search and search.lower() not in (
                book.book_id + " " + book.title + " " + book.author
            ).lower():
                continue

            book_data.append({
                "Book ID": book.book_id,
                "Title": book.title,
                "Author": book.author,
                "Status": status
            })

        if book_data:
            st.dataframe(
                book_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No matching books found.")


# -------------------------------
# Issue Book
# -------------------------------
elif menu == "Issue Book":

    st.subheader("📕 Issue a Book")

    available = [
        book for book in library.books.values()
        if not book.is_issued
    ]

    if not available:
        st.warning("No books are currently available.")

    else:

        book_options = {
            f"{book.book_id} - {book.title}": book.book_id
            for book in available
        }

        selected_book = st.selectbox(
            "Select a book to issue",
            list(book_options.keys())
        )

        if st.button("Issue Book", type="primary"):

            book_id = book_options[selected_book]

            success, message = library.issue_book(book_id)

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


# -------------------------------
# Return Book
# -------------------------------
elif menu == "Return Book":

    st.subheader("📗 Return a Book")

    issued = [
        book for book in library.books.values()
        if book.is_issued
    ]

    if not issued:
        st.warning("There are no issued books to return.")

    else:

        book_options = {
            f"{book.book_id} - {book.title}": book.book_id
            for book in issued
        }

        selected_book = st.selectbox(
            "Select a book to return",
            list(book_options.keys())
        )

        if st.button("Return Book", type="primary"):

            book_id = book_options[selected_book]

            success, message = library.return_book(book_id)

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


# -------------------------------
# Footer
# -------------------------------
st.divider()
st.caption("Library Management System | Developed using Python and Streamlit")
