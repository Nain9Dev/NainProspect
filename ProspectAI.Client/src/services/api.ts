import type {
  SystemConfigResponse,
  PipelineRunResponse,
  EnrichedLead,
  TemplatePreviewResponse,
} from '../types/contracts'
import {
  getMockConfig,
  getMockLeads,
  runMockPipeline,
  getMockTemplatePreview,
  getMockMetrics,
} from './mockProspectEngine'

const API_BASE = '/api'
let useMock = false

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch('/health', { signal: AbortSignal.timeout(2000) })
    if (res.ok) {
      const data = await res.json()
      if (data.status === 'healthy') {
        useMock = false
        return true
      }
    }
  } catch {
    // Backend offline; use standalone mock engine
  }
  useMock = true
  return false
}

export async function fetchConfig(): Promise<SystemConfigResponse> {
  if (useMock) return getMockConfig()
  try {
    const res = await fetch(`${API_BASE}/config`, { signal: AbortSignal.timeout(2500) })
    if (!res.ok) throw new Error('Backend responded with error')
    return await res.json()
  } catch {
    useMock = true
    return getMockConfig()
  }
}

export async function runPipeline(
  query: string,
  limite: number = 10,
  forceSimulation: boolean = true,
  notificar: boolean = false,
): Promise<PipelineRunResponse> {
  if (useMock) return runMockPipeline(query, limite, forceSimulation, notificar)
  try {
    const res = await fetch(`${API_BASE}/pipeline/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        limite,
        force_simulation: forceSimulation,
        notificar,
      }),
      signal: AbortSignal.timeout(5000),
    })
    if (!res.ok) throw new Error(`Fallo en la ejecucion del pipeline (${res.status})`)
    return await res.json()
  } catch {
    useMock = true
    return runMockPipeline(query, limite, forceSimulation, notificar)
  }
}

export async function fetchLeads(
  sector?: string,
  minPriority?: number,
  hasEmail?: boolean,
): Promise<EnrichedLead[]> {
  if (useMock) return getMockLeads(sector, minPriority, hasEmail)
  try {
    const params = new URLSearchParams()
    if (sector) params.append('sector', sector)
    if (minPriority) params.append('min_priority', minPriority.toString())
    if (hasEmail !== undefined) params.append('has_email', hasEmail ? 'true' : 'false')

    const url = `${API_BASE}/leads?${params.toString()}`
    const res = await fetch(url, { signal: AbortSignal.timeout(3000) })
    if (!res.ok) throw new Error('Error al listar leads')
    return await res.json()
  } catch {
    useMock = true
    return getMockLeads(sector, minPriority, hasEmail)
  }
}

export async function previewTemplate(
  sector: string,
  leadId?: string,
): Promise<TemplatePreviewResponse> {
  if (useMock) return getMockTemplatePreview(sector, leadId)
  try {
    const url = leadId
      ? `${API_BASE}/templates/${sector}/preview?lead_id=${encodeURIComponent(leadId)}`
      : `${API_BASE}/templates/${sector}/preview`
    const res = await fetch(url, { signal: AbortSignal.timeout(3000) })
    if (!res.ok) throw new Error('Error al previsualizar plantilla')
    return await res.json()
  } catch {
    useMock = true
    return getMockTemplatePreview(sector, leadId)
  }
}

export async function fetchMetrics(): Promise<Record<string, number>> {
  if (useMock) return getMockMetrics()
  try {
    const res = await fetch(`${API_BASE}/metrics`, { signal: AbortSignal.timeout(3000) })
    if (!res.ok) throw new Error('Error al recuperar metricas')
    return await res.json()
  } catch {
    useMock = true
    return getMockMetrics()
  }
}
