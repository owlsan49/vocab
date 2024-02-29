<template>
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="Listening" name="first">
            <TheWelcome />
        </el-tab-pane>
        <el-tab-pane label="Correct" name="second">
            <Correct />
        </el-tab-pane>
        <el-tab-pane label="Review" name="third">
            <Review />
        </el-tab-pane>
        <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
    </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import Correct from '../components/Correct.vue'
import TheWelcome from '../components/TheWelcome.vue'
import Review from '../components/Review.vue'

const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
    console.log(tab, event)
}
</script>
<style>
.demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}</style>