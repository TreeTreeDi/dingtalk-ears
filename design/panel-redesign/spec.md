# 面板重构 spec

Scope: `backend/static/{index.html,panel.css,panel.js}` only. Endpoints, payloads and data handling unchanged.

## Layout
- Top bar (sticky, hairline bottom): brand left · segmented source filter centered (全部 / 单聊 / @我 / group) · status right (`● 3 路 · Codex 已连接`, dot teal when all listeners ready, orange when degraded or summary paused).
- ≥961px: two columns inside 1120px — message list (hero) | 320px sticky rail (总结 card, 待办 card, meta lines).
- ≤960px: one column; ≤640px (menu-bar ~400px): bar wraps to brand+status / full-width segments; order is 总结 → 待处理 → 待办 → meta.

## Message card
sender (600) · source in muted text · time `MM-DD HH:mm` right (full value in tooltip) → original (15/24 ink) → Codex summary (13/20 muted) → draft textarea (fill bg, accent border + 3px ring on focus) → actions row: ghost text buttons left (重新生成 / 添加待办 / 标记已处理), accent pill right (确认发送). Non-pending draft states are one dot+text line (sending teal, unknown brown/orange, stale gray).

## Tokens
Neutral grays #f2f2f2 / #fff / #f6f6f6 / #e6e6e6 / #e4e4e4 / #232323 / #4a4a4a / #707070 / #9d9d9d; accent #0a7a6e; warm #c75b1c / #874c2a / #fff1e6. Type 12/13/14/15/20, 4px spacing grid (4–32), radius 6/8/12/pill. System font stack (PingFang SC). Body weight 400 for CJK readability, 600 for headings and the primary button.

## Motion
New cards: opacity + translateY(4px), 260ms `cubic-bezier(0.23,1,0.32,1)`, once per key. Button press scale(0.97) 140ms. Dialog: opacity + scale(0.97) 200ms; backdrop fade. Color changes 200ms ease. `prefers-reduced-motion`: all durations → 1ms, no press scale.

## States
Loading: card-shaped skeleton (list + summary). Empty: dashed card `没有待处理消息`. Error / degraded: peach strip above the list; skeleton hidden and pulsing stops on error. Buttons: hover (fill / darker accent), active (scale), focus-visible (2px accent outline, offset 2), disabled (40% or gray fill for primary), busy (`aria-busy` spinner, label hidden).

## Copy removed
Eyebrow, h1 subtitle, sidebar tagline + footer note, 4 stat-card labels, section notes, todo helper lines, 「消息整理」「待你审查」「已发送 · 投递成功」 labels. The listener caveat moved to the tooltip of the receive-count line.
