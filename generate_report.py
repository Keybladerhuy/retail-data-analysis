"""
generate_report.py
Generates output/report_sample.pdf — a professional consulting-style report.
Run from the project root: python generate_report.py

Optional env vars (can be set in .env):
  SENDGRID_API_KEY        — enables PDF delivery by email
  REPORT_RECIPIENT_EMAIL  — who receives the report
  REPORT_SENDER_EMAIL     — verified sender address in SendGrid
  GOOGLE_SHEETS_KEY_PATH  — service account JSON for live data
  GOOGLE_SHEETS_TEMPLATE_ID — spreadsheet ID to load from
"""
import os, warnings, logging
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as fm
from datetime import date

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT   = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(ROOT, 'output', 'charts')
OUT    = os.path.join(ROOT, 'output', 'report_sample.pdf')

# ── Japanese font detection ───────────────────────────────────────────────────
def find_jp_font():
    candidates = ['Yu Gothic', 'Meiryo', 'MS Gothic', 'MS UI Gothic',
                  'Hiragino Sans', 'Noto Sans CJK JP', 'Noto Sans JP']
    for name in candidates:
        path = fm.findfont(fm.FontProperties(family=name), fallback_to_default=False)
        if path and 'DejaVu' not in path:
            print(f'Japanese font found: {name}')
            return name
    print('Warning: no Japanese font found, falling back to default.')
    return 'sans-serif'

JP = find_jp_font()
plt.rcParams['font.family'] = JP

def fp(size=10, bold=False):
    return fm.FontProperties(family=JP, size=size,
                             weight='bold' if bold else 'normal')

# ── Design tokens ─────────────────────────────────────────────────────────────
W, H       = 8.27, 11.69   # A4 inches
PRIMARY    = '#2C7BB6'
DARK       = '#1A3A5C'
LIGHT_BG   = '#F7F9FC'
MID        = '#CCCCCC'
TEXT_COL   = '#2B2B2B'
SUB_COL    = '#666666'
TOTAL_PG   = 7

# ── Layout helpers ────────────────────────────────────────────────────────────

def new_fig():
    return plt.figure(figsize=(W, H), facecolor='white')

def add_header(fig, jp_title, en_title, page_num):
    ax = fig.add_axes([0, 0.938, 1, 0.062])
    ax.set_facecolor(PRIMARY)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.text(0.035, 0.64, jp_title, color='white', fontsize=13,
            va='center', fontproperties=fp(13, bold=True))
    ax.text(0.035, 0.19, en_title, color='#AACFE8', fontsize=8.5,
            va='center', fontproperties=fp(8.5))
    ax.text(0.965, 0.5, f'{page_num} / {TOTAL_PG}', color='white',
            fontsize=8.5, va='center', ha='right')

def add_footer(fig):
    txt = (f'本レポートは分析サービスのサンプルです　|　'
           f'作成日: {date.today().strftime("%Y年%m月%d日")}　|　'
           f'データ: UCI Online Retail II (CC BY 4.0)')
    ax = fig.add_axes([0, 0, 1, 0.032])
    ax.set_facecolor(LIGHT_BG); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.plot([0.03, 0.97], [0.88, 0.88], color=MID, linewidth=0.5)
    ax.text(0.5, 0.36, txt, color=SUB_COL, fontsize=6.5,
            ha='center', va='center', fontproperties=fp(6.5))

def load_chart(name):
    path = os.path.join(CHARTS, name)
    return mpimg.imread(path) if os.path.exists(path) else None

def section_label(fig, y, text):
    ax = fig.add_axes([0.04, y, 0.004, 0.021])
    ax.set_facecolor(PRIMARY); ax.axis('off')
    fig.text(0.053, y + 0.017, text, color=DARK, fontsize=10.5,
             va='top', fontproperties=fp(10.5, bold=True))

def bullets(fig, y_start, items, line_h=0.063):
    for i, item in enumerate(items):
        y = y_start - i * line_h
        fig.text(0.06, y, '▶', color=PRIMARY, fontsize=9.5, va='top')
        fig.text(0.082, y, item, color=TEXT_COL, fontsize=9.5, va='top',
                 linespacing=1.55, fontproperties=fp(9.5))


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — COVER
# ─────────────────────────────────────────────────────────────────────────────
def page_cover(pdf):
    fig = new_fig()

    ax_top = fig.add_axes([0, 0.77, 1, 0.23])
    ax_top.set_facecolor(DARK); ax_top.axis('off')
    ax_top.text(0.5, 0.73, 'Business Data Analysis Report',
                color='white', fontsize=22, fontweight='bold',
                ha='center', va='center')
    ax_top.text(0.5, 0.44, '業務データ分析レポート',
                color='#AACFE8', fontsize=17, ha='center', va='center',
                fontproperties=fp(17))
    ax_top.text(0.5, 0.16, 'サンプル — 小売業 売上・顧客分析',
                color='#7BAFD4', fontsize=11, ha='center', va='center',
                fontproperties=fp(11))

    ax_line = fig.add_axes([0, 0.756, 1, 0.014])
    ax_line.set_facecolor(PRIMARY); ax_line.axis('off')

    fig.text(0.5, 0.695, '分析対象', color=SUB_COL, fontsize=9,
             ha='center', fontproperties=fp(9))
    fig.text(0.5, 0.655, 'ECサイト 売上・顧客データ（2009–2011年）',
             color=TEXT_COL, fontsize=11.5, ha='center', fontweight='bold',
             fontproperties=fp(11.5, bold=True))

    fig.text(0.5, 0.595, '分析項目', color=SUB_COL, fontsize=9,
             ha='center', fontproperties=fp(9))
    for j, item in enumerate([
        '① データクレンジング・品質確認',
        '② 売上トレンド分析（月次・週次・前年比）',
        '③ 商品別パフォーマンス・パレート分析',
        '④ 顧客セグメント分析（RFM）',
    ]):
        fig.text(0.5, 0.555 - j * 0.048, item,
                 color=TEXT_COL, fontsize=10.5, ha='center',
                 fontproperties=fp(10.5))

    ax_div = fig.add_axes([0.15, 0.27, 0.70, 0.0012])
    ax_div.set_facecolor(MID); ax_div.axis('off')

    fig.text(0.5, 0.245, f'作成日: {date.today().strftime("%Y年%m月%d日")}',
             color=SUB_COL, fontsize=9, ha='center', fontproperties=fp(9))
    fig.text(0.5, 0.205, '作成者: シニアデータサイエンティスト',
             color=SUB_COL, fontsize=9, ha='center', fontproperties=fp(9))
    fig.text(0.5, 0.163, 'Coconala にてデータ分析サービスを提供中',
             color=PRIMARY, fontsize=9, ha='center', fontproperties=fp(9))

    ax_bot = fig.add_axes([0, 0, 1, 0.05])
    ax_bot.set_facecolor(DARK); ax_bot.axis('off')
    ax_bot.text(0.5, 0.5,
                '本レポートはサンプルです。実際の依頼内容に応じてカスタマイズします。',
                color='#7BAFD4', fontsize=8, ha='center', va='center',
                fontproperties=fp(8))

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 1 (Cover) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
def page_summary(pdf):
    fig = new_fig()
    add_header(fig, 'エグゼクティブサマリー', 'Executive Summary', 2)
    add_footer(fig)

    section_label(fig, 0.865, '分析の背景と目的')
    fig.text(0.06, 0.828,
             'あるECサイトが2年分の売上・顧客データを保有しているものの、データを経営判断に活かせていない状況でした。\n'
             '本分析では、売上トレンド・商品パフォーマンス・顧客行動の3つの観点から現状を整理し、\n'
             '次にとるべきアクションを提示しています。',
             color=TEXT_COL, fontsize=9.5, va='top', linespacing=1.7,
             fontproperties=fp(9.5))

    section_label(fig, 0.705, '主要な発見（3点）')
    findings = [
        ('売上は前年比で成長しているが、11月に集中する季節性が強い。\n'
         '　→ 9月中旬までに在庫・人員の準備が必要。'),
        ('上位20%の商品が売上の大半を占める（パレートの法則）。\n'
         '　→ 主力商品の欠品防止を最優先課題として管理すべき。'),
        ('優良顧客（Champions）は顧客全体の一部だが、売上への貢献度は突出して高い。\n'
         '　→ このセグメントの離脱防止策が最大のROIをもたらす。'),
    ]
    for i, text in enumerate(findings):
        y = 0.648 - i * 0.098
        ax_c = fig.add_axes([0.055, y - 0.006, 0.026, 0.026])
        circ = plt.Circle((0.5, 0.5), 0.5, color=PRIMARY)
        ax_c.add_patch(circ)
        ax_c.set_xlim(0, 1); ax_c.set_ylim(0, 1); ax_c.axis('off')
        ax_c.text(0.5, 0.5, str(i + 1), color='white', fontsize=10,
                  fontweight='bold', ha='center', va='center')
        fig.text(0.093, y, text, color=TEXT_COL, fontsize=9.5, va='top',
                 linespacing=1.65, fontproperties=fp(9.5))

    section_label(fig, 0.38, 'データ概要')
    stats = [
        ('分析期間',      '2009年12月 〜 2011年12月'),
        ('取引レコード数', '約80万件（クレンジング後）'),
        ('対象顧客数',    '約4,300名'),
        ('対象商品数',    '約3,600品目'),
        ('対象国',       '英国を中心に40カ国以上'),
    ]
    for i, (label, value) in enumerate(stats):
        y_row = 0.332 - i * 0.046
        bg = LIGHT_BG if i % 2 == 0 else 'white'
        ax_row = fig.add_axes([0.05, y_row - 0.003, 0.90, 0.042])
        ax_row.set_facecolor(bg); ax_row.axis('off')
        fig.text(0.07, y_row + 0.014, label, color=SUB_COL, fontsize=9,
                 va='center', fontproperties=fp(9))
        fig.text(0.38, y_row + 0.014, value, color=TEXT_COL, fontsize=9.5,
                 va='center', fontproperties=fp(9.5))

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 2 (Executive Summary) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — SALES TREND
# ─────────────────────────────────────────────────────────────────────────────
def page_trend(pdf):
    fig = new_fig()
    add_header(fig, '売上トレンド分析', 'Sales Trend Analysis', 3)
    add_footer(fig)

    section_label(fig, 0.875, '月別売上推移（前年比較）')
    chart = load_chart('monthly_revenue_yoy.png')
    if chart is not None:
        ax = fig.add_axes([0.04, 0.555, 0.92, 0.307])
        ax.imshow(chart); ax.axis('off')

    section_label(fig, 0.527, '分析コメント')
    bullets(fig, 0.493, [
        '11月に売上が急増する季節性が2年連続で確認される。ホリデーシーズン需要が最大の変動要因。',
        '2011年の売上は前年比で成長しており、事業の基礎的な成長トレンドは維持されている。',
        '1〜2月（Q1）は年間で最も売上が低迷する時期。割引・新商品投入などの施策検討が有効。',
    ], line_h=0.063)

    section_label(fig, 0.296, '前月比変化率（月次）')
    chart2 = load_chart('mom_revenue_change.png')
    if chart2 is not None:
        ax2 = fig.add_axes([0.04, 0.055, 0.92, 0.228])
        ax2.imshow(chart2); ax2.axis('off')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 3 (Sales Trend) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — PRODUCT PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
def page_products(pdf):
    fig = new_fig()
    add_header(fig, '商品別パフォーマンス分析', 'Product Performance Analysis', 4)
    add_footer(fig)

    section_label(fig, 0.875, 'パレート分析（売上集中度）')
    chart = load_chart('pareto_revenue.png')
    if chart is not None:
        ax = fig.add_axes([0.04, 0.565, 0.92, 0.297])
        ax.imshow(chart); ax.axis('off')

    section_label(fig, 0.536, '分析コメント')
    bullets(fig, 0.503, [
        '上位20%の商品が売上の大部分を占める「パレートの法則」が成立している。',
        '主力商品の欠品は売上全体に直接影響するため、在庫管理の最優先対象として管理すること。',
        '注文件数は多いが売上上位でない商品は、価格改定（値上げ）による利益改善の余地がある。',
    ], line_h=0.062)

    section_label(fig, 0.300, '売上上位20品目')
    chart2 = load_chart('top20_products_revenue.png')
    if chart2 is not None:
        ax2 = fig.add_axes([0.04, 0.055, 0.92, 0.232])
        ax2.imshow(chart2); ax2.axis('off')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 4 (Products) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — CUSTOMER SEGMENTATION
# ─────────────────────────────────────────────────────────────────────────────
def page_rfm(pdf):
    fig = new_fig()
    add_header(fig, '顧客セグメント分析（RFM）', 'Customer Segmentation — RFM Analysis', 5)
    add_footer(fig)

    section_label(fig, 0.875, 'セグメント別 顧客数・売上構成')
    chart_seg = load_chart('rfm_segment_distribution.png')
    chart_rev = load_chart('rfm_revenue_by_segment.png')
    if chart_seg is not None:
        ax1 = fig.add_axes([0.02, 0.608, 0.47, 0.255])
        ax1.imshow(chart_seg); ax1.axis('off')
    if chart_rev is not None:
        ax2 = fig.add_axes([0.51, 0.608, 0.47, 0.255])
        ax2.imshow(chart_rev); ax2.axis('off')

    section_label(fig, 0.578, 'セグメント別 推奨アクション')

    seg_data = [
        ('Champions',        '#2C7BB6', '最近・頻繁・高額',  'VIP特典・新商品の先行案内で関係を深める'),
        ('Loyal Customers',  '#4DAC26', '継続購入・関与高',  'ポイントプログラム・定期購入割引を提案'),
        ('At Risk',          '#FDAE61', '過去優良・最近なし', '30日以内に限定クーポンで再来店を促す'),
        ('New Customers',    '#ABDDA4', '初回・少数回購入',  '購入後7日以内のフォローメールで2回目へ'),
        ('Lost',             '#D7191C', '長期未購入',         '再獲得キャンペーン or リスト管理へ移行'),
    ]
    hdr_y = 0.536
    ax_h = fig.add_axes([0.04, hdr_y, 0.92, 0.026])
    ax_h.set_facecolor(DARK); ax_h.axis('off')
    for x, lbl in [(0.01, 'セグメント'), (0.30, '特徴'), (0.52, '推奨アクション')]:
        ax_h.text(x + 0.01, 0.5, lbl, color='white', fontsize=8.5, va='center',
                  fontproperties=fp(8.5))

    row_h = 0.074
    for i, (seg, color, feature, action) in enumerate(seg_data):
        y = hdr_y - (i + 1) * row_h
        bg = LIGHT_BG if i % 2 == 0 else 'white'
        ax_row = fig.add_axes([0.04, y, 0.92, row_h - 0.003])
        ax_row.set_facecolor(bg); ax_row.axis('off')
        ax_dot = fig.add_axes([0.042, y + row_h * 0.26, 0.010, row_h * 0.46])
        ax_dot.set_facecolor(color); ax_dot.axis('off')
        mid_y = y + row_h * 0.50
        fig.text(0.060, mid_y, seg, color=color, fontsize=8.5, va='center',
                 fontproperties=fp(8.5, bold=True))
        fig.text(0.310, mid_y, feature, color=TEXT_COL, fontsize=8.5, va='center',
                 fontproperties=fp(8.5))
        fig.text(0.525, mid_y, action, color=TEXT_COL, fontsize=8.5, va='center',
                 fontproperties=fp(8.5))

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 5 (RFM) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 — SUPPORTING ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def page_detail(pdf):
    fig = new_fig()
    add_header(fig, '補足分析', 'Supporting Analysis', 6)
    add_footer(fig)

    section_label(fig, 0.875, 'スコア別 RFMヒートマップ')
    chart_heat = load_chart('rfm_heatmap.png')
    if chart_heat is not None:
        ax = fig.add_axes([0.04, 0.636, 0.92, 0.225])
        ax.imshow(chart_heat); ax.axis('off')
    fig.text(0.06, 0.618,
             '各セグメントのR（直近性）・F（頻度）・M（金額）の平均スコアを示します。'
             'Championsはすべてのスコアが高く、Lostはすべてが低いことが確認できます。',
             color=TEXT_COL, fontsize=9.5, va='top', linespacing=1.6,
             fontproperties=fp(9.5))

    section_label(fig, 0.548, '季節性分解（トレンド・季節成分・ノイズ）')
    fig.text(0.06, 0.514,
             '売上時系列を「長期トレンド」「季節性」「残差」に分解。'
             '季節性を除いても右肩上がりのトレンドが確認でき、事業の基礎成長が示されています。',
             color=TEXT_COL, fontsize=9.5, va='top', linespacing=1.6,
             fontproperties=fp(9.5))
    chart_decomp = load_chart('seasonal_decomposition.png')
    if chart_decomp is not None:
        ax2 = fig.add_axes([0.04, 0.052, 0.92, 0.448])
        ax2.imshow(chart_decomp); ax2.axis('off')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 6 (Detail) OK')


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 — METHODOLOGY + SERVICE INFO
# ─────────────────────────────────────────────────────────────────────────────
def page_appendix(pdf):
    fig = new_fig()
    add_header(fig, '分析手法・ご依頼について', 'Methodology & Service Information', 7)
    add_footer(fig)

    section_label(fig, 0.875, '分析手法について')
    fig.text(0.06, 0.838,
             '本レポートは以下の手法・ツールを用いて作成しています。'
             '専門知識がなくても理解できるよう、結果はすべて日本語で解説しています。',
             color=TEXT_COL, fontsize=9.5, va='top', linespacing=1.7,
             fontproperties=fp(9.5))

    methods = [
        ('データクレンジング',
         'キャンセル・欠損・異常値の除去。分析に使えるデータだけを抽出します。'),
        ('トレンド分析',
         '月次・週次の集計と前年比較。季節性分解により構造的な成長トレンドを抽出します。'),
        ('パレート分析',
         '売上の集中度を可視化し、どの商品・顧客に注力すべきかを明確にします。'),
        ('RFM分析',
         '最終購入日・購入頻度・購入金額の3指標で顧客をスコアリングし、5グループに分類します。'),
    ]
    for i, (title, desc) in enumerate(methods):
        y = 0.783 - i * 0.082
        fig.text(0.06, y, f'■  {title}', color=PRIMARY, fontsize=10,
                 va='top', fontproperties=fp(10, bold=True))
        fig.text(0.06, y - 0.031, desc, color=TEXT_COL, fontsize=9.5,
                 va='top', fontproperties=fp(9.5))

    ax_div = fig.add_axes([0.05, 0.445, 0.90, 0.0012])
    ax_div.set_facecolor(MID); ax_div.axis('off')

    section_label(fig, 0.424, 'ご依頼・お問い合わせ')

    ax_box = fig.add_axes([0.05, 0.170, 0.90, 0.228])
    ax_box.set_facecolor(LIGHT_BG)
    for sp in ax_box.spines.values():
        sp.set_edgecolor(MID); sp.set_linewidth(0.6)
    ax_box.set_xlim(0, 1); ax_box.set_ylim(0, 1); ax_box.axis('off')

    lines = [
        ('現役データサイエンティストが対応します。', True, PRIMARY),
        ('', False, TEXT_COL),
        ('・  ExcelやCSVファイルを送るだけでOK', False, TEXT_COL),
        ('・  図表付き分析レポート（PDF or Excel）で納品', False, TEXT_COL),
        ('・  日本語でのわかりやすい解説つき', False, TEXT_COL),
        ('・  データの内容や目的が不明確でもご相談いただけます', False, TEXT_COL),
        ('', False, TEXT_COL),
        ('Coconalaにてサービスを提供中です。まずはお気軽にメッセージをどうぞ。', True, PRIMARY),
    ]
    for i, (line, bold, color) in enumerate(lines):
        ax_box.text(0.04, 0.92 - i * 0.113, line, color=color, fontsize=9.5,
                    va='top', fontproperties=fp(9.5, bold=bold))

    fig.text(0.5, 0.125,
             '本レポートはサンプルです。実際のご依頼内容に応じてカスタマイズした分析・レポートを作成します。',
             color=SUB_COL, fontsize=8.5, ha='center', va='top',
             fontproperties=fp(8.5))

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print('  Page 7 (Appendix) OK')


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & METRIC EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def load_report_data():
    """Load sales data via sheets_loader; returns None if no local data exists."""
    try:
        from sheets_loader import load_data
        df = load_data(
            spreadsheet_id=os.environ.get('GOOGLE_SHEETS_TEMPLATE_ID'),
            sheet_name='Sheet1',
        )
        log.info('Data loaded: %d rows', len(df))
        return df
    except FileNotFoundError as exc:
        log.warning('No data available for metric extraction: %s', exc)
        return None
    except Exception as exc:
        log.warning('Data load error: %s', exc)
        return None


def extract_metrics(df):
    """
    Return a dict with the 3 headline metrics used in the email summary.
    Falls back to descriptive placeholders if df is None.
    """
    if df is None or df.empty:
        return {
            'total_revenue':     None,
            'top_product':       'N/A (run notebooks to generate data)',
            'top_segment':       'N/A',
            'top_segment_pct':   None,
        }

    total_revenue = df['Revenue'].sum()

    product_revenue = (
        df.groupby('Description')['Revenue'].sum().sort_values(ascending=False)
    )
    top_product = product_revenue.index[0] if len(product_revenue) else 'N/A'

    # Approximate segment by recency: customers active in the last 90 days = Champions proxy
    if 'Customer ID' in df.columns:
        last_date   = df['InvoiceDate'].max()
        cutoff      = last_date - __import__('pandas').Timedelta(days=90)
        recent_rev  = df[df['InvoiceDate'] >= cutoff]['Revenue'].sum()
        top_seg_pct = (recent_rev / total_revenue * 100) if total_revenue else 0
        top_segment = 'Champions / Loyal Customers'
    else:
        top_seg_pct = None
        top_segment = 'N/A'

    return {
        'total_revenue':   total_revenue,
        'top_product':     top_product,
        'top_segment':     top_segment,
        'top_segment_pct': top_seg_pct,
    }


# ─────────────────────────────────────────────────────────────────────────────
# EMAIL DELIVERY
# ─────────────────────────────────────────────────────────────────────────────

def _build_email_body(metrics, report_date):
    rev = metrics['total_revenue']
    rev_str    = f'£{rev:,.0f}' if rev is not None else 'N/A'
    pct_str_en = f'{metrics["top_segment_pct"]:.0f}% of revenue' if metrics['top_segment_pct'] else ''
    pct_str_jp = f'売上の{metrics["top_segment_pct"]:.0f}%' if metrics['top_segment_pct'] else ''

    return (
        f'Weekly Retail Analysis Report — {report_date}\n'
        f'\n'
        f'Key Metrics:\n'
        f'  • Total Revenue:         {rev_str}\n'
        f'  • Top Product:           {metrics["top_product"]}\n'
        f'  • Top Customer Segment:  {metrics["top_segment"]}'
        + (f' ({pct_str_en})' if pct_str_en else '') +
        f'\n\nThe full report is attached as a PDF.\n'
        f'\n'
        f'---\n'
        f'\n'
        f'週次小売分析レポート — {report_date}\n'
        f'\n'
        f'主要指標：\n'
        f'  ・総売上：　　　　　{rev_str}\n'
        f'  ・売上トップ商品：　{metrics["top_product"]}\n'
        f'  ・主要顧客セグメント：{metrics["top_segment"]}'
        + (f'（{pct_str_jp}）' if pct_str_jp else '') +
        f'\n\nPDF形式のレポートを添付しております。\n'
    )


def send_report_email(pdf_path, metrics):
    """Send the PDF report by email via SendGrid. No-ops if API key is absent."""
    import base64

    api_key   = os.environ.get('SENDGRID_API_KEY', '')
    to_email  = os.environ.get('REPORT_RECIPIENT_EMAIL', '')
    from_email = os.environ.get('REPORT_SENDER_EMAIL', '')

    if not api_key:
        log.warning('SENDGRID_API_KEY not set — skipping email delivery.')
        return
    if not to_email or not from_email:
        log.warning('REPORT_RECIPIENT_EMAIL or REPORT_SENDER_EMAIL not set — skipping email.')
        return

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import (
            Mail, Attachment, FileContent, FileName, FileType, Disposition
        )
    except ImportError:
        log.warning('sendgrid package not installed — skipping email delivery.')
        return

    report_date = date.today().strftime('%Y-%m-%d')
    subject     = f'Weekly Retail Report — {report_date}'
    body        = _build_email_body(metrics, report_date)

    with open(pdf_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body,
    )
    message.attachment = Attachment(
        file_content=FileContent(encoded),
        file_name=FileName(os.path.basename(pdf_path)),
        file_type=FileType('application/pdf'),
        disposition=Disposition('attachment'),
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        log.info('Email sent → %s (status %s)', to_email, response.status_code)
    except Exception as exc:
        log.error('Email delivery failed: %s', exc)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'output'), exist_ok=True)
    print(f'Generating {OUT} ...')

    df      = load_report_data()
    metrics = extract_metrics(df)

    with PdfPages(OUT) as pdf:
        page_cover(pdf)
        page_summary(pdf)
        page_trend(pdf)
        page_products(pdf)
        page_rfm(pdf)
        page_detail(pdf)
        page_appendix(pdf)

        d = pdf.infodict()
        d['Title']   = 'Business Data Analysis Report — Sample'
        d['Author']  = 'Senior Data Scientist'
        d['Subject'] = '売上・顧客データ分析レポート（サンプル）'

    print(f'\nDone → {OUT}')

    send_report_email(OUT, metrics)
