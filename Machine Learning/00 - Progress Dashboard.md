---
tags: [ml, dashboard]
---
# Progress Dashboard

> [!info] Setup (one time)
> 1. *Settings → Community plugins → Browse* → install **Dataview** → enable.
> 2. In Dataview's settings, turn on **Enable JavaScript queries**.
> 3. Track a note by editing its properties at the top: `status` (`not-started` → `reading` → `done`), `notebook` (`not-started` → `in-progress` → `done`), `level` (`E` explain · `D` derive · `I` implement · `C` critique – see [[Masters Self-Assessment]]) and `reviewed` (the date you last reviewed it, e.g. `2026-10-03`).
> 4. Write one line a day in your [[Today I Learned|TIL note]] (command palette → *Daily notes: Open today's daily note*).

## Overall
```dataviewjs
const tracked = dv.pages('"Machine Learning"').where(p => ["not-started", "reading", "done"].includes(p.status));
const bar = (d, t, w = 20) => { const r = t ? d / t : 0, f = Math.round(r * w); return "█".repeat(f) + "░".repeat(w - f) + `  ${d}/${t} (${Math.round(r * 100)}%)`; };
const nbs = tracked.where(p => p.notebook);
const count = (arr, key, val) => arr.where(p => p[key] === val).length;
const rows = [
  ["Notes read", bar(count(tracked, "status", "done"), tracked.length)],
  ["Notes in progress", String(count(tracked, "status", "reading"))],
  ["Notebooks finished", bar(count(nbs, "notebook", "done"), nbs.length)],
  ["Self-assessed topics", bar(tracked.where(p => p.level).length, tracked.length)],
];
dv.table(["", "Progress"], rows.map(([a, b]) => [a, "`" + b + "`"]));
```

## By section
```dataviewjs
const tracked = dv.pages('"Machine Learning"').where(p => ["not-started", "reading", "done"].includes(p.status));
const bar = (d, t, w = 12) => { const r = t ? d / t : 0, f = Math.round(r * w); return "`" + "█".repeat(f) + "░".repeat(w - f) + "`"; };
const groups = {};
for (const p of tracked) {
  const sec = p.file.folder.replace(/^Machine Learning\//, "");
  (groups[sec] = groups[sec] || []).push(p);
}
const rows = Object.keys(groups).sort().map(sec => {
  const g = groups[sec], done = g.filter(p => p.status === "done").length;
  const nb = g.filter(p => p.notebook), nbDone = nb.filter(p => p.notebook === "done").length;
  return [sec, `${bar(done, g.length)} ${done}/${g.length}`, nb.length ? `${nbDone}/${nb.length}` : "–"];
});
dv.table(["Section", "Notes read", "Notebooks"], rows);
```

## Up next
```dataviewjs
const next = dv.pages('"Machine Learning"').where(p => p.status === "not-started").sort(p => p.file.path).limit(5);
dv.paragraph(next.length ? "Following the folder order of the learning path:" : "Everything started – impressive!");
dv.list(next.map(p => p.file.link));
```

## Currently reading
```dataview
LIST FROM "Machine Learning" WHERE status = "reading" SORT file.name ASC
```

## Notebooks waiting
Notes you have read whose exercise notebook isn't finished yet:
```dataview
LIST notebook FROM "Machine Learning" WHERE status = "done" AND notebook AND notebook != "done" SORT file.path ASC
```

## Review queue
Read notes not reviewed in the last 30 days (spaced repetition keeps them fresh):
```dataview
TABLE reviewed AS "Last reviewed", level AS "Level"
FROM "Machine Learning"
WHERE status = "done" AND (!reviewed OR reviewed <= date(today) - dur(30 days))
SORT reviewed ASC
```

## Self-assessment
```dataviewjs
const order = { C: 4, I: 3, D: 2, E: 1 }, names = { E: "Explain", D: "Derive", I: "Implement", C: "Critique" };
const lv = dv.pages('"Machine Learning"').where(p => ["not-started", "reading", "done"].includes(p.status) && p.level && order[String(p.level).toUpperCase()]);
const counts = ["E", "D", "I", "C"].map(k => `${names[k]}: **${lv.where(p => String(p.level).toUpperCase() === k).length}**`);
dv.paragraph(counts.join(" · "));
dv.table(["Topic", "Level", "Status"], lv.sort(p => -order[String(p.level).toUpperCase()]).map(p => [p.file.link, `${String(p.level).toUpperCase()} – ${names[String(p.level).toUpperCase()]}`, p.status]));
```

## Leaderboard
Current best per task in the [[Leaderboard]]:
```dataviewjs
const text = await dv.io.load("Machine Learning/20-Play/Leaderboard.md");
const rows = [];
for (const sec of text.split(/^## /m).filter(s => s.startsWith("Task"))) {
  const dir = sec.match(/\((higher|lower) is better\)/), hi = !dir || dir[1] === "higher";
  const entries = sec.split("\n").map(l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()))
    .filter(c => c.length >= 3 && /^\d{4}-\d{2}-\d{2}$/.test(c[0]) && !isNaN(parseFloat(c[1])));
  if (!entries.length) continue;
  const base = entries.find(c => /^baseline/i.test(c[2])) || entries[0];
  const best = entries.reduce((a, c) => (hi ? +c[1] > +a[1] : +c[1] < +a[1]) ? c : a);
  const beaten = best !== base;
  rows.push([sec.split("\n")[0].replace(/^Task \d+ · /, ""), `**${best[1]}**`, base[1], beaten ? "🏆 " + best[2] : "not beaten yet", entries.length - 1]);
}
dv.table(["Task", "Best", "Baseline", "Best method", "Attempts"], rows);
```

## Today I Learned
```dataviewjs
const tils = dv.pages('"Journal/TIL"').where(p => p.file.day && p.til && String(p.til).trim());
const days = new Set(tils.map(p => p.file.day.toISODate()).array());
let streak = 0, d = dv.date("today");
if (!days.has(d.toISODate())) d = d.minus({ days: 1 });
while (days.has(d.toISODate())) { streak++; d = d.minus({ days: 1 }); }
const topics = {};
for (const p of tils) for (const t of [].concat(p.topic || [])) { const k = t && t.path ? t.path.split("/").pop().replace(/\.md$/, "") : String(t); topics[k] = (topics[k] || 0) + 1; }
const top = Object.entries(topics).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => `${k} (${v})`).join(", ");
dv.paragraph(`🔥 Streak: **${streak}** day${streak === 1 ? "" : "s"} · 📚 Things learned so far: **${tils.length}**${top ? ` · Most learned: ${top}` : ""}`);
```
```dataview
TABLE WITHOUT ID file.link AS "Day", til AS "Today I learned", topic AS "Topic"
FROM "Journal/TIL"
WHERE til
SORT file.name DESC
LIMIT 14
```

> [!quote] Remember
> Every row in this dashboard is evidence. When imposter syndrome says "you know nothing", scroll up. See [[Imposter Syndrome]].
