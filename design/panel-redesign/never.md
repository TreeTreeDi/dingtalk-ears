# Never list — 消息助手面板

- Never add a subtitle, eyebrow, tagline, or helper line that explains what the layout already shows.
- Never put a label in front of data the position already names (no 「消息整理」 before the summary, no 「待你审查」 above a draft box).
- Never give a card more than one filled button. 确认发送 / 生成草稿 is the only accent pill; everything else is a ghost text button.
- Never use the accent for decoration. Teal means "live" (status dot) or "the action that writes to DingTalk".
- Never use orange/peach except for something that needs Shane: degraded listener, unconfirmed delivery, request errors.
- Never use drop shadows on cards; 1px hairlines only. A shadow is allowed on the modal dialog alone.
- Never hard-code a color, radius, size or duration outside `:root` tokens.
- Never animate width, height, margin or padding; only transform and opacity, ≤300 ms, ease-out on enter.
- Never animate a card that was already on screen; the entry fade plays once per message key.
- Never ship an interactive element without hover, active, focus-visible and disabled states; async buttons also need a busy state.
- Never show a centered spinner for loading; show a skeleton in the card's shape.
- Never use badges/brackets for counts; counts ride inline in muted text (`待处理 2 待审`).
- Never change an API path, payload or data field for a visual reason.
