<template>
  <!-- Toast alert rendered in <body> for viewport‑relative positioning -->
  <teleport to="body">
    <transition name="fade-alert">
      <div
        v-if="visible"
        class="alert toast-box"
        :class="['alert-' + type, position]"
      >
        {{ message }}
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message:  String,
  type:     { type: String, default: 'success' }, // success | danger | info …
  duration: { type: Number, default: 2000 },      // ms
  position: { type: String, default: 'top' }      // 'top' | 'bottom'
})

const visible = ref(false)

watch(
  () => props.message,
  msg => {
    if (!msg) return
    visible.value = true
    setTimeout(() => (visible.value = false), props.duration)
  },
  { immediate: true }
)
</script>

<style scoped>
/***********************
 * Toast Core Style    *
 ***********************/
.toast-box {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none;                 /* does not block clicks */
  z-index: 12000;                      /* very front */

  /* Compact size */
  padding: 0.5rem 0.9rem;
  font-size: 0.85rem;
  line-height: 1.3;
  border-radius: 0.4rem;
  box-shadow: 0 0.25rem 0.6rem rgba(0,0,0,.12);
  max-width: 70vw;
  min-width: 180px;
  white-space: pre-line;
}

/* Position modifiers – safe‑area support */
.toast-box.top    { top:    calc(env(safe-area-inset-top, 0px)    + 0.75rem); }
.toast-box.bottom { bottom: calc(env(safe-area-inset-bottom, 0px) + 0.75rem); }

/* Fade transition */
.fade-alert-enter-active,
.fade-alert-leave-active {
  transition: opacity .25s ease;
}
.fade-alert-enter-from,
.fade-alert-leave-to {
  opacity: 0;
}
</style>
