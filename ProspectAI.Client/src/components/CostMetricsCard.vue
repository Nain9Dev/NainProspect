<script setup lang="ts">
import type { CostMetrics } from '../types/contracts'
import { t } from '../locales/i18n'

defineProps<{
  metrics?: CostMetrics
  totalLeads: number
  inTargetBand: number
  withEmail: number
  highPriorityCount: number
}>()
</script>

<template>
  <div class="metrics-card glass-panel">
    <div class="panel-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
          <line x1="12" y1="1" x2="12" y2="23" stroke-width="2"/>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" stroke-width="2"/>
        </svg>
      </div>
      <div>
        <h3>{{ t('metricsTitle') }}</h3>
        <p class="panel-desc">{{ t('metricsSubtitle') }}</p>
      </div>
    </div>

    <!-- Grid of Key KPIs -->
    <div class="kpi-grid">
      <div class="kpi-box">
        <span class="kpi-title">{{ t('totalLeads') }}</span>
        <span class="kpi-value">{{ totalLeads }}</span>
        <span class="kpi-sub">{{ t('obtainedBatch') }}</span>
      </div>

      <div class="kpi-box">
        <span class="kpi-title">{{ t('targetBand') }}</span>
        <span class="kpi-value text-cyan">{{ inTargetBand }}</span>
        <span class="kpi-sub">{{ t('targetSize') }}</span>
      </div>

      <div class="kpi-box">
        <span class="kpi-title">{{ t('roleEmail') }}</span>
        <span class="kpi-value text-emerald">{{ withEmail }}</span>
        <span class="kpi-sub">{{ t('corporateMailbox') }}</span>
      </div>

      <div class="kpi-box">
        <span class="kpi-title">{{ t('highPriority') }}</span>
        <span class="kpi-value text-amber">{{ highPriorityCount }}</span>
        <span class="kpi-sub">{{ t('alertableTelegram') }}</span>
      </div>
    </div>

    <!-- Cost Details -->
    <div class="cost-details glass-card">
      <div class="cost-row">
        <span>{{ t('costThisRun') }}</span>
        <strong class="cost-num">${{ metrics?.coste_usd?.toFixed(6) ?? '0.000000' }} USD</strong>
      </div>
      <div class="cost-row">
        <span>{{ t('costPerLead') }}</span>
        <span class="cost-num">${{ metrics?.coste_por_lead_usd?.toFixed(6) ?? '0.000000' }} USD</span>
      </div>
      <div class="cost-row highlight-row">
        <span>{{ t('cost100Leads') }}</span>
        <strong class="cost-num text-cyan">${{ metrics?.coste_100_leads_usd?.toFixed(4) ?? '0.0000' }} USD</strong>
      </div>
      <div class="token-row">
        <span class="token-tag">In: {{ metrics?.input_tokens ?? 0 }} tok</span>
        <span class="token-tag">Out: {{ metrics?.output_tokens ?? 0 }} tok</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.metrics-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-subtle);
}

.header-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(52, 211, 153, 0.15);
  color: var(--emerald-success);
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

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.kpi-box {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
}

.kpi-title {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  letter-spacing: 0.5px;
}

.kpi-value {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 4px 0 2px;
}

.kpi-sub {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.text-cyan { color: var(--cyan-primary); }
.text-emerald { color: var(--emerald-success); }
.text-amber { color: var(--amber-warn); }

.cost-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.8rem;
}

.cost-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
}

.cost-num {
  font-family: var(--font-mono);
}

.highlight-row {
  padding-top: 6px;
  border-top: 1px dashed var(--border-subtle);
  color: var(--text-primary);
  font-weight: 600;
}

.token-row {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.token-tag {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  color: var(--text-muted);
}
</style>
