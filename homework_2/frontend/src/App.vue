<template>
  <div id="app">
    <h1>Library of Books</h1>
    <div v-if="booksError" class="error">{{ booksError }}</div>
    <ul v-else>
      <li v-for="book in books" :key="book.id">
        <strong>{{ book.title }}</strong> by {{ book.author }}
        <!-- Optionally, add a button to fetch author info -->
        <button @click="fetchAuthorInfo(book.author)">Show Author Info</button>
      </li>
    </ul>

    <div v-if="authorInfo">
      <h2>Author Info</h2>
      <p>{{ authorInfo.extract }}</p>
    </div>

    <hr />

    <div>
      <h1>Current Weather (London)</h1>
      <div v-if="weatherError" class="error">{{ weatherError }}</div>
      <div v-else-if="weather">
        <p>Temperature: {{ weather.current_weather.temperature }}°C</p>
        <p>Wind Speed: {{ weather.current_weather.windspeed }} km/h</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      books: [],
      booksError: '',
      authorInfo: null,
      weather: null,
      weatherError: ''
    }
  },
  created() {
    this.fetchBooks()
    this.fetchWeather()
  },
  methods: {
    fetchBooks() {
      axios.get('http://localhost:5000/api/books')
        .then(response => {
          this.books = response.data
        })
        .catch(error => {
          this.booksError = 'Failed to load books: ' + error
        })
    },
    fetchAuthorInfo(author) {
      axios.get('http://localhost:5000/api/author-info', {
        params: { author }
      })
      .then(response => {
        this.authorInfo = response.data
      })
      .catch(error => {
        alert('Failed to load author info: ' + error)
      })
    },
    fetchWeather() {
      axios.get('http://localhost:5000/api/weather')
        .then(response => {
          this.weather = response.data
        })
        .catch(error => {
          this.weatherError = 'Failed to load weather: ' + error
        })
    }
  }
}
</script>

<style>
#error {
  color: red;
}
</style>
