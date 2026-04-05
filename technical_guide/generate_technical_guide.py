"""
Generate the BL Crop Raid Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: bl_crop_raid_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "bl_crop_raid_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "BL Crop Raid Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="BL Crop Raid Report — Technical Guide",
        author="Ecoscope",
    )
    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("BL Crop Raid Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Human-Wildlife Conflict Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>BL Crop Raid Report</b> workflow is a data-to-report pipeline "
            "built for Big Life Foundation's human-wildlife conflict (HWC) monitoring "
            "programme in the Amboseli ecosystem. It ingests crop raid events of type "
            "<code>hwc_crop_raids</code> from <b>EarthRanger</b>, transforms and "
            "classifies the event details, and produces a comprehensive suite of charts, "
            "maps, summary tables, and a print-ready Word report."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (YAML spec) "
            "and executes within the <code>ecoscope-workflows</code> runtime. "
            "Per-month crop event maps are produced via the <code>mapvalues</code> "
            "directive, grouping by <code>ts_month_name</code>."
        ),
        sp(4),
        p("The workflow delivers the following outputs per run:"),
        make_table(
            [
                ["Category",       "Outputs"],
                ["Charts",         "Time-of-day bar chart, damage size boxplot, monthly crop raid locations, crop species pie charts (count + area), monthly incidents and damage stacked bars — 7 charts total"],
                ["Maps",           "Crop raid density grid map, timing of ranger response scatter map, species responsible scatter map, per-month crop destroyed scatter maps"],
                ["Summary tables", "6 GeoParquet tables: elephant damage by month, mean elephant group size, ranger response timing, total acres damaged, species damage, crop damage"],
                ["Report",         "Word document: Big Life crop raid template populated with all charts, maps, and tables"],
                ["Dashboard",      "Metadata dashboard (run details, time range, groupers)"],
            ],
            [4*cm, 12.5*cm],
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All crop raid data is sourced from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow fetches events of type "
            "<code>hwc_crop_raids</code> using <code>get_events</code>. "
            "<code>raise_on_empty: true</code> causes the workflow to halt with an "
            "error if no events are found — distinguishing a data-availability "
            "problem from a genuine zero-incident period. "
            "<code>include_display_values: true</code> is set so that EarthRanger "
            "returns human-readable display values for choice fields."
        ),
        p(
            "The connection is also used to resolve the currently authenticated "
            "user's full name (<code>get_current_user</code> → <code>get_user_full_name</code>) "
            "for the <i>Generated by</i> field in the Word report."
        ),

        sp(4), h2("2.2 Static Geospatial Layers"),
        p(
            "Two GeoPackage files are downloaded from Dropbox at run time and "
            "reprojected to <b>EPSG:4326</b> before use. A third file "
            "(<code>amboseli_group_ranch_boundaries.gpkg</code>) is also downloaded "
            "but is not used in downstream map layers for this workflow."
        ),
        make_table(
            [
                ["File",                                                  "Used for",                        "Key column"],
                ["amboseli_ranch_conservancies_layers.gpkg",              "Land-use fill polygons on all maps","land_use (5 categories)"],
                ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg","Ranch boundaries + electric fence","land_use (Ranch boundaries, Electric Fence)"],
            ],
            [5.5*cm, 6*cm, 5*cm],
        ),

        sp(4), h2("2.3 Base Map Tile Layers"),
        make_table(
            [
                ["Layer",                  "URL (abbreviated)",                       "Opacity", "Max zoom"],
                ["ESRI World Hillshade",    "arcgisonline.com/…/World_Hillshade/…",    "1.0",     "20"],
                ["ESRI World Street Map",  "arcgisonline.com/…/World_Street_Map/…",   "0.15",    "20"],
            ],
            [4.5*cm, 7*cm, 2*cm, 2.5*cm],
        ),

        sp(4), h2("2.4 Land-use and Boundary Layer Styles"),
        p("Land-use polygons are split by <code>land_use</code> and styled as follows:"),
        make_table(
            [
                ["Category",                   "Fill / Line Colour",              "Opacity"],
                ["Rangeland",                  "RGB(163, 156, 145)  —  #a39c91", "75 %"],
                ["Rangeland and settlement",   "RGB(255, 160, 122)  —  #ffa07a", "75 %"],
                ["Settlement and agriculture", "RGB(47,  79,  79)   —  #2f4f4f", "75 %"],
                ["Conservancies",              "RGB(143, 188, 139)  —  #8fbc8b", "75 %"],
                ["National parks and reserves","RGB(77,  102,  0)   —  #4d6600", "75 %"],
            ],
            [5*cm, 6.5*cm, 4*cm],
        ),
        p("Ranch boundaries and electric fence are line layers (no fill):"),
        make_table(
            [
                ["Feature",         "Colour",                        "Width",   "Opacity"],
                ["Ranch boundaries","RGB(0, 0, 0)  —  black",        "0.95",   "55 %"],
                ["Electric Fence",  "RGB(45, 98, 177)  —  #2d62b1", "5.5 px", "100 %"],
            ],
            [4*cm, 5*cm, 2.5*cm, 5*cm],
        ),

        sp(4), h2("2.5 Grouping Strategy"),
        p(
            "The grouper is fixed to <code>ts_month_name</code> — the calendar month "
            "name derived from the event timestamp. This drives the <code>split_by_month</code> "
            "fan-out that produces one crop event map per month. "
            "It is also used as the temporal index key for the event DataFrame."
        ),
    ]

    # ── 3. Event Data Pipeline ────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Event Data Pipeline"), hr(),

        h2("3.1 Event Fetch — hwc_crop_raids"),
        p(
            "<code>get_events</code> queries EarthRanger for events of type "
            "<code>hwc_crop_raids</code>. <code>include_details: true</code> "
            "returns the full <code>event_details</code> JSON blob. "
            "<code>include_display_values: true</code> ensures choice fields "
            "are returned as human-readable labels rather than internal codes. "
            "Only events with a valid point geometry are included "
            "(<code>include_null_geometry: false</code>)."
        ),
        p("Columns retrieved per event:"),
        bullet("id, time, event_type, event_category, reported_by, serial_number, geometry, created_at, event_details"),

        sp(4), h2("3.2 Event Details Processing"),
        p(
            "<code>process_events_details</code> is called with "
            "<code>map_to_titles: true</code> and <code>ordered: true</code>. "
            "This step retrieves the EarthRanger event schema for "
            "<code>hwc_crop_raids</code> and maps each field's internal key to its "
            "display title (e.g. <code>hwc_damage_size</code> → "
            "<code>Damage size</code>). "
            "<code>ordered: true</code> preserves the field ordering as defined "
            "in the EarthRanger event form, giving consistent column ordering "
            "in all downstream DataFrames."
        ),
        note(
            "This title-mapping step is what makes downstream column references use "
            "human-readable names such as <code>'Main crop destroyed'</code>, "
            "<code>'Crop raid location'</code>, and <code>'Species responsible'</code> "
            "rather than internal field IDs."
        ),

        sp(4), h2("3.3 JSON Normalisation and Prefix Removal"),
        p(
            "<code>normalize_json_column</code> flattens the <code>event_details</code> "
            "JSON object into individual columns named "
            "<code>event_details__&lt;field_title&gt;</code>. "
            "<code>drop_column_prefix</code> then strips the "
            "<code>event_details__</code> prefix from all column names. "
            "<code>duplicate_strategy: keep_original</code> retains the original "
            "column if a name collision occurs after prefix removal."
        ),

        sp(4), h2("3.4 Column Selection and Type Conversion"),
        p(
            "<code>map_columns</code> drops columns that are not required for "
            "analysis:"
        ),
        make_table(
            [
                ["Dropped column",              "Reason"],
                ["event_category, event_type, reported_by, event_type_display", "Administrative metadata not used in analysis"],
                ["Additional information",       "Free-text field; not structured"],
                ["Area, Deterrent methods used", "Sparse / ancillary fields"],
                ["GPS Accuracy",                 "Quality flag; not used in spatial analysis"],
                ["Partners present, Sector, Teams involved", "Operational metadata"],
                ["Secondary crop destroyed, Secondary species responsible", "Consolidated into primary fields for simplicity"],
            ],
            [6*cm, 10.5*cm],
        ),
        p("Two numeric conversions follow:"),
        bullet("<b>Damage size → float</b> (<code>convert_to_float</code>, errors coerced, null filled with 0)"),
        bullet("<b>Number of animals → int</b> (<code>convert_to_int</code>, errors coerced, null filled with 0)"),

        sp(4), h2("3.5 Temporal Attribute Extraction"),
        p(
            "<code>extract_dt_attributes</code> derives three columns from the "
            "<code>Date and time of raid</code> field:"
        ),
        make_table(
            [
                ["Derived column",   "Attribute", "Example value"],
                ["ts_month",         "month",     "1 – 12 (integer)"],
                ["ts_month_name",    "month_name","January, February, …"],
                ["ts_hour",          "hour",      "0 – 23 (integer)"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),

        sp(4), h2("3.6 Time Bin Assignment"),
        p(
            "<code>assign_time_bins</code> groups the <code>ts_hour</code> integer "
            "into 3-hour bins, producing the <code>time_bin</code> column. "
            "The 8 bins cover the full 24-hour day:"
        ),
        make_table(
            [
                ["Bin label",     "Hours covered"],
                ["12:01 – 15:00","12:01 to 15:00"],
                ["15:01 – 18:00","15:01 to 18:00"],
                ["18:01 – 21:00","18:01 to 21:00"],
                ["21:01 – 00:00","21:01 to midnight"],
                ["00:00 – 03:00","Midnight to 03:00"],
                ["03:01 – 06:00","03:01 to 06:00"],
                ["06:01 – 09:00","06:01 to 09:00"],
                ["09:01 – 12:00","09:01 to 12:00"],
            ],
            [5*cm, 11.5*cm],
        ),
        p(
            "All subsequent charts and analyses operate on the enriched DataFrame "
            "produced after this step (<code>assign_custom_bins.return</code>)."
        ),
    ]

    # ── 4. Chart Outputs ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Chart Outputs"), hr(),

        h2("4.1 Time of Day Bar Chart"),
        p(
            "<code>aggregate_by</code> counts events per <code>time_bin</code>, "
            "then <code>draw_custom_bar_chart</code> renders the distribution "
            "of crop raid incidents across the 24-hour day in 3-hour segments. "
            "Bars are ordered from midday onwards (12:01 → 09:01) to keep the "
            "late-evening / nocturnal peak visually prominent. "
            "Plot background: <code>#f5f5f5</code>; legend hidden."
        ),

        sp(4), h2("4.2 Damage Size Boxplot"),
        p(
            "<code>draw_boxplot</code> shows the distribution of field-measured "
            "damage area (acres) broken down by <b>Time of ranger response</b> "
            "(Before / During / After crop raid). "
            "Only rows with <code>Measurement unit == 'Acre'</code> are included. "
            "Orientation is vertical (<code>y_column: Damage size</code>, "
            "<code>x_column: Time of ranger response</code>), "
            "individual points are hidden (<code>show_points: false</code>), "
            "and boxes are filled in <code>#7eb0d5</code> (steel blue)."
        ),
        note(
            "The boxplot deliberately excludes non-Acre measurements (e.g. plots, "
            "rows) to ensure all values are on a comparable scale. If a user logs "
            "a raid in a different unit it will be silently excluded from this chart."
        ),

        sp(4), h2("4.3 Monthly Crop Raid Locations Stacked Bar"),
        p(
            "<code>draw_custom_stacked_bar_chart</code> shows the number of crop raid "
            "incidents per month, stacked by <b>Crop raid location</b>. "
            "Month order is fixed January → December regardless of which months "
            "have data. Stack order and colours:"
        ),
        make_table(
            [
                ["Crop raid location", "Colour"],
                ["Core AOO",           "#a6cee3  (light blue)"],
                ["Non-core AOO",       "#b2df8a  (light green)"],
                ["Outside AOO",        "#fdbf6f  (peach)"],
                ["Unknown",            "#cfcfc4  (grey)"],
            ],
            [5*cm, 11.5*cm],
        ),

        sp(4), h2("4.4 Crop Species Pie Chart (Incident Count)"),
        p(
            "Filtered to <b>Core AOO</b> events where <b>Damage caused = Yes</b>. "
            "<code>aggregate_by</code> counts incidents per <code>Main crop destroyed</code>. "
            "<code>draw_pie_chart</code> renders proportion labels as percentages "
            "(<code>textinfo: percent</code>). Each of the 24 crop types has a "
            "distinct pastel colour assigned by <code>map_color_column_value</code>."
        ),

        sp(4), h2("4.5 Crop Damage Pie Chart (Area in Acres)"),
        p(
            "Same Core AOO / Damage = Yes filter as Section 4.4, further restricted "
            "to <code>Measurement unit == 'Acre'</code>. "
            "<code>aggregate_by</code> sums <code>Damage size</code> per crop species. "
            "The pie chart shows <i>proportion of total acreage destroyed</i> "
            "rather than incident count, revealing which crops suffer the "
            "greatest land-area losses even if infrequently raided."
        ),

        sp(4), h2("4.6 Monthly Incidents Stacked Bar (Core AOO, Top Crops)"),
        p(
            "Filtered to <b>Core AOO</b>. "
            "The 24 crop species are consolidated to 5 named crops plus <i>Other</i> "
            "by <code>map_column_value</code> → <code>other_crops_destroyed</code>:"
        ),
        make_table(
            [
                ["Grouped value",  "Colour",   "Crops included"],
                ["Beans",          "#cbd5e8",  "Beans"],
                ["Maize",          "#decbe4",  "Maize"],
                ["Onion",          "#fed9a6",  "Onion"],
                ["Tomatoes",       "#fcd5ce",  "Tomatoes"],
                ["Watermelon",     "#d4ede8",  "Watermelon"],
                ["Other",          "#fee8c8",  "All remaining 19 crop types + None"],
            ],
            [3*cm, 3*cm, 10.5*cm],
        ),
        p(
            "<code>draw_custom_stacked_bar_chart</code> plots monthly incident "
            "counts (y = <code>ts_month</code> count) stacked by the grouped crop. "
            "Month order fixed January → December."
        ),

        sp(4), h2("4.7 Total Damage Stacked Bar (Core AOO, Acres)"),
        p(
            "Same Core AOO filter and grouped-crop consolidation as Section 4.6, "
            "but the y-axis is <code>Damage size</code> (acres) aggregated by count "
            "— showing how much land area is affected per crop group per month. "
            "The chart uses identical colours, stack order, and month ordering "
            "as Section 4.6 so the two charts can be read side-by-side."
        ),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs — Methodology"), hr(),

        h2("5.1 Crop Raid Density Map"),
        p(
            "A grid-based density map showing where crop raid incidents cluster "
            "across the landscape."
        ),
        h3("Density grid generation"),
        p(
            "<code>generate_density_grid</code> tessellates the area with "
            "<b>2 000 m × 2 000 m</b> square cells "
            "(<code>geometry_type: point</code>) and counts how many event "
            "point geometries fall within each cell, producing a <code>density</code> "
            "column."
        ),
        h3("Custom bin classification"),
        p(
            "Raw density counts are binned by <code>bin_column</code> into "
            "5 fixed classes:"
        ),
        make_table(
            [
                ["Bin",  "Count range", "Colour",   "Hex"],
                ["1",    "1 – 3",       "Yellow",   "#FFF7BC"],
                ["2",    "4 – 6",       "Orange",   "#FD8D3C"],
                ["3",    "7 – 9",       "Dark orange","#F03B20"],
                ["4",    "10 – 12",     "Dark red",  "#BD0026"],
                ["5",    "13+",         "Darkest red","#99000D"],
            ],
            [1.5*cm, 3*cm, 3.5*cm, 8.5*cm],
        ),
        p(
            "Fixed breaks (rather than data-driven classification) are used so "
            "that density maps across different time periods remain visually "
            "comparable — a red cell always means ≥ 13 incidents regardless of "
            "when the report is run."
        ),

        sp(4), h2("5.2 Timing of Ranger Response Map"),
        p(
            "A scatter map coloured by <b>Time of ranger response</b>, showing "
            "where rangers arrived before, during, or after raids."
        ),
        make_table(
            [
                ["Response timing",  "Colour",       "Hex"],
                ["Before crop raid", "Light blue",   "#a6cee3"],
                ["During crop raid", "Red",          "#ff0000"],
                ["After crop raid",  "Golden yellow","#d5b60a"],
            ],
            [4*cm, 3.5*cm, 9*cm],
        ),
        p(
            "Before rendering, geometric outliers are removed "
            "(<code>exclude_geom_outliers</code>, Z-score threshold 3) and null "
            "geometries are dropped (<code>drop_null_geometry</code>). "
            "The scatter layer uses a fixed radius of 4 px, 75 % opacity, "
            "with a black outline (get_line_width 0.25)."
        ),

        sp(4), h2("5.3 Species Responsible Map"),
        p(
            "A scatter map coloured by <b>Species responsible</b>, showing the "
            "spatial distribution of raids by different wildlife species."
        ),
        make_table(
            [
                ["Species",  "Colour",          "Hex"],
                ["Baboon",   "Mint green",      "#b3e2cd"],
                ["Buffalo",  "Peach",           "#fdcdac"],
                ["Eland",    "Lavender",        "#cbd5e8"],
                ["Elephant", "Pink",            "#f4cae4"],
                ["Gazelle",  "Light green",     "#e6f5c9"],
                ["Giraffe",  "Light yellow",    "#fff2ae"],
                ["Impala",   "Warm cream",      "#f1e2cc"],
                ["Zebra",    "Light grey",      "#cccccc"],
                ["Unknown",  "Neutral grey",    "#cfcfc4"],
            ],
            [3.5*cm, 3.5*cm, 9.5*cm],
        ),
        p(
            "Same geometry cleaning pipeline as Section 5.2 (Z-score outlier "
            "removal + null geometry drop). Identical scatter styling: radius 4 px, "
            "opacity 75 %, black outline."
        ),

        sp(4), h2("5.4 Per-Month Crop Event Maps (mapvalues fan-out)"),
        p(
            "One interactive map is produced <i>per calendar month</i> "
            "present in the data, coloured by <b>Main crop destroyed</b>. "
            "Each of the 24 crop types has a distinct pastel colour "
            "(matching the pie chart palette in Section 4.4)."
        ),
        h3("Fan-out pipeline"),
        p(
            "<code>split_groups</code> partitions the enriched event DataFrame "
            "by <code>ts_month_name</code> (the <code>R_NAME</code>-equivalent "
            "grouper for this workflow). Each downstream task in the chain "
            "(<code>assign_overall_crop_colors</code>, "
            "<code>exclude_crop_outliers</code>, <code>remove_crop_geoms</code>, "
            "<code>generate_crop_layer</code>, <code>combine_ambo_crop_layers</code>, "
            "<code>crops_zoom_value</code>, <code>draw_crops_map</code>, "
            "<code>persist_crop_map</code>, <code>convert_crop_map_png</code>) "
            "processes one month per invocation via <code>mapvalues</code>."
        ),
        p(
            "<code>dataframe_column_first_unique_str</code> extracts the month "
            "name per split group. <code>zip_groupbykey</code> aligns the per-month "
            "HTML with the corresponding month name so each output file is "
            "suffixed correctly (e.g. <code>_January.html</code>)."
        ),
        p(
            "Map view state (<code>view_state_deck_gdf</code>) is computed "
            "per month from the cleaned events GeoDataFrame, zooming to the "
            "extent of that month's incident locations."
        ),
    ]

    # ── 6. Summary Tables ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Tables"), hr(),
        p(
            "Six summary tables are persisted as GeoParquet files. "
            "All use <code>crosstab_summary</code> or <code>aggregate_by</code> "
            "to collapse the event DataFrame into a structured tabular form "
            "suitable for insertion into the Word report."
        ),
        make_table(
            [
                ["Output file",                             "Dimensions",                                    "How computed"],
                ["total_land_size_damaged_by_elephants",    "ts_month_name × Main crop destroyed (sum of Damage size in Acres)", "crosstab on elephant-only events with Acres filter; rows ordered January → December"],
                ["average_elephant_group_size_over_time",  "ts_month_name → mean Number of animals",        "aggregate_by mean on Number of animals; converted to int; rows ordered January → December"],
                ["timing_of_ranger_response",              "Time of ranger response × Crop raid location (count) + % strings", "crosstab count; rows ordered Before → During → After; add_pct_str appends percentage in brackets"],
                ["total_area_damaged_by_crop_raid_location","Time of ranger response × Crop raid location (sum of Damage size in Acres) + % strings", "crosstab sum on Acres-filtered events; same ordering and pct string logic"],
                ["total_land_damage_by_species_responsible","Species responsible × Crop raid location (incidents + acres, merged)", "Two crosstabs (count and sum); column suffixes _incidents and _acres added before left-merge on Species responsible"],
                ["total_crops_damaged_by_species",          "Main crop destroyed × Crop raid location (incidents + acres, merged)", "Same two-crosstab merge approach as above but indexed by Main crop destroyed"],
            ],
            [5.5*cm, 5*cm, 6*cm],
        ),
        note(
            "Percentage strings are added by <code>add_pct_str</code>, which "
            "computes each row's share of the total column and appends it in "
            "parentheses (e.g. <code>12 (42.9%)</code>). The total row and "
            "index column are excluded from percentage calculation via "
            "<code>exclude_rows</code>."
        ),
    ]

    # ── 7. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Word Report"), hr(),

        h2("7.1 Template Download"),
        p(
            "The report template (<code>crop_raid_report_template.docx</code>) is "
            "downloaded automatically from Dropbox at run time "
            "(<code>fetch_and_persist_file</code>, up to 3 retries, "
            "<code>overwrite_existing: false</code>)."
        ),

        h2("7.2 Author Attribution"),
        p(
            "The currently authenticated EarthRanger user is looked up via "
            "<code>get_current_user</code> and their display name resolved by "
            "<code>get_user_full_name</code>. This name is passed as "
            "<code>generated_by</code> to <code>generate_crop_raid_report</code>, "
            "automatically attributing the report to the ranger who ran it."
        ),

        h2("7.3 Report Generation"),
        p(
            "<code>generate_crop_raid_report</code> populates the template with "
            "all chart images (PNG, captured at 2× device scale factor) and "
            "summary tables. Key parameters:"
        ),
        make_table(
            [
                ["Parameter",    "Value",                             "Description"],
                ["template_path","downloaded .docx",                 "Big Life crop raid report template"],
                ["output_dir",   "ECOSCOPE_WORKFLOWS_RESULTS",       "Output directory"],
                ["filename",     "big_life_crop_raid_report.docx",   "Output filename"],
                ["time_period",  "analysis time_range",              "Report period displayed in the header"],
                ["generated_by", "EarthRanger user full name",       "Author field in the report"],
            ],
            [3.5*cm, 5*cm, 8*cm],
        ),
        p(
            "Chart screenshots use a 5 ms tile-load wait "
            "(all charts are self-contained HTML with no external tile requests). "
            "Map screenshots use 40 000 ms to allow satellite tile layers to load "
            "fully before capture."
        ),
    ]

    # ── 8. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Output Files"), hr(),
        p("All outputs are written to <code>ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                ["File",                                         "Format",     "Content"],
                ["time_bin_bar_chart.html / .png",               "HTML / PNG", "Time of day bar chart (3-hour bins)"],
                ["damage_size_boxplot.html / .png",              "HTML / PNG", "Damage size boxplot by ranger response timing"],
                ["monthly_crop_raid_location_incidents.html / .png","HTML / PNG","Monthly incident count stacked by crop raid location"],
                ["proportion_crop_species_targeted.html / .png", "HTML / PNG", "Pie chart — crop species by incident count (Core AOO)"],
                ["proportion_land_damaged.html / .png",          "HTML / PNG", "Pie chart — crop species by total acres damaged (Core AOO)"],
                ["total_incidents_recorded.html / .png",         "HTML / PNG", "Monthly incidents stacked by grouped crop (Core AOO)"],
                ["total_damage_recorded.html / .png",            "HTML / PNG", "Monthly damage in acres stacked by grouped crop (Core AOO)"],
                ["crop_raid_incident_density_map.html / .png",   "HTML / PNG", "Density grid map of all crop raid events"],
                ["timing_of_response_event_map.html / .png",     "HTML / PNG", "Scatter map coloured by ranger response timing"],
                ["species_responsible_event_map.html / .png",    "HTML / PNG", "Scatter map coloured by species responsible"],
                ["<month>.html / .png",                          "HTML / PNG", "Per-month crop destroyed scatter map"],
                ["total_land_size_damaged_by_elephants.geoparquet","GeoParquet","Elephant damage by month × crop (acres)"],
                ["average_elephant_group_size_over_time.geoparquet","GeoParquet","Mean elephant group size per month"],
                ["timing_of_ranger_response.geoparquet",         "GeoParquet", "Ranger response timing crosstab with % strings"],
                ["total_area_damaged_by_crop_raid_location.geoparquet","GeoParquet","Acres damaged by response timing × location"],
                ["total_land_damage_by_species_responsible.geoparquet","GeoParquet","Species incidents + acres by crop raid location"],
                ["total_crops_damaged_by_species.geoparquet",    "GeoParquet", "Crop incidents + acres by crop raid location"],
                ["big_life_crop_raid_report.docx",               "Word",       "Final populated crop raid report"],
            ],
            [6.5*cm, 2.5*cm, 7.5*cm],
        ),
    ]

    # ── 9. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Skip Conditions"),
        p(
            "Every task carries two default skip conditions via "
            "<code>task-instance-defaults</code>:"
        ),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty, the task and all its dependants are skipped."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all downstream tasks that depend on it are also skipped."),
        p(
            "Map-generation tasks (<code>draw_density_map</code>, "
            "<code>draw_response_map</code>, <code>draw_species_map</code>, "
            "<code>draw_crops_map</code>) and their geometry-cleaning predecessors "
            "carry explicit <code>skipif</code> blocks with both conditions, "
            "guarding against rendering failures from empty GeoDataFrames."
        ),

        h2("9.2 mapvalues Fan-out (Per-Month Crop Maps)"),
        p(
            "<code>split_groups</code> partitions the enriched event DataFrame "
            "by the <code>ts_month_name</code> grouper. "
            "Each task in the per-month pipeline uses <code>mapvalues</code> "
            "to iterate over the resulting list, producing one output per month "
            "present in the data. <code>zip_groupbykey</code> aligns "
            "per-month map HTML with the month name string before "
            "<code>persist_text</code>, so filenames are suffixed correctly."
        ),

        h2("9.3 Screenshot Timing"),
        make_table(
            [
                ["Task group",                   "wait_for_timeout", "max_concurrent_pages", "Reason"],
                ["All chart screenshots",        "5 ms",            "1",                    "Charts are self-contained HTML; render immediately"],
                ["Density / response / species map PNGs", "40 000 ms", "1",              "External tile layers require time to load"],
                ["Per-month crop map PNGs",      "40 000 ms",       "1",                    "Same reason — tile layers"],
            ],
            [5*cm, 3*cm, 3*cm, 5.5*cm],
        ),

        h2("9.4 Core AOO Analysis Scope"),
        p(
            "Several charts and all summary tables are scoped to <b>Core AOO</b> "
            "events only (<code>filter_row_values: column='Crop raid location', "
            "values=['Core AOO']</code>). This reflects the operational focus on "
            "incidents within the core area of operation where Big Life rangers "
            "have primary responsibility."
        ),
    ]

    # ── 10. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        make_table(
            [
                ["Package",                         "Version",   "Role"],
                ["ecoscope-workflows-core",         "0.22.17.*", "Core task library and workflow engine"],
                ["ecoscope-workflows-ext-ecoscope", "0.22.17.*", "Ecoscope spatial tasks (events, density grid, maps)"],
                ["ecoscope-workflows-ext-custom",   "0.0.39.*",  "Custom utility tasks (column transforms, geometry cleaning, crosstab)"],
                ["ecoscope-workflows-ext-ste",      "0.0.17.*",  "STE tasks (time bin assignment, aggregate_by, custom stacked bar)"],
                ["ecoscope-workflows-ext-mnc",      "0.0.7.*",   "MNC domain tasks"],
                ["ecoscope-workflows-ext-mep",      "0.12.0.*",  "MEP tasks (crop raid report generation, pie and boxplot charts)"],
                ["ecoscope-workflows-ext-ate",      "0.0.2.*",   "ATE tasks (process_events_details, filter_color_map)"],
                ["ecoscope-workflows-ext-big-life",  "0.0.9.*",  "Big Life domain tasks (generate_crop_raid_report, user lookup)"],
            ],
            [5.5*cm, 2.8*cm, 8.2*cm],
        ),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
