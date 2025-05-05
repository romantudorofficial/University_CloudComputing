<template>
  <div class="container">
    <h1>📚 Book Library Project</h1>
    <p>Welcome to the Cloud Computing Homework 4 frontend!</p>
    <button @click="pingBackend">Test Backend</button>
    <p v-if="response">Response: {{ response }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const response = ref('')

async function pingBackend() {
  try {
    const res = await fetch('/api/ping')  // Ensure '/api' is added for the proxy route
    const data = await res.text()
    response.value = data
  } catch (err) {
    response.value = 'Error connecting to backend'
  }
}

</script>

<style>
.container {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
  text-align: center;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
</style>
