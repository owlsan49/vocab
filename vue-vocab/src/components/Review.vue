<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="unified">
      <el-input v-model="form.unidf" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onDisplay">Display</el-button>
    </el-form-item>
    <!-- <p v-if="label == -1">success</p> -->
  </el-form>

  <div>
    <div class="demo-progress">
      <el-progress :text-inside="true" :stroke-width="40" :percentage="barPercentage" />
    </div>
    <audio ref="audioRef" :src="currentAudio"></audio>
    <el-button @click="togglePlay" class="el-icon-play">play</el-button>
    <p v-if="label == 1">{{ currentString }}-{{ currentMean }}</p>
    <el-input v-model="input_box" placeholder="Please input" />
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import { GetVocab } from '../apis/read'

export default {
  name: 'SimpleAudioPlayer',
  // props: {
  //   audioSource: {
  //     type: String,
  //     required: true
  //   }
  // },
  setup() {
    const audioRef = ref(null);
    const isPlaying = ref(false);
    const audioSource = ref('https://sensearch.baidu.com/gettts?lan=uk&spd=3&source=alading&text=')
    const form = reactive({ unidf: '', update: false })
    const input_box = ref('')
    const label = ref(1)
    const flag = ref(0)
    const currentIndex = ref(-1)
    const referWords = ref([])
    const meanings = ref([])

    function togglePlay() {
      audioRef.value.play();
    }

    function onDisplay() {
      GetVocab(form)
        .then(response => {
          if ('msg' in response.data) {
            alert(response.data.msg)
          }
          // console.log(response.data.rw)
          referWords.value = response.data.rw
          meanings.value = response.data.mean
          flag.value = 1

          showNextString()
        })
        .catch(error => {
          alert('error')
        })
    }

    // 计算当前显示的字符串
    const currentString = computed(() => {
      return referWords.value.length > 0 ? referWords.value[currentIndex.value] : '';
    })
    const currentMean = computed(() => {
      return meanings.value.length > 0 ? meanings.value[currentIndex.value] : '';
    })
    const currentAudio = computed(() => {
      return audioSource.value + (currentString.value == '' ? 'apple' : currentString.value);
    })
    const barPercentage = computed(() => {
      return meanings.value.length > 0 ? ((currentIndex.value/meanings.value.length)*100).toFixed(2) : 0.0;
    })

    function showNextString() {
      if ((currentIndex.value+1) == referWords.value.length) {
        alert('finished!')
      }
      label.value = (label.value + 1) % 3
      if (label.value == 2) {
        currentIndex.value = (currentIndex.value + 1) % referWords.value.length
      }

      // console.log('ccccc', currentIndex.value)
      // console.log('dddddd', referWords.value)
    }

    // 监听回车键按下事件
    function handleKeydown(event) {
      if (event.key === 'Enter') {
        console.log('press enter')
        console.log(currentString.value)
        console.log(currentMean.value)
        togglePlay()
        showNextString()
      }
    }

    // 挂载和卸载事件监听器
    watch(flag, (newValue, oldValue) => {
      if (newValue === 1) {
        // 当flag等于0时，开始监听事件
        window.addEventListener('keydown', handleKeydown);
      } else if (oldValue === 1) {
        // 当flag不再等于0时，如果之前添加过监听器，则移除它
        window.removeEventListener('keydown', handleKeydown);
      }
    });

    onBeforeUnmount(() => {
      window.removeEventListener('keydown', handleKeydown);
    });

    return {
      audioRef,
      isPlaying,
      togglePlay,
      currentAudio,
      form,
      onDisplay,
      input_box,
      label,
      currentString,
      currentMean,
      barPercentage,
    };
  }
};
</script>