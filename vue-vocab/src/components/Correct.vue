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
            <h4 class="disp_listening formatted-item" v-for="(item, index) in error_words.value" :key="index"> 
                {{ item }} - {{ correct_words.value[index] }}
            </h4> 
            <!-- <h4 class="disp_correct"> {{ correct_words.value[index].join('   ') }} </h4> -->
        </div>
    </el-form>


    <!-- <el-descriptions title="Results">
        <el-descriptions-item v-for="(value, key) in corrected_results" :label="key">{{ value }}</el-descriptions-item>
    </el-descriptions> -->

    <div>
        <h2>Results</h2>
        <h3>error rate: {{ corrected_results.value }}</h3>
    </div>


    <!-- <el-button><a href="\">Go Home</a></el-button> -->
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
const corrected_results = ref([])
const error_words = ref([])
const correct_words = ref([])
const gap_length = 6
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
                // error_words.value = computed(() => {
                //     const result = []
                //     for (let i = 0; i < response.data.ew.length; i += gap_length) {
                //         result.push(response.data.ew.slice(i, i + gap_length));
                //     }
                //     return result;
                // })
                error_words.value = computed(() => {
                    return response.data.ew;
                })
                corrected_results.value = computed(() => {
                    return response.data.error_rate;
                })

                correct_words.value = computed(() => {
                    return response.data.rw;
                })
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
}
.res_list {
    font-size: 20px;
}
</style>