import json

html = '''<!-- HERO + POSTER -->
<div style="display:flex;flex-wrap:wrap;gap:clamp(24px,4vw,48px);align-items:center;max-width:1100px;margin:0 auto 32px;">
  <div style="flex:1;min-width:300px;text-align:center;">
    <span style="display:inline-block;background:#3C7D47;color:#fff;font-size:12px;font-weight:700;letter-spacing:1px;padding:5px 14px;border-radius:20px;margin-bottom:12px;">BATCH 3 &bull; NOW OPEN</span>
    <h1 style="font-size:clamp(28px,5vw,42px);font-weight:700;color:#205B69;margin:0 0 12px;line-height:1.2;">Internship Program</h1>
    <p style="font-size:clamp(14px,2vw,16px);line-height:1.6;color:#444;margin:0 0 20px;">Bergabunglah dengan tim engineer SURIOTA. Belajar langsung dari proyek industri IoT, otomasi, dan energi terbarukan.</p>
    <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:20px;">
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;">&#9201; 3&ndash;6 Bulan</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;">&#127758; Hybrid</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;">&#127919; 4 Posisi</span>
    </div>
    <a href="mailto:admin@suriota.com?subject=Internship%20Batch%203%20Application" style="display:inline-block;background:#205B69;color:#fff;font-size:15px;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none;">Daftar Sekarang</a>
  </div>
  <div style="flex:0 0 auto;text-align:center;">
    <img src="https://suriota.com/wp-content/uploads/2025/07/4.png" alt="Poster Internship Batch 3" style="width:clamp(260px,35vw,380px);height:auto;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.12);"/>
  </div>
</div>

<!-- 2-COLUMN: POSITIONS + WHY JOIN & SKILLS -->
<div style="display:flex;flex-wrap:wrap;gap:clamp(24px,3vw,40px);max-width:1100px;margin:0 auto 32px;">
  <div style="flex:1;min-width:320px;">
    <h2 style="font-size:22px;font-weight:700;color:#205B69;margin:0 0 16px;">Posisi yang Tersedia</h2>
    <div style="display:flex;flex-wrap:wrap;gap:12px;">
      <div style="flex:1;min-width:140px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <div style="font-size:28px;margin-bottom:8px;">&#128187;</div>
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 6px;">R&D App Developer</h3>
        <p style="font-size:12px;color:#666;line-height:1.5;margin:0;">Next.js, React & platform SURGE</p>
      </div>
      <div style="flex:1;min-width:140px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <div style="font-size:28px;margin-bottom:8px;">&#9881;</div>
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 6px;">DevOps Engineer</h3>
        <p style="font-size:12px;color:#666;line-height:1.5;margin:0;">Caprover, VPS & CI/CD</p>
      </div>
      <div style="flex:1;min-width:140px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <div style="font-size:28px;margin-bottom:8px;">&#129514;</div>
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 6px;">QA Specialist</h3>
        <p style="font-size:12px;color:#666;line-height:1.5;margin:0;">Manual & automated testing</p>
      </div>
      <div style="flex:1;min-width:140px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <div style="font-size:28px;margin-bottom:8px;">&#127912;</div>
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 6px;">UI/UX Designer</h3>
        <p style="font-size:12px;color:#666;line-height:1.5;margin:0;">Figma & design system</p>
      </div>
    </div>
  </div>
  <div style="flex:1;min-width:320px;">
    <h2 style="font-size:22px;font-weight:700;color:#205B69;margin:0 0 12px;">Kenapa SURIOTA?</h2>
    <p style="font-size:14px;line-height:1.7;color:#444;margin:0 0 16px;">Program internship dirancang untuk pengalaman praktis mendalam. Kamu akan menjadi bagian integral dari proyek IoT, otomasi industri, dan energi terbarukan.</p>
    <h3 style="font-size:15px;font-weight:700;color:#205B69;margin:0 0 10px;">Tech Stack</h3>
    <div style="display:flex;flex-wrap:wrap;gap:6px;">
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Next.js</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">React</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Prisma</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">MySQL</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">PostgreSQL</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Git</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Caprover</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Ubuntu VPS</span>
      <span style="background:#EAF4EC;color:#3C7D47;font-size:12px;font-weight:600;padding:5px 12px;border-radius:16px;">Figma</span>
    </div>
  </div>
</div>

<!-- 2-COLUMN: REQUIREMENTS + BENEFITS -->
<div style="display:flex;flex-wrap:wrap;gap:clamp(24px,3vw,40px);max-width:1100px;margin:0 auto 32px;">
  <div style="flex:1;min-width:320px;">
    <h2 style="font-size:22px;font-weight:700;color:#205B69;margin:0 0 14px;">Kualifikasi &amp; Dokumen</h2>
    <div style="display:flex;flex-wrap:wrap;gap:16px;">
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 10px;">&#128203; Kualifikasi</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:13px;line-height:1.7;color:#444;">
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Mahasiswa tingkat akhir / fresh grad</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Memiliki PC/laptop pribadi</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Bisa kerja remote (hybrid)</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Semangat belajar hal baru</li>
          <li style="padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Komunikasi &amp; kerja tim</li>
        </ul>
      </div>
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 10px;">&#128206; Dokumen</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:13px;line-height:1.7;color:#444;">
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">1.</span> CV terbaru</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">2.</span> Proposal magang</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">3.</span> Surat persetujuan kampus</li>
          <li style="padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">4.</span> Transkrip nilai</li>
        </ul>
      </div>
    </div>
  </div>
  <div style="flex:1;min-width:320px;">
    <h2 style="font-size:22px;font-weight:700;color:#205B69;margin:0 0 14px;">Benefit</h2>
    <div style="display:flex;flex-wrap:wrap;gap:10px;">
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#128295;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Hands-on</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Proyek nyata industri</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#128218;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Courses</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Akses kursus skill</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#128176;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Uang Saku</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Bulanan + per project</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#128220;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Sertifikat</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Pengakuan resmi</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#128107;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Mentorship</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Bimbingan pro</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#129309;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Networking</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Jaringan profesional</p>
      </div>
    </div>
  </div>
</div>

<!-- COMPACT CTA -->
<div style="background:#205B69;color:#fff;padding:clamp(24px,4vw,36px);border-radius:12px;text-align:center;max-width:1100px;margin:0 auto;">
  <h2 style="font-size:clamp(18px,3vw,26px);font-weight:700;margin:0 0 8px;line-height:1.3;">Siap Berkarir di Teknologi?</h2>
  <p style="font-size:clamp(13px,1.5vw,15px);line-height:1.6;margin:0 auto 20px;opacity:0.9;max-width:480px;">Kirim CV &amp; dokumen ke <strong>admin@suriota.com</strong> dengan subjek: <em>[Nama] &ndash; Internship Batch 3</em></p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:20px;">
    <div style="background:rgba(255,255,255,0.12);padding:10px 16px;border-radius:8px;font-size:13px;"><strong>1.</strong> Siapkan CV &amp; dokumen</div>
    <div style="background:rgba(255,255,255,0.12);padding:10px 16px;border-radius:8px;font-size:13px;"><strong>2.</strong> Kirim ke admin@suriota.com</div>
    <div style="background:rgba(255,255,255,0.12);padding:10px 16px;border-radius:8px;font-size:13px;"><strong>3.</strong> Tunggu konfirmasi</div>
  </div>
  <a href="mailto:admin@suriota.com?subject=Internship%20Batch%203%20Application" style="display:inline-block;background:#fff;color:#205B69;font-size:15px;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none;">Daftar Sekarang via Email</a>
</div>'''

payload = {
    "jsonrpc": "2.0",
    "id": 70,
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

with open('u_compact.json','w',encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print('Compact HTML length:', len(html))
