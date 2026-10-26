<script setup lang="ts">
import { ref, onMounted } from 'vue'
import HeaderNav from './components/HeaderNav.vue'
import PipelineControl from './components/PipelineControl.vue'
import CostMetricsCard from './components/CostMetricsCard.vue'
import LeadsTable from './components/LeadsTable.vue'
import TemplateViewerModal from './components/TemplateViewerModal.vue'
import ComplianceNotice from './components/ComplianceNotice.vue'
import ShowcaseHero from './components/ShowcaseHero.vue'
import { SCENARIO_LIMIT, SCENARIO_QUERY } from './services/scenario'

import type {
  SystemConfigResponse,
  EnrichedLead,
  TemplatePreviewResponse,
  CostMetrics,
} from './types/contracts'
import {
  checkHealth,
  fetchConfig,
  fetchLeads,
  runPipeline,
  previewTemplate,
} from './services/api'

const isOnline = ref(false)
const config = ref<SystemConfigResponse | null>(null)
const leads = ref<EnrichedLead[]>([])
const loading = ref(false)
const activeMetrics = ref<CostMetrics | undefined>()

const selectedLead = ref<EnrichedLead | null>(null)
const previewData = ref<TemplatePreviewResponse | null>(null)

// Summary counts
const inTargetBand = ref(0)
const withEmail = ref(0)
const highPriorityCount = ref(0)

async function initialize() {
  isOnline.value = await checkHealth()
  try {
    config.value = await fetchConfig()
    await reloadLeads()
  } catch (e) {
    console.error('Initialization error:', e)
  }
}

async function reloadLeads() {
  try {
    const list = await fetchLeads()
    leads.value = list
    recalculateCounts(list)
  } catch (e) {
    console.error('Failed to load leads:', e)
  }
}

function recalculateCounts(list: EnrichedLead[]) {
  inTargetBand.value = list.filter(l => l.tamano_estimado === 'mediana').length
  withEmail.value = list.filter(l => Boolean(l.email)).length
  highPriorityCount.value = list.filter(l => l.prioridad >= 4).length
}

async function handleExecuteRun(payload: { query: string; limit: number; simulation: boolean }) {
  loading.value = true
  try {
    const response = await runPipeline(payload.query, payload.limit, payload.simulation, false)
    leads.value = response.leads
    activeMetrics.value = response.coste
    recalculateCounts(response.leads)
  } catch (error) {
    alert(`Error ejecutando pipeline: ${(error as Error).message}`)
  } finally {
    loading.value = false
  }
}

/** The guided scenario runs the same pipeline as the launcher, so it works with the API or without it. */
function runScenario(): Promise<void> {
  return handleExecuteRun({ query: SCENARIO_QUERY, limit: SCENARIO_LIMIT, simulation: true })
}

/** "Probar mi búsqueda": takes the visitor to the search field of the launcher. */
function focusOwnSearch() {
  const field = document.getElementById('query-input')
  if (!field) return
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  field.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' })
  field.focus({ preventScroll: true })
}

async function handlePreviewLead(lead: EnrichedLead) {
  selectedLead.value = lead
  try {
    previewData.value = await previewTemplate(lead.industria, lead.id)
  } catch (e) {
    alert(`Error al generar vista previa: ${(e as Error).message}`)
  }
}

function handleCloseModal() {
  selectedLead.value = null
  previewData.value = null
}

onMounted(() => {
  initialize()
  setInterval(async () => {
    isOnline.value = await checkHealth()
  }, 10000)
})
</script>

<template>
  <div class="app-container">
    <HeaderNav
      :is-online="isOnline"
      :scraping-mode="config?.scraping_mode ?? 'SIMULADO'"
      :classification-mode="config?.classification_mode ?? 'SIMULADO'"
    />

    <ShowcaseHero
      :leads="leads"
      :run-scenario="runScenario"
      @view-email="handlePreviewLead"
      @own-search="focusOwnSearch"
    />

    <main class="main-grid">
      <!-- Left Sidebar: Controls, Metrics, and Compliance -->
      <aside class="sidebar">
        <PipelineControl
          :loading="loading"
          @execute="handleExecuteRun"
        />

        <CostMetricsCard
          :metrics="activeMetrics"
          :total-leads="leads.length"
          :in-target-band="inTargetBand"
          :with-email="withEmail"
          :high-priority-count="highPriorityCount"
        />

        <ComplianceNotice />
      </aside>

      <!-- Right Main Content: Leads Table -->
      <section class="content-area">
        <LeadsTable
          :leads="leads"
          :loading="loading"
          @preview-lead="handlePreviewLead"
        />
      </section>
    </main>

    <!-- Modal for Email Template Preview -->
    <TemplateViewerModal
      :preview="previewData"
      @close="handleCloseModal"
    />
  </div>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-area {
  display: flex;
  flex-direction: column;
}
</style>
