<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { t } from '../locales/i18n'
import type { EnrichedLead } from '../types/contracts'
import {
  SCENARIO_STEPS,
  format,
  pickShowcaseLead,
  SCENARIO_LIMIT,
  scenarioDelays,
  summarize,
} from '../services/scenario'

const props = defineProps<{
  leads: EnrichedLead[]
  /** Runs the pipeline for the scenario and resolves when the leads are in. */
  runScenario: () => Promise<void>
}>()

const emit = defineEmits<{
  (e: 'view-email', lead: EnrichedLead): void
  (e: 'own-search'): void
}>()

type Phase = 'idle' | 'running' | 'done'

const phase = ref<Phase>('idle')
/** Index of the stage on screen; -1 before the scenario starts. */
const current = ref(-1)
/** Leads the scenario itself produced, so the figures do not drift if the table is filtered later. */
const scenarioLeads = ref<EnrichedLead[]>([])
let timer: ReturnType<typeof setTimeout> | null = null

const summary = computed(() => summarize(scenarioLeads.value))
const showcaseLead = computed(() => pickShowcaseLead(scenarioLeads.value))

const prefersReducedMotion = () =>
  typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

const stepKeys = {
  capture: { title: 'stepCaptureTitle', body: 'stepCaptureBody' },
  classify: { title: 'stepClassifyTitle', body: 'stepClassifyBody' },
  comply: { title: 'stepComplyTitle', body: 'stepComplyBody' },
  outreach: { title: 'stepOutreachTitle', body: 'stepOutreachBody' },
} as const

function metricFor(index: number): string {
  const s = summary.value

  switch (SCENARIO_STEPS[index]) {
    case 'capture':
      return format(t('metricFound'), { n: s.found })
    case 'classify':
      return format(t('metricClassified'), { band: s.inTargetBand, high: s.highPriority })
    case 'comply':
      return format(t('metricCompliance'), { mail: s.withRoleEmail, out: s.discarded })
    default:
      return showcaseLead.value ? t('metricOutreach') : t('metricOutreachNone')
  }
}

function stateOf(index: number): 'done' | 'active' | 'pending' {
  if (phase.value === 'done' || index < current.value) return 'done'
  return index === current.value ? 'active' : 'pending'
}

const liveMessage = computed(() => {
  if (phase.value === 'idle') return ''
  if (phase.value === 'done') return t('heroDone')
  const key = stepKeys[SCENARIO_STEPS[Math.max(current.value, 0)]].title
  return `${current.value + 1}/${SCENARIO_STEPS.length}: ${t(key)}`
})

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => {
    if (ms <= 0) return resolve()
    timer = setTimeout(resolve, ms)
  })
}

async function start() {
  if (phase.value === 'running') return

  const delays = scenarioDelays(prefersReducedMotion())
  phase.value = 'running'
  current.value = 0
  scenarioLeads.value = []

  await Promise.all([props.runScenario(), wait(delays[0])])
  // The table now holds the run's leads: the scenario keeps its own copy for the figures.
  scenarioLeads.value = props.leads.slice(0, SCENARIO_LIMIT)

  for (let step = 1; step < SCENARIO_STEPS.length; step += 1) {
    current.value = step
    await wait(delays[step])
  }

  phase.value = 'done'
}

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})
</script>

<template>
  <section class="hero glass-panel" aria-labelledby="hero-title">
    <div class="hero-copy">
      <span class="eyebrow">{{ t('heroEyebrow') }}</span>
      <h2 id="hero-title" class="hero-title">{{ t('heroTitle') }}</h2>
      <p class="hero-lead">{{ t('heroLead') }}</p>

      <div class="hero-actions">
        <button type="button" class="btn-primary" :disabled="phase === 'running'" @click="start">
          <span v-if="phase === 'running'" class="spinner" aria-hidden="true"></span>
          <svg v-else viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" aria-hidden="true">
            <polygon points="5 3 19 12 5 21 5 3" stroke-width="2" />
          </svg>
          {{ phase === 'running' ? t('heroRunning') : phase === 'done' ? t('heroRunAgain') : t('heroRun') }}
        </button>
        <button type="button" class="btn-link" @click="emit('own-search')">{{ t('heroOwn') }}</button>
      </div>

      <p class="hero-note">{{ t('heroNote') }}</p>
    </div>

    <ol class="steps" :aria-label="t('heroStepsLabel')">
      <li
        v-for="(id, index) in SCENARIO_STEPS"
        :key="id"
        class="step"
        :class="`is-${stateOf(index)}`"
        :aria-current="stateOf(index) === 'active' ? 'step' : undefined"
      >
        <span class="step-number" aria-hidden="true">{{ index + 1 }}</span>
        <div class="step-text">
          <strong>{{ t(stepKeys[id].title) }}</strong>
          <span class="step-body">{{ t(stepKeys[id].body) }}</span>
          <span v-if="stateOf(index) === 'done'" class="step-metric">{{ metricFor(index) }}</span>
        </div>
      </li>
    </ol>

    <div v-if="phase === 'done' && showcaseLead" class="hero-cta">
      <button type="button" class="btn-primary" @click="emit('view-email', showcaseLead)">
        {{ t('heroViewEmail') }}
      </button>
    </div>

    <p class="visually-hidden" role="status" aria-live="polite">{{ liveMessage }}</p>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
  gap: 28px 36px;
  align-items: center;
  margin-bottom: 20px;
  padding: clamp(20px, 3vw, 32px);
  background:
    radial-gradient(circle at 12% 0%, rgba(56, 189, 248, 0.16), transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(129, 140, 248, 0.14), transparent 45%),
    var(--bg-card);
}

.eyebrow {
  display: block;
  margin-bottom: 10px;
  color: var(--cyan-primary);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.hero-title {
  max-width: 20ch;
  margin-bottom: 12px;
  font-family: var(--font-display);
  font-size: clamp(1.7rem, 3.4vw, 2.5rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.hero-lead {
  max-width: 34rem;
  color: var(--text-secondary);
  font-size: 0.98rem;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
  margin-top: 20px;
}

.btn-link {
  min-height: 44px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--cyan-primary);
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.btn-link:hover {
  text-decoration: underline;
}

.hero-note {
  max-width: 34rem;
  margin-top: 14px;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 10px;
  list-style: none;
}

.step {
  display: flex;
  gap: 14px;
  padding: 12px 14px;
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.5);
  transition: border-color 0.3s ease, background 0.3s ease, opacity 0.3s ease;
}

.step.is-pending {
  opacity: 0.55;
}

.step.is-active {
  border-color: var(--border-active);
  background: rgba(56, 189, 248, 0.1);
  box-shadow: 0 0 0 3px var(--cyan-glow);
}

.step.is-done {
  border-color: rgba(52, 211, 153, 0.35);
}

.step-number {
  display: grid;
  flex: none;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.07);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 700;
}

.is-active .step-number {
  background: var(--cyan-primary);
  color: #04121f;
}

.is-done .step-number {
  background: var(--emerald-success);
  color: #052e1c;
}

.step-text {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 2px;
}

.step-body {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

/* The figure of a finished stage: a pill with text, so it never relies on colour alone. */
.step-metric {
  align-self: flex-start;
  margin-top: 6px;
  padding: 2px 10px;
  border: 1px solid rgba(52, 211, 153, 0.4);
  border-radius: 999px;
  background: rgba(52, 211, 153, 0.12);
  color: var(--emerald-success);
  font-family: var(--font-mono);
  font-size: 0.74rem;
  font-weight: 600;
}

.hero-cta {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

@media (prefers-reduced-motion: no-preference) {
  .step.is-done .step-metric {
    animation: pop 0.4s ease both;
  }
}

@keyframes pop {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 62rem) {
  .hero {
    grid-template-columns: minmax(0, 1fr);
  }

  .hero-cta {
    justify-content: flex-start;
  }
}
</style>
