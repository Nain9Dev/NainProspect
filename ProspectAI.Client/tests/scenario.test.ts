import test from 'node:test'
import assert from 'node:assert/strict'
import { format, pickShowcaseLead, scenarioDelays, summarize, SCENARIO_STEPS } from '../src/services/scenario.ts'
import type { EnrichedLead } from '../src/types/contracts.ts'

function lead(overrides: Partial<EnrichedLead>): EnrichedLead {
  return {
    id: 'x',
    nombre: 'Empresa',
    pais: 'España',
    fuente: 'test',
    industria: 'logistica',
    tamano_estimado: 'mediana',
    prioridad: 3,
    confianza: 'media',
    motivo: '',
    estado: 'cualificado',
    created_at: '2026-10-26T10:00:00Z',
    email: 'info@empresa.es',
    ...overrides,
  }
}

test('SH-003: the figures come from the leads of the run', () => {
  const leads = [
    lead({ id: 'a', prioridad: 5, tamano_estimado: 'mediana', email: 'a@a.es' }),
    lead({ id: 'b', prioridad: 4, tamano_estimado: 'mediana', email: 'b@b.es' }),
    lead({ id: 'c', prioridad: 3, tamano_estimado: 'pequena', email: null }),
    lead({ id: 'd', prioridad: 2, tamano_estimado: 'grande', email: 'd@d.es', estado: 'descartado' }),
  ]

  assert.deepEqual(summarize(leads), {
    found: 4,
    inTargetBand: 2,
    highPriority: 2,
    withRoleEmail: 3,
    discarded: 1,
  })
})

test('SH-003: an empty run has zero figures, not undefined', () => {
  assert.deepEqual(summarize([]), { found: 0, inTargetBand: 0, highPriority: 0, withRoleEmail: 0, discarded: 0 })
})

test('SH-003: the stages are the four of the pipeline, in order', () => {
  assert.deepEqual([...SCENARIO_STEPS], ['capture', 'classify', 'comply', 'outreach'])
})

test('SH-004: the best lead has the top priority and a mailbox', () => {
  const best = pickShowcaseLead([
    lead({ id: 'low', prioridad: 3 }),
    lead({ id: 'no-mail', prioridad: 5, email: null }),
    lead({ id: 'best', prioridad: 5 }),
    lead({ id: 'also', prioridad: 4 }),
  ])

  assert.equal(best?.id, 'best')
})

test('SH-004: among equal priorities the target size band wins', () => {
  const best = pickShowcaseLead([
    lead({ id: 'big', prioridad: 5, tamano_estimado: 'grande' }),
    lead({ id: 'mid', prioridad: 5, tamano_estimado: 'mediana' }),
  ])

  assert.equal(best?.id, 'mid')
})

test('SH-004: no lead with a mailbox means no email to show', () => {
  assert.equal(pickShowcaseLead([lead({ email: null })]), null)
  assert.equal(pickShowcaseLead([]), null)
})

test('SH-007: reduced motion removes every delay', () => {
  assert.deepEqual(scenarioDelays(true), [0, 0, 0, 0])
})

test('SH-003: with motion the stages are paced and each takes time', () => {
  const delays = scenarioDelays(false)

  assert.equal(delays.length, SCENARIO_STEPS.length)
  assert.ok(delays.every((ms) => ms >= 400 && ms <= 2500))
})

test('SH-006: placeholders are replaced, and an unknown one is left visible', () => {
  assert.equal(format('{n} empresas en {band}', { n: 12, band: '50-250' }), '12 empresas en 50-250')
  assert.equal(format('{n} y {missing}', { n: 1 }), '1 y {missing}')
})
