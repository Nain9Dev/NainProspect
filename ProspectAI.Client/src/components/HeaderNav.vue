<script setup lang="ts">
defineProps<{
  isOnline: boolean
  scrapingMode: string
  classificationMode: string
}>()
</script>

<template>
  <header class="header glass-panel">
    <div class="brand">
      <div class="logo-box">
        <svg viewBox="0 0 24 24" class="logo-icon" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2" />
          <line x1="16.5" y1="16.5" x2="22" y2="22" stroke-width="2" stroke-linecap="round" />
          <circle cx="11" cy="11" r="3" fill="#38bdf8" />
        </svg>
      </div>
      <div class="titles">
        <div class="title-row">
          <h1>NainProspect</h1>
          <span class="badge badge-indigo">Gateway B2B</span>
          <span class="badge badge-rose">Compuerta LSSI-CE</span>
        </div>
        <p class="subtitle">Sourcing de empresas B2B, enriquecimiento Haiku 4.5 y compuerta legal LSSI-CE 21</p>
      </div>
    </div>

    <div class="status-bar">
      <div class="status-pill" :class="{ 'online': isOnline, 'offline': !isOnline }">
        <span class="dot"></span>
        <span class="text">{{ isOnline ? 'API Conectada (:8106)' : 'Motor Autónomo Client-Side (0,00 €)' }}</span>
      </div>

      <div class="mode-tags">
        <span class="mode-tag" :title="scrapingMode">Scraping: {{ scrapingMode.split(' ')[0] }}</span>
        <span class="mode-tag" :title="classificationMode">IA: {{ classificationMode.split(' ')[0] }}</span>
      </div>

      <a
        href="https://github.com/Nain9Dev/ProspectAI"
        target="_blank"
        rel="noopener"
        class="docs-link btn-secondary"
      >
        <span>Docs & Código</span>
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke-width="2"/>
          <polyline points="15 3 21 3 21 9" stroke-width="2"/>
          <line x1="10" y1="14" x2="21" y2="3" stroke-width="2"/>
        </svg>
      </a>
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(129, 140, 248, 0.2) 100%);
  border: 1px solid rgba(56, 189, 248, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  width: 24px;
  height: 24px;
  color: #38bdf8;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

h1 {
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  background: linear-gradient(to right, #ffffff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.status-bar {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: var(--font-mono);
}

.status-pill.online {
  background: rgba(52, 211, 153, 0.1);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.3);
}

.status-pill.offline {
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 8px currentColor;
}

.mode-tags {
  display: flex;
  gap: 8px;
}

.mode-tag {
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
}

.docs-link {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
</style>
