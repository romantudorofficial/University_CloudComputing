<template>

  <div id = "app">

    <header class = "header">

      <h1>Library of Books</h1>
    
    </header>

    <section class = "books-section">

      <h2>Books Collection</h2>

      <div v-if = "booksError" class = "error">{{ booksError }}</div>

      <ul class = "book-list" v-else>

        <li class = "book-item" v-for = "book in books" :key = "book.id">

          <div class = "book-info">

            <strong>{{ book.title }}</strong>
            <span class = "by">by</span>
            <span class = "author">{{ book.author }}</span>

          </div>

          <button class = "info-btn" @click = "fetchAuthorInfo(book.author)">Show Author Info</button>

        </li>

      </ul>

    </section>

    <section class = "author-section" v-if = "authorInfo">

      <h2>Author Info</h2>
      <p>{{ authorInfo.extract }}</p>

    </section>

    <hr />

    <section class = "weather-section">

      <h2>Current Weather (Iași, Romania)</h2>

      <div v-if = "weatherError" class="error">{{ weatherError }}</div>

      <div v-else-if = "weather" class="weather-info">

        <p><span class = "label">Temperature:</span> {{ weather.current_weather.temperature }}°C</p>
        <p><span class = "label">Wind Speed:</span> {{ weather.current_weather.windspeed }} km/h</p>

      </div>

    </section>

  </div>

</template>



<script>

import axios from 'axios'

export default {

  name: 'App',

  data ()
  {
    return {
      books: [],
      booksError: '',
      authorInfo: null,
      weather: null,
      weatherError: ''
    }
  },

  created ()
  {
    this.fetchBooks()
    this.fetchWeather()
  },

  methods:
  {
    fetchBooks ()
    {
      axios.get('http://localhost:5000/api/books')
        .then(response => {
          this.books = response.data
        })
        .catch(error => {
          this.booksError = 'Failed to load books: ' + error
        })
    },

    fetchAuthorInfo (author)
    {
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

    fetchWeather () 
    {
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



<style scoped>

/* Overall container styling */

#app
{
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


/* Header styling */

.header
{
  text-align: center;
  padding: 15px 0;
  background: #2c3e50;
  color: #fff;
  border-radius: 8px;
}


.header h1
{
  margin: 0;
  font-size: 2.5rem;
}


/* Section headings */

.books-section, .author-section, .weather-section
{
  margin-top: 30px;
}


h2
{
  color: #34495e;
  border-bottom: 2px solid #3498db;
  padding-bottom: 5px;
}


/* Books list styling */

.book-list
{
  list-style: none;
  padding: 0;
}


.book-item
{
  background: #fff;
  margin: 10px 0;
  padding: 15px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s;
}


.book-item:hover
{
  transform: translateY(-3px);
}


.book-info
{
  display: flex;
  align-items: center;
  gap: 5px;
}


.book-info .by
{
  color: #7f8c8d;
}


.info-btn
{
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.3s ease;
}


.info-btn:hover
{
  background: #2980b9;
}


/* Error message styling */

.error
{
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
}


/* Weather section styling */

.weather-info p
{
  margin: 8px 0;
  font-size: 1.1rem;
}


.label
{
  font-weight: bold;
  color: #2c3e50;
}


/* Horizontal rule styling */

hr
{
  border: none;
  height: 1px;
  background: #ddd;
  margin: 30px 0;
}

</style>