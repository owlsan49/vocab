<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="unified idf">
      <el-input v-model="form.unidf" />
    </el-form-item>
    <el-form-item label="Date">
      <el-input v-model="form.date" />
    </el-form-item>
    <el-form-item label="Section">
      <el-input v-model="form.section" />
    </el-form-item>
    <el-form-item label="Listening Sheet">
      <el-input v-model="form.listening_word" type="textarea" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Submit</el-button>
      <!-- <el-button><a href="/about">Correct</a></el-button> -->
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { GetInfoPost } from '@/apis/read'

// do not use same name with ref
const form = reactive({
  unidf: '',
  date: '',
  section: '',
  delivery: false,
  type: [],
  resource: '',
  listening_word: '',
})
const submit_params = {}
const url = '/submit'
const onSubmit = () => {
  for (const key in form) {
    if (form.hasOwnProperty(key)) {
      submit_params[key] = form[key]
    }
  }
  GetInfoPost(url, submit_params)
    .then(response => {
      alert('success')
    })
    .catch(error => {
      alert('error')
    })
}
</script>

<style>
.el-textarea__inner {
  height: 400px;
}

body {
    margin: 100px;
}
</style>