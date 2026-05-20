import json

with open('current_editor.html','r',encoding='utf-8') as f:
    html = f.read()

# Clean up previous hide attempts
html = html.replace('<style>.entry-title{display:none !important;}[data-id="dd5da11"]{display:none !important;}</style><script>document.addEventListener("DOMContentLoaded",function(){var s=document.querySelector("[data-id=\'dd5da11\']");if(s)s.style.display="none";});</script>', '<style>.entry-title{display:none !important;}</style>')

old_req = '''<!-- 2-COLUMN: REQUIREMENTS + BENEFITS -->
<div style="display:flex;flex-wrap:wrap;gap:clamp(24px,3vw,40px);max-width:1100px;margin:0 auto 32px;">
  <div style="flex:1;min-width:320px;">
    <h2 style="font-size:22px;font-weight:700;color:#205B69;margin:0 0 14px;">Kualifikasi &amp; Dokumen</h2>
    <div style="display:flex;flex-wrap:wrap;gap:12px;">
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 10px;">&#128203; Kualifikasi</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:12px;line-height:1.7;color:#444;">
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Mahasiswa tingkat akhir / fresh grad</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Memiliki PC/laptop pribadi</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Bisa kerja remote (hybrid)</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Semangat belajar hal baru</li>
          <li style="padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Komunikasi &amp; kerja tim</li>
        </ul>
      </div>
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 10px;">&#128206; Dokumen</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:12px;line-height:1.7;color:#444;">
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
    <div style="display:flex;flex-wrap:wrap;gap:6px;">
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
        <div style="font-size:24px;margin-bottom:6px;">&#128101;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Mentorship</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Bimbingan pro</p>
      </div>
      <div style="flex:1;min-width:120px;background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:14px;text-align:center;">
        <div style="font-size:24px;margin-bottom:6px;">&#127757;</div>
        <h4 style="font-size:12px;font-weight:700;color:#205B69;margin:0 0 4px;">Networking</h4>
        <p style="font-size:11px;color:#666;line-height:1.4;margin:0;">Jaringan profesional</p>
      </div>
    </div>
  </div>
</div>'''

new_req = '''<!-- COLLAPSIBLE: REQUIREMENTS + BENEFITS -->
<div style="max-width:1100px;margin:0 auto 24px;">
  <details style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px 20px;margin-bottom:10px;">
    <summary style="font-size:18px;font-weight:700;color:#205B69;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">
      <span>&#128203; Kualifikasi &amp; Dokumen</span>
      <span style="font-size:12px;color:#3C7D47;background:#EAF4EC;padding:4px 10px;border-radius:12px;">Klik untuk lihat</span>
    </summary>
    <div style="display:flex;flex-wrap:wrap;gap:20px;margin-top:16px;">
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 8px;">&#128203; Kualifikasi</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:13px;line-height:1.7;color:#444;">
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Mahasiswa tingkat akhir / fresh grad</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Memiliki PC/laptop pribadi</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Bisa kerja remote (hybrid)</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Semangat belajar hal baru</li>
          <li style="padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">&#10003;</span> Komunikasi &amp; kerja tim</li>
        </ul>
      </div>
      <div style="flex:1;min-width:200px;">
        <h3 style="font-size:14px;font-weight:700;color:#205B69;margin:0 0 8px;">&#128206; Dokumen</h3>
        <ul style="list-style:none;padding:0;margin:0;font-size:13px;line-height:1.7;color:#444;">
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">1.</span> CV terbaru</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">2.</span> Proposal magang</li>
          <li style="margin-bottom:4px;padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">3.</span> Surat persetujuan kampus</li>
          <li style="padding-left:20px;position:relative;"><span style="position:absolute;left:0;color:#3C7D47;">4.</span> Transkrip nilai</li>
        </ul>
      </div>
    </div>
  </details>
  <details style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:16px 20px;">
    <summary style="font-size:18px;font-weight:700;color:#205B69;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;">
      <span>&#127942; Benefit</span>
      <span style="font-size:12px;color:#3C7D47;background:#EAF4EC;padding:4px 10px;border-radius:12px;">Klik untuk lihat</span>
    </summary>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;">
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#128295;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Hands-on</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Proyek nyata industri</p>
      </div>
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#128218;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Courses</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Akses kursus skill</p>
      </div>
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#128176;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Uang Saku</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Bulanan + per project</p>
      </div>
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#128220;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Sertifikat</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Pengakuan resmi</p>
      </div>
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#128101;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Mentorship</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Bimbingan pro</p>
      </div>
      <div style="flex:1;min-width:100px;text-align:center;padding:10px;">
        <div style="font-size:28px;margin-bottom:6px;">&#127757;</div>
        <h4 style="font-size:13px;font-weight:700;color:#205B69;margin:0 0 4px;">Networking</h4>
        <p style="font-size:12px;color:#666;line-height:1.4;margin:0;">Jaringan profesional</p>
      </div>
    </div>
  </details>
</div>'''

if old_req in html:
    html = html.replace(old_req, new_req)
    print('Replaced Requirements & Benefits with collapsible sections')
else:
    print('WARNING: Could not find old_req pattern')

# Reduce poster size
html = html.replace('width:clamp(260px,35vw,380px)', 'width:clamp(200px,28vw,300px)')

# Reduce CTA padding
html = html.replace('padding:24px 20px', 'padding:16px 20px')

payload = {
    "jsonrpc": "2.0",
    "id": 121,
    "method": "tools/call",
    "params": {
        "name": "elementor-mcp-update-element",
        "arguments": {
            "post_id": 1127,
            "element_id": "fc46ef1",
            "settings": {
                "editor": html
            }
        }
    }
}

with open('u_final.json','w',encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print('Final version created, length:', len(html))
