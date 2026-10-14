import type {
  SystemConfigResponse,
  PipelineRunResponse,
  EnrichedLead,
  TemplatePreviewResponse,
} from '../types/contracts'

const API_BASE = '/api'

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch('/health')
    if (!res.ok) return false
    const data = await res.json()
    return data.status === 'healthy'
  } catch {
    return false
  }
}

export async function fetchConfig(): Promise<SystemConfigResponse> {
  const res = await fetch(`${API_BASE}/config`)
  if (!res.ok) throw new Error('Error al consultar configuracion del sistema')
  return res.json()
}

export async function runPipeline(
  query: string,
  limite: number = 10,
  forceSimulation: boolean = true,
  notificar: boolean = false,
): Promise<PipelineRunResponse> {
  const res = await fetch(`${API_BASE}/pipeline/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      limite,
      force_simulation: forceSimulation,
      notificar,
    }),
  })
  if (!res.ok) throw new Error(`Fallo en la ejecucion del pipeline (${res.status})`)
  return res.json()
}

export async function fetchLeads(
  sector?: string,
  minPriority?: number,
  hasEmail?: boolean,
): Promise<EnrichedLead[]> {
  const params = new URLSearchParams()
  if (sector) params.append('sector', sector)
  if (minPriority) params.append('min_priority', minPriority.toString())
  if (hasEmail !== undefined) params.append('has_email', hasEmail ? 'true' : 'false')

  const url = `${API_BASE}/leads?${params.toString()}`
  const res = await fetch(url)
  if (!res.ok) throw new Error('Error al listar leads')
  return res.json()
}

export async function previewTemplate(
  sector: string,
  leadId?: string,
): Promise<TemplatePreviewResponse> {
  const url = leadId
    ? `${API_BASE}/templates/${sector}/preview?lead_id=${encodeURIComponent(leadId)}`
    : `${API_BASE}/templates/${sector}/preview`
  const res = await fetch(url)
  if (!res.ok) throw new Error('Error al previsualizar plantilla')
  return res.json()
}

export async function fetchMetrics(): Promise<Record<string, number>> {
  const res = await fetch(`${API_BASE}/metrics`)
  if (!res.ok) throw new Error('Error al recuperar metricas')
  return res.json()
}
