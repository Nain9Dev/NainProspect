import { ref } from 'vue'

export type Locale = 'es' | 'en'

const STORAGE_KEY = 'nain_locale'
const EVENT_NAME = 'nain:locale-change'

function getInitialLocale(): Locale {
  if (typeof window === 'undefined') return 'es'
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'es' || stored === 'en') return stored
  return 'es'
}

export const currentLocale = ref<Locale>(getInitialLocale())

export function setLocale(locale: Locale) {
  if (currentLocale.value === locale) return
  currentLocale.value = locale
  if (typeof window !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, locale)
    window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: { locale } }))
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener(EVENT_NAME, (event: Event) => {
    const custom = event as CustomEvent<{ locale?: Locale }>
    const target = custom.detail?.locale
    if (target === 'es' || target === 'en') {
      currentLocale.value = target
    }
  })
}

export const translations = {
  es: {
    // Header
    gatewayBadge: 'Gateway B2B',
    lssiBadge: 'Compuerta LSSI-CE',
    subtitle: 'Sourcing de empresas B2B, enriquecimiento Haiku 4.5 y compuerta legal LSSI-CE 21',
    connectedApi: 'API Conectada (:8106)',
    autonomousMotor: 'Motor Autónomo Client-Side (0,00 €)',
    docsAndCode: 'Docs & Código',
    scraping: 'Scraping',
    ai: 'IA',

    // Pipeline control
    pipelineLauncher: 'Lanzador de Pipeline',
    pipelineDesc: 'Sourcing de empresas y clasificación IA determinista',
    searchQueryLabel: 'Consulta de Búsqueda (Google Places / Web)',
    searchQueryPlaceholder: 'Ej: empresas de logistica en Madrid',
    quickQueries: 'Consultas rápidas:',
    maxLeadsLabel: 'Límite de Leads',
    option5Leads: '5 leads (muestreo ultra rápido)',
    option10Leads: '10 leads (benchmark estándar)',
    option20Leads: '20 leads (lote completo)',
    simulatedModeLabel: 'Modo Simulación',
    simulatedModeHint: 'Usa fixtures sintéticos sin coste de API',
    runButton: 'Ejecutar Pipeline',
    runningButton: 'Ejecutando Sourcing & IA...',

    // Metrics
    metricsTitle: 'Métricas & Coste Real',
    metricsSubtitle: 'Consumo de tokens Haiku 4.5 y rendimiento de embudo',
    totalLeads: 'Total Leads',
    obtainedBatch: 'obtenidos en lote',
    targetBand: 'Banda 50-500',
    targetSize: 'tamaño objetivo',
    roleEmail: 'Email Rol',
    corporateMailbox: 'buzón corporativo',
    highPriority: 'Prioridad >= 4',
    alertableTelegram: 'alertables telegram',
    costThisRun: 'Coste esta ejecución:',
    costPerLead: 'Coste por lead:',
    cost100Leads: 'Coste 100 leads:',
    tokensProcessed: 'Tokens procesados:',

    // Compliance
    complianceHeader: 'Garantías de Cumplimiento Legal (RGPD & LSSI-CE)',
    complianceRule1Title: 'Solo direcciones de rol:',
    complianceRule1Body: 'El sistema descarta automáticamente correos con nombre de persona (ej. juan@...) para mantenerse exclusivamente en el plano de persona jurídica.',
    complianceRule2Title: 'Pie legal determinista:',
    complianceRule2Body: 'Construido en código según los requisitos del art. 21 de la LSSI-CE, nunca al azar de un modelo de IA.',
    complianceRule3Title: 'Aislamiento de datos:',
    complianceRule3Body: 'La carpeta data/ y los CSVs jamás se versionan en Git.',

    // Leads table
    searchPlaceholder: 'Buscar por nombre, ciudad o email...',
    allSectors: 'Todos los sectores',
    secLogistics: 'Logística',
    secTech: 'Tecnología',
    secRetail: 'Retail',
    secIndustrial: 'Industrial',
    secFood: 'Alimentación',
    secOther: 'Otros',
    allPriorities: 'Todas las prioridades',
    prioMaxOnly: 'Solo P5 (Máxima)',
    prioHighOnly: 'P >= 4 (Prioritarios)',
    filterEmailOnly: 'Solo con email',
    thPriority: 'Prioridad',
    thCompany: 'Empresa',
    thIndustry: 'Industria',
    thSize: 'Tamaño Estimado',
    thConfidence: 'Confianza',
    thRoleEmail: 'Email Corporativo (Rol)',
    thAction: 'Acción',
    loadingLeads: 'Clasificando leads con IA...',
    noLeadsMatch: 'No se encontraron empresas con los criterios seleccionados.',
    noRoleMailbox: 'Sin buzón rol',
    btnViewEmail: 'Ver Email',
    empAbbr: 'emp.',

    // Modal
    modalTitle: 'Previsualización de Outreach',
    modalBannerTitle: 'Compuerta Legal LSSI-CE Art. 21 Activa: Envío Real Bloqueado',
    modalBannerDesc: 'El sistema detiene el pipeline en previsualización determinista. No se envía ningún correo automáticamente para garantizar el estricto cumplimiento del RGPD (interés legítimo 6.1.f) y LSSI-CE 21.',
    recipientLabel: 'Para:',
    subjectLabel: 'Asunto:',
    adBadge: 'PUBLICIDAD',
    btnCopyHtml: 'Copiar Código HTML',
    btnCopied: 'Copiado al portapapeles',
    btnClose: 'Cerrar',
  },
  en: {
    // Header
    gatewayBadge: 'B2B Gateway',
    lssiBadge: 'LSSI-CE Gate',
    subtitle: 'B2B company sourcing, Haiku 4.5 enrichment, and legal LSSI-CE 21 safety gate',
    connectedApi: 'API Connected (:8106)',
    autonomousMotor: 'Autonomous Client-Side Engine ($0.00)',
    docsAndCode: 'Docs & Code',
    scraping: 'Scraping',
    ai: 'AI',

    // Pipeline control
    pipelineLauncher: 'Pipeline Launcher',
    pipelineDesc: 'Company sourcing and deterministic AI classification',
    searchQueryLabel: 'Search Query (Google Places / Web)',
    searchQueryPlaceholder: 'e.g., logistics companies in Madrid',
    quickQueries: 'Quick queries:',
    maxLeadsLabel: 'Lead Limit',
    option5Leads: '5 leads (ultra fast sample)',
    option10Leads: '10 leads (standard benchmark)',
    option20Leads: '20 leads (full batch)',
    simulatedModeLabel: 'Simulation Mode',
    simulatedModeHint: 'Uses synthetic fixtures with $0.00 API cost',
    runButton: 'Execute Pipeline',
    runningButton: 'Running Sourcing & AI...',

    // Metrics
    metricsTitle: 'Metrics & Real Cost',
    metricsSubtitle: 'Haiku 4.5 token consumption and funnel efficiency',
    totalLeads: 'Total Leads',
    obtainedBatch: 'batch generated',
    targetBand: 'Band 50-500',
    targetSize: 'target headcount',
    roleEmail: 'Role Email',
    corporateMailbox: 'corporate mailbox',
    highPriority: 'Priority >= 4',
    alertableTelegram: 'telegram alertable',
    costThisRun: 'Cost this run:',
    costPerLead: 'Cost per lead:',
    cost100Leads: 'Cost per 100 leads:',
    tokensProcessed: 'Processed tokens:',

    // Compliance
    complianceHeader: 'Legal Compliance Guarantees (GDPR & LSSI-CE)',
    complianceRule1Title: 'Role addresses only:',
    complianceRule1Body: 'The system automatically discards person-name mailboxes (e.g. john@...) to operate strictly within legal entities.',
    complianceRule2Title: 'Deterministic legal footer:',
    complianceRule2Body: 'Built directly in code per Article 21 of LSSI-CE, never left to LLM stochastic hallucination.',
    complianceRule3Title: 'Data isolation:',
    complianceRule3Body: 'The data/ folder and raw CSV files are never committed to version control.',

    // Leads table
    searchPlaceholder: 'Search by name, city, or email...',
    allSectors: 'All sectors',
    secLogistics: 'Logistics',
    secTech: 'Technology',
    secRetail: 'Retail',
    secIndustrial: 'Industrial',
    secFood: 'Food & Beverage',
    secOther: 'Other',
    allPriorities: 'All priorities',
    prioMaxOnly: 'P5 only (Maximum)',
    prioHighOnly: 'P >= 4 (Priority)',
    filterEmailOnly: 'Only with email',
    thPriority: 'Priority',
    thCompany: 'Company',
    thIndustry: 'Industry',
    thSize: 'Estimated Size',
    thConfidence: 'Confidence',
    thRoleEmail: 'Corporate Email (Role)',
    thAction: 'Action',
    loadingLeads: 'Classifying leads with AI...',
    noLeadsMatch: 'No companies match the selected criteria.',
    noRoleMailbox: 'No role mailbox',
    btnViewEmail: 'View Email',
    empAbbr: 'emp.',

    // Modal
    modalTitle: 'Outreach Preview',
    modalBannerTitle: 'LSSI-CE Art. 21 Legal Gate Active: Real Sending Blocked',
    modalBannerDesc: 'The system halts the pipeline at deterministic preview. No emails are ever dispatched automatically, ensuring strict adherence to GDPR (legitimate interest 6.1.f) and Spanish LSSI-CE 21.',
    recipientLabel: 'To:',
    subjectLabel: 'Subject:',
    adBadge: 'ADVERTISEMENT',
    btnCopyHtml: 'Copy HTML Code',
    btnCopied: 'Copied to clipboard',
    btnClose: 'Close',
  },
} as const

export type TranslationKey = keyof typeof translations.es

export function t(key: TranslationKey): string {
  const loc = currentLocale.value
  return translations[loc][key] ?? translations.es[key] ?? key
}
