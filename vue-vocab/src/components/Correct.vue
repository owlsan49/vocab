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
        <div v-for="(item, index) in processedArray.value" :key="index" class="row">
            <h2> {{ item }} </h2>
            <el-form-item>
                <el-input v-model="correct_words[index]" />
            </el-form-item>
        </div>

        <el-form-item>
            <el-button type="primary" @click="onSubmit">Submit</el-button>
        </el-form-item>
    </el-form>
</template>
  
<script lang="ts" setup>
import { reactive, ref, computed } from 'vue'
import type { FormProps } from 'element-plus'
import { GetVocab, GetInfoPost } from '../apis/read'

// do not use same name with ref
const labelPosition = ref<FormProps['labelPosition']>('top')
const form = reactive({
    unidf: '',
})
const submit_params = {}
const records = reactive({})
const processedArray = ref([])
const correct_words = ref([])
const onDisplay = () => {
    for (const key in form) {
        if (form.hasOwnProperty(key)) {
            submit_params[key] = form[key]
        }
    }
    GetVocab(submit_params)
        .then(response => {
            if ('msg' in response.data) {
                alert(response.data.msg)
            }
            else {
                console.log('success')
                console.log(response.data.listening_word)
                Object.assign(records, response.data)
                processedArray.value = computed(() => {
                    const result = []
                    for (let i = 0; i < response.data.listening_word.length; i += 4) {
                        result.push(response.data.listening_word.slice(i, i + 4));
                    }
                    return result;
                })
                console.log(processedArray.value)
                // console.log(processedArray)
            }

        })
        .catch(error => {
            alert('error')
        })
}

const sub_url = '/correct'
const correct_param = {}
const onSubmit = () => {
    console.log(correct_words.value.join(' '))
    correct_param['correct_str'] = correct_words.value.join(' ')
    correct_param['unidf'] = form['unidf']
    GetInfoPost(sub_url, correct_param)
        .then(response => {
            alert('success')
        })
        .catch(error => {
            alert('error')
        })
}

</script>
  
<style></style>