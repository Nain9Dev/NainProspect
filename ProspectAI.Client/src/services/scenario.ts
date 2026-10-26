/**
 * Logic of the guided scenario (specs/002-showcase-header).
 *
 * Kept free of Vue so it can be tested with the Node runner and no extra dependency. The
 * scenario never invents a figure: every number it shows is derived from the leads the run
 * returned, so it keeps telling the truth about the engine whichever data it receives.
 */
import type { EnrichedLead } from '../types/contracts'

export type ScenarioStep = 'capture' | 'classify' | 'comply' | 'outreach'

export const SCENARIO_STEPS: readonly ScenarioStep[] = ['capture', 'classify', 'comply', 'outreach']

/** The first launcher preset, in simulation: the search the scenario runs for the visitor. */
export const SCENARIO_QUERY = 'empresas de logistica en Madrid'

/** Leads the scenario reads back. A run returns its own leads first, ahead of the earlier sample. */
export const SCENARIO_LIMIT = 10

/** Priority from which a lead counts as high (the same threshold the table and the metrics use). */
const HIGH_PRIORITY = 4

export interface ScenarioSummary {
  found: number
  inTargetBand: number
  highPriority: number
  withRoleEmail: number
  discarded: number
}

export function summarize(leads: readonly EnrichedLead[]): ScenarioSummary {
  return {
    found: leads.length,
    inTargetBand: leads.filter((lead) => lead.tamano_estimado === 'mediana').length,
    highPriority: leads.filter((lead) => lead.prioridad >= HIGH_PRIORITY).length,
    withRoleEmail: leads.filter((lead) => Boolean(lead.email)).length,
    discarded: leads.filter((lead) => lead.estado === 'descartado').length,
  }
}

/**
 * The lead whose email the scenario ends on: the highest priority among those with a mailbox,
 * preferring the target size band when priorities tie. The first one wins a full tie, so the
 * choice is stable between renders.
 */
export function pickShowcaseLead(leads: readonly EnrichedLead[]): EnrichedLead | null {
  let best: EnrichedLead | null = null

  for (const lead of leads) {
    if (!lead.email) continue

    if (
      best === null ||
      lead.prioridad > best.prioridad ||
      (lead.prioridad === best.prioridad && inBand(lead) && !inBand(best))
    ) {
      best = lead
    }
  }

  return best
}

function inBand(lead: EnrichedLead): boolean {
  return lead.tamano_estimado === 'mediana'
}

/** Milliseconds each stage stays on screen. All zero for a visitor who asked for less motion (SH-007). */
export function scenarioDelays(reducedMotion: boolean): number[] {
  return reducedMotion ? SCENARIO_STEPS.map(() => 0) : [700, 1300, 1300, 1100]
}

/** Replaces `{name}` placeholders, leaving an unknown one visible rather than printing "undefined". */
export function format(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (whole, key: string) => (key in values ? String(values[key]) : whole))
}
