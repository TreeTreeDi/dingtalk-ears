# Panel v2 spec (Kargul style)

**Shell.** Gray page #EFEFEF, one white app panel (12px radius, 1px #DBDBDB hairline, max 1280px). Sticky top bar: brand left, status pill right (gray pulsing dot while starting, teal tint when live, peach when degraded). Below: main list + fixed 320px right rail split by a hairline; the rail is sticky and scrolls on its own.

**Type.** Geist (installed font; CSP blocks shipping files) → -apple-system / PingFang SC / Noto Sans CJK. Weights 500 body, 700 headings. Scale 24 (h1, -0.48 tracking) / 18 (h2) / 14 body / 13 / 12 meta. Times use Geist Mono.

**Color.** Ink #232323, body #707070, muted #9D9D9D (separators, placeholders, disabled), done #A3A3A3. Teal #0A7A6E only for live. Brown #874C2A + peach #FFE7D2 only for needs-Shane.

**List head.** h1 待处理, inline count "N 待审" (brown when N>0), segmented control right-aligned on the title baseline (active = dark pill). At ≤640px the control goes full width under the title.

**Rows.** Two-column grid: 88px mono time axis + content (max 720). Name 700 + sources as inline text joined by ' · '. Rows that need Shane get an orange dot hanging left of the name, so names stay aligned. Codex output sits in a tinted 12px block: summary, white textarea, state label, actions. Ghost actions align with the summary text; the single dark pill (确认发送 / 生成草稿) sits right.

**States.** Draft labels: none = dashed dot, sending = teal pulse, unknown = brown, stale = gray. Buttons: ghost hover = #F2F2F2 fill, active = scale 0.97, focus-visible = 2px ink outline offset 2, disabled = 40% opacity (primary: gray fill), busy = aria-busy opacity pulse. Empty = one quiet line in the content column. Error = peach strip under the title; skeleton freezes.

**Rail.** 总结 (refresh icon button, summary, meta line), 待办 (inline count, rows; done = gray + green check, unknown = brown, creating = teal), 实时接收 (two-column key-value: 单聊 / @我 / groups → "N 条", 更新 → HH:MM:SS mono; listener caveat in tooltip).

**Archive.** "已处理 N" disclosure with rotating chevron; handled rows in gray.

**Motion.** 300ms cubic-bezier(0.76,0,0.24,1) on color/opacity/transform only; row enter fade+4px rise; dialog scale 0.97→1. prefers-reduced-motion: 1ms, no press scale.

**Responsive.** ≤900px: single column, order bar / 总结 / list / 待办 / 实时接收. ≤640px: 16px padding, time moves right of the name.
