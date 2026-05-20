"""Create ZH Home (pilot)."""
import sys
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass
from _cn_rollout import create_zh_page, health_check

# Home-specific translations
EXTRA = [
    # Hero
    ('Next Gen. Industrial Partner', '新一代工业合作伙伴'),
    # Brand attribution span text already in master via class
    # Subtitle
    ('SURIOTA</strong> is a technology company', 'SURIOTA</strong> 是专注于'),
    ('Industrial IoT &amp; System Integration</strong>', '工业物联网与系统集成</strong>'),
    (', headquartered in <a href="https:\\/\\/maps.google.com\\/maps?q=SURYA%20INOVASI%20PRIORITAS&amp;t=m&amp;z=17&amp;output=embed&amp;iwloc=near">Batam, Riau Islands</a>', '的科技公司,总部位于<a href="https:\\/\\/maps.google.com\\/maps?q=SURYA%20INOVASI%20PRIORITAS&amp;t=m&amp;z=17&amp;output=embed&amp;iwloc=near">印度尼西亚廖内群岛巴淡岛</a>'),
]

zh_id = create_zh_page(en_pid=12, zh_slug='shouye', zh_title='首页', extra_translations=EXTRA)
if zh_id:
    print(f'\n✅ ZH Home created: ID {zh_id}')
    print(f'   URL: https://suriota.com/zh/shouye/')
else:
    print('\n❌ Failed')
