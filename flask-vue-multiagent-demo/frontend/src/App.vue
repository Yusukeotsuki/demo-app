<template>
  <div class="max-w-3xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
    <!-- タイトル -->
    <h1 class="text-3xl font-bold mb-6 text-center">Multi-Agent Chat</h1>

    <!-- チャット履歴 -->
    <div class="space-y-4 h-[600px] overflow-y-auto mb-6">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="flex"
        :class="msg.from === 'user' ? 'justify-end' : 'justify-start'"
      >
        <!-- エージェント発言 -->
        <template v-if="msg.from !== 'user'">
          <div class="max-w-[70%]">
            <!-- ヘッダー -->
            <div class="flex items-center bg-blue-500 text-white px-3 py-1 rounded-t-lg">
              <img
                :src="`/${msg.from}.svg`"
                alt="Agent Icon"
                class="h-5 w-5 rounded-full mr-2"
              />
              <span class="font-semibold">{{ msg.from }}</span>
            </div>
            <!-- 本文 -->
            <div
              class="bg-blue-100 text-black px-4 py-3 rounded-b-lg whitespace-pre-wrap prose prose-sm"
            >
              <div v-html="renderMarkdown(msg.text)"></div>
            </div>
          </div>
        </template>

        <!-- ユーザー発言 -->
        <template v-else>
          <div class="max-w-[70%] flex justify-end">
            <div class="bg-green-100 text-green-900 px-4 py-3 rounded-lg whitespace-pre-wrap">
              <p>{{ msg.text }}</p>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 入力欄 & 添付ボタン -->
    <div class="flex items-center space-x-2">
      <div class="relative flex-1">
        <input
          v-model="input"
          @keyup.enter="sendMessage"
          class="w-full border rounded-lg px-4 py-2 pr-12 focus:outline-none"
          placeholder="Type a message or attach Excel..."
        />
        <img
          v-if="showExcelIcon"
          src="/excel_icon.svg"
          alt="Excel Icon"
          class="absolute right-4 top-1/2 transform -translate-y-1/2 h-6 w-6"
        />
      </div>
      <button
        @click="$refs.fileInput.click()"
        class="bg-yellow-500 text-white px-4 py-2 rounded-lg"
      >
        Attach
      </button>
      <input
        type="file"
        ref="fileInput"
        accept=".xlsx,.xls"
        class="hidden"
        @change="onFileChange"
      />
      <button
        @click="sendMessage"
        class="bg-blue-600 text-white px-6 py-2 rounded-lg"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
  data() {
    return {
      input: '',
      messages: [],
      showExcelIcon: false,
      selectedFile: null,
      evtSource: null,
    }
  },
  methods: {
    // Markdown → HTML
    renderMarkdown(text) {
      return marked.parse(text)
    },

    // Excelファイル選択
    onFileChange(event) {
      const file = event.target.files[0]
      if (file && /\.(xlsx|xls)$/i.test(file.name)) {
        this.showExcelIcon = true
        this.selectedFile = file
        this.input = file.name
      } else {
        this.showExcelIcon = false
        this.selectedFile = null
      }
    },

     sendMessage() {
      const text = this.input.trim()
      if (!text && !this.selectedFile) return

      // ユーザー発言を即プッシュ
      this.messages.push({
        id: Date.now(),
        from: 'user',
        text: text || this.selectedFile.name
      })
      this.input = ''
      this.showExcelIcon = false

     // 既存のストリームがあれば閉じる
     if (this.evtSource) {
       this.evtSource.close()
       this.evtSource = null
     }

     // 必ずクエリ文字列を付与して GET で接続
     const url = `http://localhost:5000/api/chat_stream?message=${encodeURIComponent(text)}`
     this.evtSource = new EventSource(url)

      let buffer = ''
      const msgId = Date.now() + Math.random()

      this.evtSource.onmessage = (e) => {
        const { from, chunk } = JSON.parse(e.data)
        buffer += chunk

        const idx = this.messages.findIndex(m => m.id === msgId)
        if (idx === -1) {
          this.messages.push({ id: msgId, from, text: buffer })
        } else {
          this.$set(this.messages, idx, { id: msgId, from, text: buffer })
        }
      }

      // SSE の end イベントでクローズ＆参照クリア
      this.evtSource.addEventListener('end', () => {
        this.evtSource.close()
        this.evtSource = null
      })
    }
  }
}
</script>

<style>
/* カスタムスクロールバー */
.space-y-4::-webkit-scrollbar {
  width: 8px;
}
.space-y-4::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

/* Tailwind Prose を有効化する場合 */
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/base.min.css";
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/components.min.css";
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/utilities.min.css";
</style>
