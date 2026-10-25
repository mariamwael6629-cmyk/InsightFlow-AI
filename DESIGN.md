# Design — InsightFlow AI

**World: the switchboard.** InsightFlow patches many channels of customer feedback into one place. The landing page shows exactly that: a bakelite operator panel where email, reviews, surveys, social, support chat and app-store feedback each have a jack and a lamp lit by sentiment. Cords run from every jack into one mood-score meter, and a lamp flickers now and then as feedback comes in. The rest of the product sits on office-grey paper with ink rules and the same three lamp colours. The DM Serif display, italic accent words, DM Mono and glow fields are gone.

## Tokens (`insightflow-ai.html` `:root`)

| Token | Value | Role |
|---|---|---|
| `--paper` / `--paper-2` / `--white` | `#F1F2F3` / `#E5E7EA` / `#FFFFFF` | ground, wells, panels |
| `--ink` / `--ink-2` / `--ink-3` | `#15171A` / `#474C55` / `#676D77` | text levels |
| `--accent` / `--accent-lite` / `--accent-soft` | `#8A6320` / `#E6D3AE` / `#F5EDDC` | brass: labels, highlights, pricing emphasis |
| `--good` / `--warn` / `--danger` (+ `-bg`) | `#1E7A4E` / `#9A5B00` / `#BF3328` | sentiment on light surfaces |
| `--panel` / `--panel-2` | `#17191C` / `#22252A` | the switchboard |
| `--brass` | `#C9A15A` | sockets, panel labels, meter border |
| `--lamp-g` / `--lamp-a` / `--lamp-r` | `#3FD18A` / `#F5B73D` / `#FF6A55` | positive / mixed / negative lamps on dark |

### Type
**Sofia Sans Condensed** 600–800 for display and numbers, like the labels engraved on a switchboard. **Sofia Sans** 400–700 for everything else. Labels are sentence case. There's no monospace or serif.

### Shape
Radii 4px (buttons) to 10px (panels). The nav sits on a 2px ink rule.

## Components
- **Switchboard** (landing hero): channel rows (lamp, name, count, brass socket), SVG patch cords in lamp colours, and a mood meter (score, weekly change, bar, response count). It collapses to a two-column jack grid without cords on tablets.
- **Sentiment chart:** in its own white panel under the hero, with positive in green and negative in red.
- **Buttons:** primary is ink and turns brass on hover; the ghost button keeps its outline.
- **Icons:** the emoji-to-SVG swap script redraws interface emoji as line icons. Priority dots (🔴🟡🟢) are dropped, because the label next to them already names the priority.

## Motion
Cords draw in on load. A random lamp blinks every 2.2s. The "Live" lamp pulses. All of it stops under reduced motion.
