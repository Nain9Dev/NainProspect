export type IndustryType = "logistica" | "tecnologia" | "retail" | "industrial" | "alimentacion" | "otro"
export type SizeBandType = "micro" | "pequena" | "mediana" | "grande" | "desconocido"
export type ConfidenceType = "alta" | "media" | "baja"

export interface EnrichedLead {
  id: string
  nombre: string
  web?: string
  email?: string | null
  telefono?: string
  ciudad?: string
  pais: string
  categoria_origen?: string
  empleados_declarados?: number | null
  fuente: string

  industria: IndustryType
  tamano_estimado: SizeBandType
  prioridad: number
  confianza: ConfidenceType
  motivo: string
  estado: string
  created_at: string
}

export interface CostMetrics {
  input_tokens: number
  output_tokens: number
  coste_usd: number
  coste_por_lead_usd: number
  coste_100_leads_usd: number
}

export interface PipelineRunResponse {
  run_id: string
  timestamp: string
  query: string
  mode: string
  total_leads: number
  in_target_band: number
  with_email: number
  high_priority_count: number
  coste: CostMetrics
  leads: EnrichedLead[]
}

export interface TemplatePreviewResponse {
  sector: string
  description: string
  subject: string
  recipient: string
  body_html: string
  legal_footer_html: string
  full_html: string
}

export interface SystemConfigResponse {
  app_name: string
  version: string
  mode_description: string
  scraping_mode: string
  classification_mode: string
  telegram_mode: string
  email_dispatch_mode: string
  target_employee_band: string
  priority_threshold: number
  sender_company: string
  sender_optout: string
}
