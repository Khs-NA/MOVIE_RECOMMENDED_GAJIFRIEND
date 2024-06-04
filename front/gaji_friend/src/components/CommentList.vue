<template>
  <li>
    <span> {{ comment.create_user }} : </span>
    <span class="comment-content">{{ comment.content }}</span>
  </li>
</template>

<script setup>
defineProps({
  comment: Object
})
</script>

<style lang="scss" scoped>

</style>
