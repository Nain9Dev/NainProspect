<script setup lang="ts">
import { ref } from 'vue'
import type { TemplatePreviewResponse } from '../types/contracts'

const props = defineProps<{
  preview: TemplatePreviewResponse | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const copied = ref(false)

function copyHtml() {
  if (!props.preview) return
  navigator.clipboard.writeText(props.preview.full_html)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<template>
  <div v-if="preview" class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-card glass-panel">
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="header-left">
          <span class="badge badge-indigo">{{ preview.sector }}</span>
          <h3>Previsualizacion de Outreach</h3>
        </div>
        <button class="close-btn" @click="emit('close')">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18" stroke-width="2"/>
            <line x1="6" y1="6" x2="18" y2="18" stroke-width="2"/>
          </svg>
        </button>
      </div>

      <!-- Legal Compliance Alert Banner -->
      <div class="compliance-banner">
        <div class="banner-icon">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke-width="2"/>
          </svg>
        </div>
        <div class="banner-text">
          <strong>Compuerta Legal LSSI-CE Art. 21 Activa: Envio Real Bloqueado</strong>
          <p>
            El sistema detiene el pipeline en previsualizacion determinista. No se envia ningun correo
            automaticamente para garantizar el estricto cumplimiento del RGPD (interes legitimo 6.1.f) y LSSI-CE 21.
          </p>
        </div>
      </div>

      <!-- Email Details -->
      <div class="email-meta">
        <div class="meta-row">
          <span class="meta-label">Para:</span>
          <span class="meta-val font-mono">{{ preview.recipient }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Asunto:</span>
          <strong class="meta-val">{{ preview.subject }}</strong>
        </div>
      </div>

      <!-- Live Rendered Frame / Box -->
      <div class="email-preview-box">
        <div class="preview-badge">PUBLICIDAD</div>
        <div class="rendered-body" v-html="preview.body_html"></div>
        <div class="rendered-footer" v-html="preview.legal_footer_html"></div>
      </div>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button class="btn-secondary" @click="copyHtml">
          <span>{{ copied ? 'Copiado al portapapeles' : 'Copiar Codigo HTML' }}</span>
        </button>
        <button class="btn-primary" @click="emit('close')">
          <span>Cerrar</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-card {
  width: 100%;
  max-width: 680px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

h3 {
  font-family: var(--font-display);
  font-size: 1.1rem;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  padding: 4px;
}

.close-btn:hover {
  color: var(--text-primary);
}

.compliance-banner {
  display: flex;
  gap: 12px;
  padding: 12px 20px;
  background: rgba(244, 63, 94, 0.12);
  border-bottom: 1px solid rgba(244, 63, 94, 0.3);
}

.banner-icon {
  color: var(--rose-danger);
  flex-shrink: 0;
  margin-top: 2px;
}

.banner-text strong {
  display: block;
  font-size: 0.8rem;
  color: #fda4af;
}

.banner-text p {
  font-size: 0.72rem;
  color: #fecdd3;
  margin-top: 2px;
  line-height: 1.4;
}

.email-meta {
  padding: 14px 24px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.meta-row {
  display: flex;
  gap: 12px;
  font-size: 0.85rem;
}

.meta-label {
  width: 60px;
  color: var(--text-muted);
}

.meta-val {
  color: var(--text-primary);
}

.font-mono {
  font-family: var(--font-mono);
  color: var(--cyan-primary);
}

.email-preview-box {
  padding: 24px;
  overflow-y: auto;
  background: #0f172a;
  flex: 1;
  font-size: 0.9rem;
  line-height: 1.6;
}

.preview-badge {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--cyan-primary);
  margin-bottom: 14px;
}

.rendered-body {
  color: #f8fafc;
}

.rendered-body :deep(p) {
  margin-bottom: 12px;
}

.rendered-body :deep(strong) {
  color: #38bdf8;
}

.rendered-footer {
  margin-top: 20px;
}

.rendered-footer :deep(hr) {
  border-color: #334155;
}

.rendered-footer :deep(p) {
  font-size: 0.75rem;
  color: #94a3b8;
  line-height: 1.4;
}

.rendered-footer :deep(a) {
  color: #38bdf8;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
}
</style>
