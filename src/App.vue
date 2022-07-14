<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <section>
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/audio">Audio</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/video">Video</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/detection">Detection</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/reference">Reference</router-link>
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <router-view />
  </section>
</template>

