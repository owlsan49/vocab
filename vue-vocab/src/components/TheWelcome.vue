<template>
  <h5>
    Last
  </h5>
  <el-table :data="tableInfo" style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="section" label="Section" width="180" />
    <el-table-column prop="error_rate" label="Error rate" width="180" />
  </el-table>
  <h5>
    Dictation Sheet
  </h5>
  <el-form :model="form" label-width="120px">
    <el-form-item label="unified idf">
      <el-input v-model="form.unidf" />
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
import { reactive, onMounted, ref, computed } from 'vue'
import { GetInfoPost, GetInitInfo } from '@/apis/read'

// do not use same name with ref
const form = reactive({
  unidf: '',
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

const tableInfo = ref([])
onMounted(() => {
  GetInitInfo()
    .then(response => {
      console.log(response)
      tableInfo.value = response.data.last_info
      console.log(tableInfo.value)
    })
    .catch(error => {
      alert('error')
    })
});

const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]

</script>

<style>
.el-textarea__inner {
  height: 400px;
}

body {
  margin: 100px;
}
</style>