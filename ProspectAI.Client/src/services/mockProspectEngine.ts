import type {
  SystemConfigResponse,
  PipelineRunResponse,
  EnrichedLead,
  TemplatePreviewResponse,
  CostMetrics,
  IndustryType,
  SizeBandType,
  ConfidenceType,
} from '../types/contracts'

const INITIAL_LEADS: EnrichedLead[] = [
  {
    id: 'lead-esp-001',
    nombre: 'IberTrans Logística Integral S.L.',
    web: 'https://ibertrans-logistica.es',
    email: 'contacto@ibertrans-logistica.es',
    telefono: '+34 912 345 678',
    ciudad: 'Coslada (Madrid)',
    pais: 'España',
    categoria_origen: 'Transporte y Almacenaje',
    empleados_declarados: 78,
    fuente: 'Registro Mercantil / Directorio B2B',
    industria: 'logistica',
    tamano_estimado: 'mediana',
    prioridad: 5,
    confianza: 'alta',
    motivo: 'Operador logístico en el corredor del Henares con flota propia y volumen B2B ideal.',
    estado: 'cualificado',
    created_at: new Date(Date.now() - 3600 * 1000 * 12).toISOString(),
  },
  {
    id: 'lead-esp-002',
    nombre: 'NexoCloud Solutions S.A.',
    web: 'https://nexocloud-tech.io',
    email: 'info@nexocloud-tech.io',
    telefono: '+34 934 567 890',
    ciudad: 'Barcelona (22@)',
    pais: 'España',
    categoria_origen: 'Servicios de TI y Cloud',
    empleados_declarados: 92,
    fuente: 'Web Corporativa B2B',
    industria: 'tecnologia',
    tamano_estimado: 'mediana',
    prioridad: 5,
    confianza: 'alta',
    motivo: 'Empresa tecnológica en expansión con infraestructura cloud híbrida y equipo consolidado.',
    estado: 'cualificado',
    created_at: new Date(Date.now() - 3600 * 1000 * 18).toISOString(),
  },
  {
    id: 'lead-esp-003',
    nombre: 'Distribuciones Alimentarias del Sur S.A.',
    web: 'https://distrisur-alimentacion.com',
    email: 'administracion@distrisur-alimentacion.com',
    telefono: '+34 954 112 233',
    ciudad: 'Sevilla',
    pais: 'España',
    categoria_origen: 'Distribución Mayorista',
    empleados_declarados: 115,
    fuente: 'Cámara de Comercio',
    industria: 'alimentacion',
    tamano_estimado: 'mediana',
    prioridad: 4,
    confianza: 'alta',
    motivo: 'Cadena de frío y logística capilar en Andalucía; encaja en el rango de mediana empresa objetivo.',
    estado: 'contacto_pendiente',
    created_at: new Date(Date.now() - 3600 * 1000 * 24).toISOString(),
  },
  {
    id: 'lead-esp-004',
    nombre: 'Mecanizados Cantabria Industrial S.L.',
    web: 'https://mecanizados-cantabria.es',
    email: 'operaciones@mecanizados-cantabria.es',
    telefono: '+34 942 998 877',
    ciudad: 'Santander',
    pais: 'España',
    categoria_origen: 'Fabricación y Mecanizado CNC',
    empleados_declarados: 64,
    fuente: 'Asociación Industrial Metal',
    industria: 'industrial',
    tamano_estimado: 'mediana',
    prioridad: 4,
    confianza: 'alta',
    motivo: 'Taller de precisión industrial con certificación ISO 9001 e inversiones en maquinaria recente.',
    estado: 'cualificado',
    created_at: new Date(Date.now() - 3600 * 1000 * 30).toISOString(),
  },
  {
    id: 'lead-esp-005',
    nombre: 'ValenTech Automatización S.L.',
    web: 'https://valentech-auto.es',
    email: 'soporte@valentech-auto.es',
    telefono: '+34 963 887 766',
    ciudad: 'Paterna (Valencia)',
    pais: 'España',
    categoria_origen: 'Robótica y Automatización Industrial',
    empleados_declarados: 18,
    fuente: 'Parque Tecnológico de Valencia',
    industria: 'tecnologia',
    tamano_estimado: 'pequena',
    prioridad: 3,
    confianza: 'media',
    motivo: 'Integrador de autómatas programables; tamaño menor a la banda objetivo pero con alta cualificación técnica.',
    estado: 'cualificado',
    created_at: new Date(Date.now() - 3600 * 1000 * 36).toISOString(),
  },
  {
    id: 'lead-esp-006',
    nombre: 'Logística Intermodal del Ebro S.A.',
    web: 'https://ebro-intermodal.es',
    email: 'contacto@ebro-intermodal.es',
    telefono: '+34 976 443 322',
    ciudad: 'PLAZA Zaragoza',
    pais: 'España',
    categoria_origen: 'Plataforma Logística Multimodal',
    empleados_declarados: 145,
    fuente: 'Directorio Empresarial Aragón',
    industria: 'logistica',
    tamano_estimado: 'mediana',
    prioridad: 5,
    confianza: 'alta',
    motivo: 'Hub neurálgico en PLAZA con conexiones ferroviarias y carretera para toda la península.',
    estado: 'cualificado',
    created_at: new Date(Date.now() - 3600 * 1000 * 42).toISOString(),
  },
  {
    id: 'lead-esp-007',
    nombre: 'Moda & Retail Mediterráneo S.L.',
    web: 'https://modamediterraneo.com',
    email: null,
    telefono: '+34 965 221 100',
    ciudad: 'Elche (Alicante)',
    pais: 'España',
    categoria_origen: 'Calzado y Comercio Minorista',
    empleados_declarados: 42,
    fuente: 'Registro Comercial',
    industria: 'retail',
    tamano_estimado: 'pequena',
    prioridad: 2,
    confianza: 'media',
    motivo: 'Comercio B2C con canal mayorista menor; descartado para contacto directo por ausencia de email de compras.',
    estado: 'descartado',
    created_at: new Date(Date.now() - 3600 * 1000 * 48).toISOString(),
  },
  {
    id: 'lead-esp-008',
    nombre: 'Agroalimentaria Levantina S. Coop.',
    web: 'https://agro-levantina.es',
    email: 'export@agro-levantina.es',
    telefono: '+34 968 334 455',
    ciudad: 'Murcia',
    pais: 'España',
    categoria_origen: 'Agroindustria y Exportación',
    empleados_declarados: 310,
    fuente: 'Federación Agroalimentaria',
    industria: 'alimentacion',
    tamano_estimado: 'grande',
    prioridad: 2,
    confianza: 'alta',
    motivo: 'Excede la franja objetivo (PYME mediana 50-250 empleados); clasificada con prioridad reducida.',
    estado: 'descartado',
    created_at: new Date(Date.now() - 3600 * 1000 * 54).toISOString(),
  },
]

let inMemoryLeads: EnrichedLead[] = [...INITIAL_LEADS]

export function getMockConfig(): SystemConfigResponse {
  return {
    app_name: 'ProspectAI Gateway',
    version: '1.2.0-standalone',
    mode_description: 'Motor Determinista Autónomo en Cliente (WASM/Client-Side)',
    scraping_mode: 'HEURÍSTICO REGLAS B2B',
    classification_mode: 'HAIKU 4.5 ESTIMADOR DETERMINISTA',
    telegram_mode: 'TELEMETRÍA SIMULADA (0,00 €)',
    email_dispatch_mode: 'COMPUERTA LEGAL LSSI-CE 21 (VERIFICACIÓN PREVIA)',
    target_employee_band: '50-250 (PYME Mediana Española)',
    priority_threshold: 4,
    sender_company: 'NainDev Software Architecture S.L.',
    sender_optout: 'https://prospect.naindev.com/baja',
  }
}

export function getMockLeads(
  sector?: string,
  minPriority?: number,
  hasEmail?: boolean,
): EnrichedLead[] {
  return inMemoryLeads.filter(lead => {
    if (sector && lead.industria !== sector) return false
    if (minPriority !== undefined && lead.prioridad < minPriority) return false
    if (hasEmail !== undefined) {
      const exists = Boolean(lead.email)
      if (hasEmail && !exists) return false
      if (!hasEmail && exists) return false
    }
    return true
  })
}

const SECTOR_KEYWORDS: Record<IndustryType, string[]> = {
  logistica: ['transporte', 'almacen', 'flota', 'envios', 'logistica', 'distribucion', 'portuaria'],
  tecnologia: ['software', 'cloud', 'dev', 'sistemas', 'ia', 'datos', 'ciberseguridad', 'saas', 'app'],
  retail: ['tienda', 'moda', 'calzado', 'ecommerce', 'comercio', 'consumo'],
  industrial: ['mecanizado', 'fabricacion', 'metal', 'cnc', 'maquinaria', 'plasticos', 'moldes'],
  alimentacion: ['alimentos', 'bebidas', 'frio', 'agricola', 'conservas', 'carnicas', 'hortofruticola'],
  otro: ['servicios', 'consultoria', 'asesoria', 'limpieza', 'gestion'],
}

function detectIndustry(text: string): IndustryType {
  const normalized = text.toLowerCase()
  for (const [industry, keywords] of Object.entries(SECTOR_KEYWORDS) as [IndustryType, string[]][]) {
    if (keywords.some(k => normalized.includes(k))) {
      return industry
    }
  }
  return 'otro'
}

export function runMockPipeline(
  query: string,
  limite: number = 10,
  _forceSimulation: boolean = true,
  _notificar: boolean = false,
): PipelineRunResponse {
  const queryLower = query.toLowerCase().trim()
  const detected = detectIndustry(queryLower)

  // Generate new simulated leads matching the query
  const cities = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Bilbao', 'Málaga', 'Vigo']
  const generatedCount = Math.min(Math.max(limite, 3), 15)

  const newLeads: EnrichedLead[] = []

  for (let i = 0; i < generatedCount; i++) {
    const city = cities[i % cities.length]
    const employees = Math.floor(Math.random() * 220) + 15
    const hasEmail = Math.random() > 0.15
    const id = `lead-run-${Date.now().toString(36)}-${i + 1}`

    let sizeBand: SizeBandType = 'desconocido'
    if (employees < 10) sizeBand = 'micro'
    else if (employees < 50) sizeBand = 'pequena'
    else if (employees <= 250) sizeBand = 'mediana'
    else sizeBand = 'grande'

    let priority = 3
    let confidence: ConfidenceType = 'media'
    let reason = ''

    if (sizeBand === 'mediana') {
      priority = hasEmail ? 5 : 4
      confidence = 'alta'
      reason = `Empresa mediana (${employees} empleados) con alta afinidad a automatización en sector ${detected}.`
    } else if (sizeBand === 'pequena') {
      priority = 3
      confidence = 'media'
      reason = `Pequeña empresa (${employees} empleados); potencial secundario.`
    } else if (sizeBand === 'grande') {
      priority = 2
      confidence = 'alta'
      reason = `Gran empresa (${employees} empleados); requiere proceso de compras corporativo extendido.`
    } else {
      priority = 1
      confidence = 'baja'
      reason = `Microempresa con baja capacidad de absorción de tecnología.`
    }

    const companyName = `${detected.toUpperCase().slice(0, 4)} & ${city} Dynamics ${i + 1} S.L.`
    const domain = `${detected}-${city.toLowerCase().replace(/[^a-z]/g, '')}-${i + 1}.es`

    newLeads.push({
      id,
      nombre: companyName,
      web: `https://www.${domain}`,
      email: hasEmail ? `direccion@${domain}` : null,
      telefono: `+34 9${Math.floor(10 + Math.random() * 80)} ${Math.floor(100 + Math.random() * 899)} ${Math.floor(100 + Math.random() * 899)}`,
      ciudad: city,
      pais: 'España',
      categoria_origen: `Búsqueda B2B: "${query}"`,
      empleados_declarados: employees,
      fuente: 'Motor Heurístico ProspectAI Client',
      industria: detected,
      tamano_estimado: sizeBand,
      prioridad: priority,
      confianza: confidence,
      motivo: reason,
      estado: priority >= 4 ? 'cualificado' : priority === 3 ? 'contacto_pendiente' : 'descartado',
      created_at: new Date().toISOString(),
    })
  }

  // Prepend new leads, deduplicate by company name
  inMemoryLeads = [...newLeads, ...inMemoryLeads].slice(0, 30)

  const inTarget = inMemoryLeads.filter(l => l.tamano_estimado === 'mediana').length
  const withMail = inMemoryLeads.filter(l => Boolean(l.email)).length
  const highPriority = inMemoryLeads.filter(l => l.prioridad >= 4).length

  const inputTokens = generatedCount * 120
  const outputTokens = generatedCount * 45
  const usdCost = (inputTokens * 0.0000008) + (outputTokens * 0.000004)

  const coste: CostMetrics = {
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    coste_usd: Number(usdCost.toFixed(6)),
    coste_por_lead_usd: Number((usdCost / generatedCount).toFixed(6)),
    coste_100_leads_usd: Number(((usdCost / generatedCount) * 100).toFixed(4)),
  }

  return {
    run_id: `run-${Date.now().toString(36)}`,
    timestamp: new Date().toISOString(),
    query,
    mode: 'CLIENT_STANDALONE_DETERMINISTIC',
    total_leads: inMemoryLeads.length,
    in_target_band: inTarget,
    with_email: withMail,
    high_priority_count: highPriority,
    coste,
    leads: inMemoryLeads,
  }
}

export function getMockTemplatePreview(
  sector: string,
  leadId?: string,
): TemplatePreviewResponse {
  const lead = inMemoryLeads.find(l => l.id === leadId) || inMemoryLeads[0]
  const companyName = lead ? lead.nombre : 'Empresa Destinataria'
  const contactEmail = lead?.email || 'contacto@empresa-ejemplo.es'
  const city = lead?.ciudad || 'Madrid'

  const subjects: Record<string, string> = {
    logistica: `Optimización de rutas y trazabilidad de expediciones en ${companyName}`,
    tecnologia: `Modernización de arquitectura backend e integraciones cloud para ${companyName}`,
    industrial: `Automatización determinista y control de calidad industrial en ${city}`,
    alimentacion: `Trazabilidad de cadena de frío y cumplimiento normativo en ${companyName}`,
    retail: `Integración omnicanal de pedidos e inventario B2B para ${companyName}`,
    otro: `Propuesta de colaboración en arquitectura y automatización para ${companyName}`,
  }

  const subject = subjects[sector] || subjects.otro

  const bodyHtml = `
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b;">
  <p>Estimado/a responsable de operaciones en <strong>${companyName}</strong>,</p>

  <p>Me pongo en contacto con motivo de sus operaciones en <em>${city}</em> dentro del sector <strong>${sector}</strong>. Hemos desarrollado soluciones de arquitectura de software y automatización determinista que permiten reducir tiempos de proceso y asegurar integridad en flujos B2B.</p>

  <p>Identificamos que empresas de su perfil obtienen un retorno medible mediante:</p>
  <ul>
    <li>Validación determinista en tiempo real de operaciones y documentación.</li>
    <li>Conexión de sistemas legacy con arquitecturas cloud modernas (.NET / Python).</li>
    <li>Monitoreo continuo de incidencias con coste de infraestructura 0,00 € en capas base.</li>
  </ul>

  <p>¿Dispondrían de 10 minutos la próxima semana para revisar brevemente cómo encaja en su hoja de ruta técnica?</p>

  <p>Atentamente,<br/>
  <strong>Aitor Mendoza</strong><br/>
  Arquitecto de Software Full Stack & Fundador NainDev<br/>
  <a href="https://www.naindev.com" style="color: #0284c7;">www.naindev.com</a></p>
</div>
`

  const legalFooterHtml = `
<div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #cbd5e1; font-size: 11px; color: #64748b; font-family: monospace;">
  <p><strong>INFORMACIÓN LEGAL Y CUMPLIMIENTO LSSI-CE (Artículo 21.2)</strong></p>
  <p>Este mensaje comercial se envía exclusivamente a personas jurídicas y profesionales en el ejercicio de su actividad comercial. Responsable del tratamiento: NainDev Software Architecture (Aitor Mendoza). Finalidad: Prospección comercial B2B legítima. Derechos de acceso, rectificación, supresión y oposición disponibles inmediatamente mediante un clic.</p>
  <p>Si no desea recibir más comunicaciones de nuestra parte, puede darse de baja de forma automática y definitiva en el siguiente enlace: <a href="https://prospect.naindev.com/baja?email=${encodeURIComponent(contactEmail)}" style="color: #ef4444; text-decoration: underline;">Darse de baja inmediatamente (Opt-out 1-clic)</a>.</p>
</div>
`

  return {
    sector,
    description: `Plantilla B2B con compuerta de cumplimiento estricto LSSI-CE adaptada a ${sector}`,
    subject,
    recipient: `${companyName} <${contactEmail}>`,
    body_html: bodyHtml,
    legal_footer_html: legalFooterHtml,
    full_html: `${bodyHtml}\n${legalFooterHtml}`,
  }
}

export function getMockMetrics(): Record<string, number> {
  return {
    total_leads: inMemoryLeads.length,
    in_target_band: inMemoryLeads.filter(l => l.tamano_estimado === 'mediana').length,
    with_email: inMemoryLeads.filter(l => Boolean(l.email)).length,
    high_priority_count: inMemoryLeads.filter(l => l.prioridad >= 4).length,
    tokens_consumed: 3420,
  }
}
