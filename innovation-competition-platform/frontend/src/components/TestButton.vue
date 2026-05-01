<template>
  <button
    class="test-btn"
    :class="[
      `test-btn--${variant}`,
      `test-btn--${size}`,
      {
        'test-btn--loading': loading,
        'test-btn--disabled': disabled,
        'test-btn--icon-only': iconOnly,
        'test-btn--circle': circle,
        'test-btn--gradient': gradient,
      }
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span class="test-btn__content">
      <span v-if="$slots.icon" class="test-btn__icon">
        <slot name="icon" />
      </span>
      <span v-if="loading" class="test-btn__spinner"></span>
      <span v-if="!iconOnly" class="test-btn__text">
        <slot />
      </span>
    </span>
    <span v-if="!disabled && !loading && !iconOnly" class="test-btn__glow"></span>
  </button>
</template>

<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'medium' },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  iconOnly: { type: Boolean, default: false },
  circle: { type: Boolean, default: false },
  gradient: { type: Boolean, default: false }
})

const emit = defineEmits(['click'])

const handleClick = (e) => {
  if (!props.disabled && !props.loading) emit('click', e)
}
</script>

<style scoped>
.test-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 600;
  letter-spacing: 0.01em;
  border: none;
  outline: none;
  cursor: pointer;
  white-space: nowrap;
  user-select: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.test-btn:focus-visible {
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.35);
}

.test-btn__content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.test-btn__text {
  line-height: 1.2;
}

.test-btn__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.test-btn__glow {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

/* Size variants */
.test-btn--small {
  padding: 7px 16px;
  font-size: 13px;
  border-radius: 9px;
  min-height: 32px;
}
.test-btn--medium {
  padding: 10px 22px;
  font-size: 14px;
  border-radius: 11px;
  min-height: 40px;
}
.test-btn--large {
  padding: 14px 30px;
  font-size: 15px;
  border-radius: 13px;
  min-height: 48px;
}

/* Icon only sizing */
.test-btn--icon-only.test-btn--small { padding: 7px; width: 32px; height: 32px; }
.test-btn--icon-only.test-btn--medium { padding: 10px; width: 40px; height: 40px; }
.test-btn--icon-only.test-btn--large { padding: 14px; width: 48px; height: 48px; }

/* Circle variant */
.test-btn--circle { border-radius: 50%; }

/* Primary - Indigo (#4F46E5) */
.test-btn--primary {
  background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3), inset 0 1px 0 rgba(255,255,255,0.12);
}
.test-btn--primary:hover:not(:disabled):not(.test-btn--loading) {
  background: linear-gradient(135deg, #4338CA 0%, #5B50ED 100%);
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.45), inset 0 1px 0 rgba(255,255,255,0.15);
  transform: translateY(-1px);
}
.test-btn--primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 6px rgba(79, 70, 229, 0.3);
}
.test-btn--primary .test-btn__glow {
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.18), transparent 60%);
}
.test-btn--primary:hover .test-btn__glow { opacity: 1; }

/* Secondary */
.test-btn--secondary {
  background: #EEF2FF;
  color: #4338CA;
  border: 1px solid rgba(79, 70, 229, 0.15);
}
.test-btn--secondary:hover:not(:disabled):not(.test-btn--loading) {
  background: #E0E7FF;
  border-color: rgba(79, 70, 229, 0.28);
  transform: translateY(-1px);
  box-shadow: 0 2px 10px rgba(79, 70, 229, 0.12);
}
.test-btn--secondary:active:not(:disabled) { transform: translateY(0); }

/* Outline */
.test-btn--outline {
  background: transparent;
  color: #4F46E5;
  border: 1.5px solid #C7D2FE;
}
.test-btn--outline:hover:not(:disabled):not(.test-btn--loading) {
  background: rgba(79, 70, 229, 0.04);
  border-color: #A5B4FC;
  transform: translateY(-1px);
}
.test-btn--outline:active:not(:disabled) { transform: translateY(0); }

/* Ghost */
.test-btn--ghost {
  background: transparent;
  color: #6366F1;
}
.test-btn--ghost:hover:not(:disabled):not(.test-btn--loading) {
  background: rgba(99, 102, 241, 0.07);
  color: #4F46E5;
}

/* Accent / CTA - Orange (#F97316) */
.test-btn--accent {
  background: linear-gradient(135deg, #F97316 0%, #FB923C 100%);
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(249, 115, 22, 0.3), inset 0 1px 0 rgba(255,255,255,0.15);
}
.test-btn--accent:hover:not(:disabled):not(.test-btn--loading) {
  background: linear-gradient(135deg, #EA580C 0%, #F97316 100%);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.45);
  transform: translateY(-1px);
}
.test-btn--accent:active:not(:disabled) { transform: translateY(0); }

/* Gradient accent (dual gradient) */
.test-btn--gradient {
  background: linear-gradient(135deg, #4F46E5 0%, #F97316 100%);
  color: #ffffff;
  box-shadow: 0 2px 14px rgba(79, 70, 229, 0.3), 0 2px 14px rgba(249, 115, 22, 0.2);
}
.test-btn--gradient:hover:not(:disabled):not(.test-btn--loading) {
  background: linear-gradient(135deg, #4338CA 0%, #EA580C 100%);
  box-shadow: 0 4px 24px rgba(79, 70, 229, 0.45), 0 4px 24px rgba(249, 115, 22, 0.3);
  transform: translateY(-1px);
}

/* Loading state */
.test-btn--loading {
  cursor: wait;
  opacity: 0.85;
}

.test-btn__spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: testBtnSpin 0.65s linear infinite;
}

@keyframes testBtnSpin {
  to { transform: rotate(360deg); }
}

/* Disabled state */
.test-btn:disabled,
.test-btn--disabled {
  cursor: not-allowed;
  opacity: 0.45;
  transform: none !important;
  box-shadow: none !important;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .test-btn { transition: none; }
  .test-btn__spinner { animation-duration: 1.5s; }
  .test-btn:hover:not(:disabled):not(.test-btn--loading) { transform: none; }
}
</style>
