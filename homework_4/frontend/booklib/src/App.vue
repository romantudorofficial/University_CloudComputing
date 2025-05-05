<template>
  <div class="container">
    <h1>📚 Book Library</h1>
    <p>Welcome to the Book Library Project!</p>
    <button @click="pingBackend">Test Backend</button>
    <p v-if="response">Response: {{ response }}</p>

    <h2 class="books-header">Books in Library</h2>
    <ul>
      <li v-for="book in books" :key="book.id" class="book-item">
        <strong>{{ book.title }}</strong> by {{ book.author }}
        <p>{{ book.description }}</p>
      </li>
    </ul>

    <div>
      <h3>Add a New Book</h3>
      <form @submit.prevent="addBook">
        <input v-model="newBook.title" placeholder="Book Title" required />
        <input v-model="newBook.author" placeholder="Author" required />
        <textarea v-model="newBook.description" placeholder="Description" required></textarea>
        <button type="submit">Add Book</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const response = ref('')
const books = ref([])
const newBook = ref({
  title: '',
  author: '',
  description: ''
})

async function pingBackend() {
  try {
    const res = await fetch('http://localhost:5000/ping')
    const data = await res.text()
    response.value = data
  } catch (err) {
    response.value = 'Error connecting to backend'
  }
}

async function fetchBooks() {
  try {
    const res = await fetch('http://localhost:5000/books')
    const data = await res.json()
    books.value = data
  } catch (err) {
    console.error('Error fetching books:', err)
  }
}

async function addBook() {
  try {
    const res = await fetch('http://localhost:5000/books', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newBook.value)
    })
    if (res.ok) {
      fetchBooks()  // Refresh the list after adding a book
      newBook.value = { title: '', author: '', description: '' }  // Reset form
    }
  } catch (err) {
    console.error('Error adding book:', err)
  }
}

onMounted(() => {
  fetchBooks()  // Fetch books when the component is mounted
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
  text-align: center;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f4f4f4;
  margin: 0.5rem 0;
  padding: 1rem;
  border-radius: 8px;
}

input, textarea {
  margin: 0.5rem;
  padding: 0.5rem;
  width: 80%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Style for the Books in Library header */
.books-header {
  color: white;  /* White color for the Books in Library header */
  font-size: 1.5rem;
  margin-top: 2rem;
}

/* Style for the book item text */
.book-item {
  color: black;  /* Black color for book title, author, and description */
}

.book-item strong {
  font-size: 1.2rem;
  color: black; /* Ensure title is black */
}

.book-item p {
  color: black; /* Ensure description text is black */
}
</style>
