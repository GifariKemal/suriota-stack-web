import json

html = '''<!-- QUICK STATS -->
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:48px;">
  <div style="display:flex;align-items:center;gap:8px;background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:10px 20px;border-radius:24px;"><span style="font-size:18px;">⏱</span> 3–6 Bulan</div>
  <div style="display:flex;align-items:center;gap:8px;background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:10px 20px;border-radius:24px;"><span style="font-size:18px;">🌍</span> Hybrid / Remote</div>
  <div style="display:flex;align-items:center;gap:8px;background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:10px 20px;border-radius:24px;"><span style="font-size:18px;">📅</span> Batch 3</div>
  <div style="display:flex;align-items:center;gap:8px;background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:10px 20px;border-radius:24px;"><span style="font-size:18px;">🎯</span> 4 Posisi</div>
</div>

<!-- WHY JOIN -->
<div style="text-align:center;margin-bottom:48px;">
  <span style="display:inline-block;background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:700;padding:5px 14px;border-radius:20px;margin-bottom:14px;">KENAPA SURIOTA?</span>
  <h2 style="font-size:clamp(24px,4vw,32px);font-weight:700;color:#205B69;margin:0 0 16px;line-height:1.3;">Belajar dari Proyek Nyata</h2>
  <p style="font-size:clamp(15px,2vw,17px);line-height:1.8;color:#444;max-width:640px;margin:0 auto;">Program internship kami dirancang untuk memberikan pengalaman praktis mendalam. Kamu akan menjadi bagian integral dari proyek-proyek IoT, otomasi industri, dan energi terbarukan yang berdampak langsung.</p>
</div>

<!-- POSITION CARDS -->
<div style="display:flex;flex-wrap:wrap;gap:20px;margin-bottom:48px;">
  <div style="flex:1;min-width:220px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
    <div style="font-size:36px;margin-bottom:12px;">💻</div>
    <h3 style="font-size:17px;font-weight:700;color:#205B69;margin:0 0 8px;">R&D Application Developer</h3>
    <p style="font-size:14px;color:#666;line-height:1.6;margin:0;">Mengembangkan aplikasi internal dan platform SURGE menggunakan Next.js & React.</p>
  </div>
  <div style="flex:1;min-width:220px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
    <div style="font-size:36px;margin-bottom:12px;">⚙️</div>
    <h3 style="font-size:17px;font-weight:700;color:#205B69;margin:0 0 8px;">DevOps & Deployment Engineer</h3>
    <p style="font-size:14px;color:#666;line-height:1.6;margin:0;">Mengelola infrastruktur server, CI/CD pipeline, dan deployment dengan Caprover & VPS.</p>
  </div>
  <div style="flex:1;min-width:220px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
    <div style="font-size:36px;margin-bottom:12px;">🧪</div>
    <h3 style="font-size:17px;font-weight:700;color:#205B69;margin:0 0 8px;">QA & Testing Specialist</h3>
    <p style="font-size:14px;color:#666;line-height:1.6;margin:0;">Memastikan kualitas produk melalui manual & automated testing.</p>
  </div>
  <div style="flex:1;min-width:220px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
    <div style="font-size:36px;margin-bottom:12px;">🎨</div>
    <h3 style="font-size:17px;font-weight:700;color:#205B69;margin:0 0 8px;">UI/UX Designer</h3>
    <p style="font-size:14px;color:#666;line-height:1.6;margin:0;">Merancang antarmuka produk dan design system menggunakan Figma.</p>
  </div>
</div>

<!-- SKILL STACK -->
<div style="margin-bottom:48px;">
  <div style="text-align:center;margin-bottom:24px;">
    <span style="display:inline-block;background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:700;padding:5px 14px;border-radius:20px;margin-bottom:14px;">TECH STACK</span>
    <h2 style="font-size:clamp(24px,4vw,32px);font-weight:700;color:#205B69;margin:0;line-height:1.3;">Skill yang Kami Cari</h2>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:700px;margin:0 auto;">
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">Next.js</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">React</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">Prisma ORM</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">MySQL</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">PostgreSQL</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">Git</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">Caprover</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">VPS Ubuntu</span>
    <span style="background:#EAF4EC;color:#3C7D47;font-size:14px;font-weight:600;padding:8px 16px;border-radius:20px;">Figma</span>
  </div>
</div>

<!-- REQUIREMENTS -->
<div style="display:flex;flex-wrap:wrap;gap:32px;margin-bottom:48px;">
  <div style="flex:1;min-width:280px;">
    <h3 style="font-size:20px;font-weight:700;color:#205B69;margin:0 0 16px;">📋 Kualifikasi Umum</h3>
    <ul style="list-style:none;padding:0;margin:0;font-size:15px;line-height:1.8;color:#444;">
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">✓</span> Mahasiswa tingkat akhir atau fresh graduate</li>
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">✓</span> Memiliki PC/laptop pribadi</li>
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">✓</span> Mampu bekerja remote (hybrid)</li>
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">✓</span> Bersemangat belajar hal baru</li>
      <li style="padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">✓</span> Kemampuan komunikasi & kerja tim</li>
    </ul>
  </div>
  <div style="flex:1;min-width:280px;">
    <h3 style="font-size:20px;font-weight:700;color:#205B69;margin:0 0 16px;">📎 Persyaratan Dokumen</h3>
    <ul style="list-style:none;padding:0;margin:0;font-size:15px;line-height:1.8;color:#444;">
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">1.</span> Curriculum Vitae (CV) terbaru</li>
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">2.</span> Proposal magang (jika diperlukan)</li>
      <li style="margin-bottom:8px;padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">3.</span> Surat persetujuan dari kampus</li>
      <li style="padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;font-weight:700;">4.</span> Transkrip nilai</li>
    </ul>
  </div>
</div>

<!-- BENEFIT CARDS -->
<div style="margin-bottom:48px;">
  <div style="text-align:center;margin-bottom:24px;">
    <span style="display:inline-block;background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:700;padding:5px 14px;border-radius:20px;margin-bottom:14px;">BENEFIT</span>
    <h2 style="font-size:clamp(24px,4vw,32px);font-weight:700;color:#205B69;margin:0;line-height:1.3;">Yang Akan Kamu Dapatkan</h2>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:20px;">
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">🔧</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Hands-on Experience</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Proyek nyata langsung dari industri</p>
    </div>
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">📚</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Online & Offline Courses</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Akses kursus untuk upgrade skill</p>
    </div>
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">💰</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Uang Saku + Bonus</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Bulanan & bonus per project</p>
    </div>
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">📜</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Sertifikat Magang</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Pengakuan resmi partisipasi</p>
    </div>
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">👨‍🏫</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Mentorship</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Bimbingan profesional berpengalaman</p>
    </div>
    <div style="flex:1;min-width:160px;background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:24px;text-align:center;">
      <div style="font-size:32px;margin-bottom:10px;">🤝</div>
      <h4 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 6px;">Networking</h4>
      <p style="font-size:13px;color:#666;line-height:1.5;margin:0;">Jaringan talenta & profesional</p>
    </div>
  </div>
</div>

<!-- CTA -->
<div style="background:#205B69;color:#fff;padding:clamp(32px,5vw,48px);border-radius:16px;text-align:center;">
  <h2 style="font-size:clamp(22px,4vw,30px);font-weight:700;margin:0 0 12px;line-height:1.3;">Siap untuk Berkarir di Teknologi?</h2>
  <p style="font-size:clamp(14px,2vw,16px);line-height:1.7;margin:0 auto 28px;opacity:0.9;max-width:520px;">Kirimkan CV terbaru dan dokumen persyaratan ke email kami dengan subjek yang sesuai.</p>
  <div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;margin-bottom:28px;">
    <div style="background:rgba(255,255,255,0.12);padding:14px 20px;border-radius:12px;text-align:left;min-width:200px;">
      <div style="font-size:12px;opacity:0.7;margin-bottom:4px;">Langkah 1</div>
      <div style="font-size:15px;font-weight:600;">Siapkan CV & dokumen</div>
    </div>
    <div style="background:rgba(255,255,255,0.12);padding:14px 20px;border-radius:12px;text-align:left;min-width:200px;">
      <div style="font-size:12px;opacity:0.7;margin-bottom:4px;">Langkah 2</div>
      <div style="font-size:15px;font-weight:600;">Kirim ke admin@suriota.com</div>
    </div>
    <div style="background:rgba(255,255,255,0.12);padding:14px 20px;border-radius:12px;text-align:left;min-width:200px;">
      <div style="font-size:12px;opacity:0.7;margin-bottom:4px;">Langkah 3</div>
      <div style="font-size:15px;font-weight:600;">Tunggu konfirmasi tim</div>
    </div>
  </div>
  <a href="mailto:admin@suriota.com?subject=Internship%20Batch%203%20Application" style="display:inline-block;background:#fff;color:#205B69;font-size:16px;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;box-shadow:0 4px 16px rgba(0,0,0,0.15);">Daftar Sekarang via Email</a>
</div>'''

payload = {
    "jsonrpc": "2.0",
    "id": 66,
    "method": "tools/call",
    "params": {
        "name": "elementor-mcp-update-element",
        "arguments": {
            "post_id": 1127,
            "element_id": "fc46ef1",
            "settings": {"editor": html}
        }
    }
}

with open('u6.json','w',encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print('Length:', len(html))
