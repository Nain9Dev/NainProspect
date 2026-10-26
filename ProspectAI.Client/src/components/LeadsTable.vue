<script setup lang="ts">
import { ref, computed } from 'vue'
import type { EnrichedLead } from '../types/contracts'
import { t } from '../locales/i18n'

const props = defineProps<{
  leads: EnrichedLead[]
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'preview-lead', lead: EnrichedLead): void
}>()

const search = ref('')
const filterSector = ref('todos')
const filterPriority = ref<number | 'todos'>('todos')
const filterEmailOnly = ref(false)

const filteredLeads = computed(() => {
  return props.leads.filter(lead => {
    if (search.value) {
      const q = search.value.toLowerCase()
      const match = lead.nombre.toLowerCase().includes(q) ||
                    (lead.ciudad?.toLowerCase().includes(q) ?? false) ||
                    (lead.email?.toLowerCase().includes(q) ?? false)
      if (!match) return false
    }

    if (filterSector.value !== 'todos') {
      if (lead.industria !== filterSector.value) return false
    }

    if (filterPriority.value !== 'todos') {
      if (lead.prioridad < (filterPriority.value as number)) return false
    }

    if (filterEmailOnly.value) {
      if (!lead.email) return false
    }

    return true
  })
})

function getPriorityBadgeClass(prio: number): string {
  if (prio === 5) return 'badge-emerald'
  if (prio === 4) return 'badge-cyan'
  if (prio === 3) return 'badge-indigo'
  if (prio === 2) return 'badge-amber'
  return 'badge-rose'
}
</script>

<template>
  <div class="table-container glass-panel">
    <!-- Filter Bar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65" stroke-width="2"/>
        </svg>
        <input
          v-model="search"
          type="text"
          class="search-input"
          :placeholder="t('searchPlaceholder')"
        />
      </div>

      <div class="filters">
        <select v-model="filterSector" class="filter-select">
          <option value="todos">{{ t('allSectors') }}</option>
          <option value="logistica">{{ t('secLogistics') }}</option>
          <option value="tecnologia">{{ t('secTech') }}</option>
          <option value="retail">{{ t('secRetail') }}</option>
          <option value="industrial">{{ t('secIndustrial') }}</option>
          <option value="alimentacion">{{ t('secFood') }}</option>
          <option value="otro">{{ t('secOther') }}</option>
        </select>

        <select v-model="filterPriority" class="filter-select">
          <option value="todos">{{ t('allPriorities') }}</option>
          <option :value="5">{{ t('prioMaxOnly') }}</option>
          <option :value="4">{{ t('prioHighOnly') }}</option>
        </select>

        <label class="checkbox-filter">
          <input type="checkbox" v-model="filterEmailOnly" />
          <span>{{ t('filterEmailOnly') }}</span>
        </label>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="leads-table">
        <thead>
          <tr>
            <th>{{ t('thPriority') }}</th>
            <th>{{ t('thCompany') }}</th>
            <th>{{ t('thIndustry') }}</th>
            <th>{{ t('thSize') }}</th>
            <th>{{ t('thConfidence') }}</th>
            <th>{{ t('thRoleEmail') }}</th>
            <th class="text-right">{{ t('thAction') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7" class="empty-state">
              <span class="spinner"></span>
              <p>{{ t('loadingLeads') }}</p>
            </td>
          </tr>
          <tr v-else-if="filteredLeads.length === 0">
            <td colspan="7" class="empty-state">
              <p>{{ t('noLeadsMatch') }}</p>
            </td>
          </tr>
          <tr v-else v-for="lead in filteredLeads" :key="lead.id" class="lead-row">
            <td>
              <span class="badge" :class="getPriorityBadgeClass(lead.prioridad)">
                P{{ lead.prioridad }}
              </span>
            </td>

            <td class="company-cell">
              <strong>{{ lead.nombre }}</strong>
              <small v-if="lead.ciudad">{{ lead.ciudad }}, {{ lead.pais }}</small>
            </td>

            <td>
              <span class="sector-tag">{{ lead.industria }}</span>
            </td>

            <td>
              <div class="size-box">
                <span class="size-name">{{ lead.tamano_estimado }}</span>
                <small v-if="lead.empleados_declarados" class="headcount-tag">
                  {{ lead.empleados_declarados }} {{ t('empAbbr') }}
                </small>
              </div>
            </td>

            <td>
              <span class="conf-badge" :class="'conf-' + lead.confianza">
                {{ lead.confianza }}
              </span>
            </td>

            <td>
              <span v-if="lead.email" class="email-text">
                {{ lead.email }}
              </span>
              <span v-else class="no-email">{{ t('noRoleMailbox') }}</span>
            </td>

            <td class="text-right">
              <button
                class="btn-secondary btn-sm"
                @click="emit('preview-lead', lead)"
                :title="t('btnViewEmail')"
              >
                <span>{{ t('btnViewEmail') }}</span>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke-width="2"/>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.table-container {
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 6px 12px;
  width: 320px;
  color: var(--text-muted);
}

.search-input {
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.85rem;
  width: 100%;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.filter-select {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-size: 0.8rem;
  padding: 6px 10px;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
}

.checkbox-filter {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.table-wrapper {
  overflow-x: auto;
}

.leads-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.85rem;
}

th {
  padding: 12px 18px;
  font-size: 0.72rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  letter-spacing: 0.5px;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid var(--border-subtle);
}

td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--border-subtle);
  vertical-align: middle;
}

.lead-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.company-cell {
  display: flex;
  flex-direction: column;
}

.company-cell strong {
  color: var(--text-primary);
}

.company-cell small {
  color: var(--text-muted);
  font-size: 0.72rem;
}

.sector-tag {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: capitalize;
}

.size-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.size-name {
  text-transform: capitalize;
}

.headcount-tag {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--cyan-primary);
}

.conf-badge {
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.conf-alta { background: rgba(52, 211, 153, 0.15); color: #34d399; }
.conf-media { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
.conf-baja { background: rgba(148, 163, 184, 0.15); color: #94a3b8; }

.email-text {
  font-family: var(--font-mono);
  color: #38bdf8;
  font-size: 0.78rem;
}

.no-email {
  color: var(--text-muted);
  font-style: italic;
  font-size: 0.75rem;
}

.text-right {
  text-align: right;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.75rem;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: var(--text-muted);
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(56, 189, 248, 0.3);
  border-top-color: var(--cyan-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
