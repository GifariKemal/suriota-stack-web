"""Homepage final sync — comprehensive translation dictionary."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from _sync_lib import sync_page

# Homepage translation dict — exhaustive, no &amp; assumptions
HP_TRANS = {
    # Hero
    'Next Gen. Industrial Partner': 'Mitra Industri Generasi Baru',
    'OUR 5 CORE SERVICES': '5 LAYANAN INTI KAMI',

    # Service card titles (raw & since they're in HTML attributes too)
    'IoT & System Integration': 'IoT & Integrasi Sistem',
    'AI & Data Analytics': 'AI & Analitik Data',
    'Software as a Service': 'Software sebagai Layanan',
    'Automation & Renewable Energy': 'Otomasi & Energi Terbarukan',

    # Service descriptions
    'End-to-end Industrial IoT \u2014 Modbus gateway, MQTT, edge computing, SCADA, sensor-to-cloud pipelines with IEC 62443 security for manufacturing, oil & gas, and maritime operations.':
        'IoT Industri menyeluruh \u2014 gateway Modbus, MQTT, edge computing, SCADA, pipeline sensor-ke-cloud dengan keamanan IEC 62443 untuk manufaktur, oil & gas, dan operasi maritim.',
    'Predictive maintenance, OEE dashboards, computer-vision QC, and real-time operational intelligence \u2014 turning raw machine data into actionable plant-floor decisions.':
        'Predictive maintenance, dashboard OEE, computer-vision QC, dan intelligence operasional real-time \u2014 mengubah data mesin menjadi keputusan plant-floor yang actionable.',
    'SURGE multi-tenant IoT platform \u2014 Energy Mapping (kWh, power factor), Water Analytic (KLHK SPARING compliance), Vessel Tracking (fleet + fuel monitoring).':
        'Platform IoT multi-tenant SURGE \u2014 Energy Mapping (kWh, power factor), Water Analytic (compliance SPARING KLHK), Vessel Tracking (armada + monitoring bahan bakar).',
    'PLC integration, SCADA modernization, Solar PV PLTS design, hybrid PLTS-PLTB systems, and smart street light (PJU) \u2014 turnkey industrial energy transition.':
        'Integrasi PLC, modernisasi SCADA, desain Solar PV PLTS, sistem hybrid PLTS-PLTB, dan smart street light (PJU) \u2014 transisi energi industri turnkey.',
    'Industry 4.0 roadmap, OT/IT convergence assessment, IIoT readiness audit, SCADA modernization, and cloud migration strategy for Indonesian manufacturers.':
        'Roadmap Industry 4.0, assessment konvergensi OT/IT, audit kesiapan IIoT, modernisasi SCADA, dan strategi migrasi cloud untuk manufaktur Indonesia.',

    # Hero intro text (HTML embedded)
    'is a technology company specializing in <strong>Industrial IoT & System Integration</strong>, headquartered in Batam, Riau Islands. Since January 2023, we have delivered <strong>64+ industrial projects</strong>':
        'adalah perusahaan teknologi yang berfokus pada <strong>IoT Industri & Integrasi Sistem</strong>, berkantor pusat di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan <strong>64+ proyek industri</strong>',
    'from Modbus gateways to complete IoT platforms across manufacturing, energy, logistics, and maritime sectors.':
        'dari gateway Modbus hingga platform IoT lengkap untuk sektor manufaktur, energi, logistik, dan maritim.',

    # Trust line
    'With our commitment to the highest technical standards, SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability for clients across Indonesia.':
        'Dengan komitmen kami terhadap standar teknis tertinggi, SURIOTA adalah mitra terpercaya dalam meningkatkan efisiensi, produktivitas, dan keberlanjutan bisnis klien di seluruh Indonesia.',

    # Buttons
    'Free Consultation': 'Konsultasi Gratis',
    'View All Portfolio': 'Lihat Semua Portfolio',
    'SEND': 'KIRIM',

    # Section headings
    'Products': 'Produk',
    'Trusted By': 'Dipercaya Oleh',
    'Our Location': 'Lokasi Kami',
    'Contact Us': 'Hubungi Kami',
    'Capabilities': 'Kapabilitas',

    # Capabilities labels
    'Industrial Projects': 'Proyek Industri',
    'In-House Products': 'Produk In-House',
    'Core Services': 'Layanan Inti',
    'Team Professionals': 'Profesional Tim',

    # Form labels (common)
    'Name': 'Nama',
    'Email': 'Email',
    'Message': 'Pesan',
    'Phone': 'Telepon',
}

sync_page(12, 5273, HP_TRANS, page_label='Homepage', trigger_url='https://suriota.com/id/beranda/')
