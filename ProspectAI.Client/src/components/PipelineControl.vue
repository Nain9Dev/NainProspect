<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'execute', payload: { query: string; limit: number; simulation: boolean }): void
}>()

defineProps<{
  loading: boolean
}>()

const query = ref('empresas de logistica en Madrid')
const limit = ref(10)
const forceSimulation = ref(true)

const PRESETS = [
  'empresas de logistica en Madrid',
  'empresas de software en Valencia',
  'cadenas de retail en Barcelona',
  'suministros industriales en Bilbao',
]

function selectPreset(preset: string) {
  query.value = preset
}

function handleExecute() {
  if (!query.value.trim()) return
  emit('execute', {
    query: query.value.trim(),
    limit: limit.value,
    simulation: forceSimulation.value,
  })
}
</script>

<template>
  <div class="control-panel glass-panel">
    <div class="panel-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
          <polygon points="5 3 19 12 5 21 5 3" stroke-width="2" />
        </svg>
      </div>
      <div>
        <h3>Lanzador de Pipeline</h3>
        <p class="panel-desc">Sourcing de empresas y clasificacion IA determinista</p>
      </div>
    </div>

    <form @submit.prevent="handleExecute" class="form">
      <div class="field-group">
        <label for="query-input">Consulta de Busqueda (Google Places / Web)</label>
        <input
          id="query-input"
          v-model="query"
          type="text"
          class="input-field"
          placeholder="Ej: empresas de logistica en Madrid"
          required
        />
      </div>

      <div class="presets">
        <span class="preset-label">Consultas rapidas:</span>
        <div class="preset-chips">
          <button
            v-for="p in PRESETS"
            :key="p"
            type="button"
            class="preset-chip"
            :class="{ 'active': query === p }"
            @click="selectPreset(p)"
          >
            {{ p }}
          </button>
        </div>
      </div>

      <div class="row-fields">
        <div class="field-group limit-field">
          <label for="limit-select">Limite de Leads</label>
          <select id="limit-select" v-model="limit" class="input-field select-field">
            <option :value="5">5 leads (muestreo ultra rapido)</option>
            <option :value="10">10 leads (benchmark estandar)</option>
            <option :value="20">20 leads (lote completo)</option>
          </select>
        </div>

        <div class="field-group toggle-group">
          <label class="toggle-label">
            <input
              type="checkbox"
              v-model="forceSimulation"
              class="toggle-checkbox"
            />
            <span class="toggle-text">
              <strong>Modo Simulacion</strong>
              <small>Usa fixtures sinteticos sin coste de API</small>
            </span>
          </label>
        </div>
      </div>

      <button
        type="submit"
        class="btn-primary run-button"
        :disabled="loading || !query.trim()"
      >
        <svg v-if="!loading" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
          <polyline points="23 4 23 10 17 10" stroke-width="2"/>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" stroke-width="2"/>
        </svg>
        <span v-else class="spinner"></span>
        <span>{{ loading ? 'Ejecutando Sourcing & IA...' : 'Ejecutar Pipeline' }}</span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.control-panel {
  padding: 20px;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-subtle);
}

.header-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(56, 189, 248, 0.15);
  color: var(--cyan-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

h3 {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
}

.panel-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.presets {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.preset-label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.preset-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.preset-chip {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.preset-chip:hover,
.preset-chip.active {
  background: rgba(56, 189, 248, 0.15);
  border-color: rgba(56, 189, 248, 0.4);
  color: var(--cyan-primary);
}

.row-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.select-field {
  cursor: pointer;
}

.toggle-group {
  background: rgba(0, 0, 0, 0.2);
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.toggle-checkbox {
  width: 18px;
  height: 18px;
  accent-color: var(--cyan-primary);
  cursor: pointer;
}

.toggle-text {
  display: flex;
  flex-direction: column;
}

.toggle-text strong {
  font-size: 0.8rem;
  color: var(--text-primary);
}

.toggle-text small {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.run-button {
  justify-content: center;
  margin-top: 6px;
  padding: 12px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
