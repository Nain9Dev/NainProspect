<template>
  <div class="compliance-notice glass-card">
    <div class="notice-header">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-width="2"/>
      </svg>
      <h4>Garantias de Cumplimiento Legal (RGPD & LSSI-CE)</h4>
    </div>
    <ul class="rule-list">
      <li>
        <strong>Solo direcciones de rol:</strong> El sistema descarta automaticamente correos con nombre de persona (ej. <em>juan@...</em>) para mantenerse exclusivamente en el plano de persona juridica.
      </li>
      <li>
        <strong>Pie legal determinista:</strong> Construido en codigo segun los requisitos del art. 21 de la LSSI-CE, nunca al azar de un modelo de IA.
      </li>
      <li>
        <strong>Aislamiento de datos:</strong> La carpeta <code>data/</code> y los CSVs jamas se versionan en Git.
      </li>
    </ul>
  </div>
</template>

<style scoped>
.compliance-notice {
  font-size: 0.75rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.notice-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--cyan-primary);
  margin-bottom: 8px;
}

h4 {
  font-size: 0.8rem;
  font-weight: 600;
}

.rule-list {
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rule-list li strong {
  color: var(--text-primary);
}

code {
  font-family: var(--font-mono);
  background: rgba(255, 255, 255, 0.08);
  padding: 1px 4px;
  border-radius: 4px;
}
</style>
