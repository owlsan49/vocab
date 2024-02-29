<template>
    <el-form :model="form" label-width="120px" :label-position="labelPosition">
        <el-form-item label="unified">
            <el-input v-model="form.unidf" />
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="onDisplay">Display</el-button>
        </el-form-item>
    </el-form>

    <el-form :model="form" label-width="120px" :label-position="labelPosition">
        <div class="formatted-list">
            <h4 class="disp_listening formatted-item" v-for="(item, index) in error_words" :key="index">
                <div style="display: block;">
                    {{ item }} - {{ correct_words[index] }}
                </div>
                <div style="display: block; color: rgb(0, 145, 255);">
                    {{ meanings[index] }}
                </div>
            </h4>
        </div>
    </el-form>

    <div>
        <h2>Results</h2>
        <h3>error rate: {{ corrected_results }}</h3>
    </div>

</template>
  
<script lang="ts" setup>
import { ref } from 'vue'
import type { FormProps } from 'element-plus'
import { GetVocab } from '../apis/read'

// do not use same name with ref
const labelPosition = ref<FormProps['labelPosition']>('top')
let form = ref({ "unidf": "", "update": true })
let records = ref({})
let corrected_results = ref([])
let error_words = ref([])
let correct_words = ref([])
let meanings = ref([])

const onDisplay = () => {
    GetVocab(form.value)
        .then(response => {
            if ('msg' in response.data) {
                alert(response.data.msg)
            }
            else {
                console.log('success')
                records.value = response.data
                error_words.value = response.data.ew
                corrected_results.value = response.data.error_rate
                correct_words.value = response.data.rw
                meanings.value = response.data.mean
            }

        })
        .catch(error => {
            alert('error')
        })
}

</script>
  
<style>
.disp_listening .disp_correct {
    font-size: 32px;
    white-space: pre;
}

.disp_correct {
    color: rgb(187, 3, 3);
}

body {
    margin: 100px;
}

.formatted-list {
    display: flex;
    flex-wrap: wrap;
}

.formatted-item {
    width: 30%;
    text-align: left;
    padding-right: 30px;
}

.res_list {
    font-size: 20px;
}
</style>