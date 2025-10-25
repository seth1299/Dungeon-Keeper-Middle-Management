# Dungeon Keeper: Middle Management — Solo HTML Edition (GDD)

**Revision:** v0.9 (Solo Edition)  
**Audience:** Single-player, browser (desktop/mobile) or packaged desktop app
**Session Length:** 10–25 minutes per raid cycle  
**Pillars:**  
1) **Plan smart** (resource tradeoffs, room synergies)  
2) **Resolve fast** (one-roll skirmishes, tight tables)  
3) **Grow notorious** (Threat & Reputation feedback)  
4) **Protect the phylactery** (clear loss state with upgrades)

---

## Quick start & runtime options

### Browser (classic static files)
1. Serve the repo with any static web server (e.g., `python -m http.server 8000`).
2. Visit `http://localhost:8000/index.html` in your browser.

### Desktop applet (Python + PyInstaller)
1. Install dependencies: `pip install -r requirements.txt`.
2. Launch the desktop build for local play: `python app.py`.
3. Package a single-file executable:
   - macOS/Linux: `pyinstaller --onefile --windowed --add-data "index.html:." --add-data "styles.css:." --add-data "data:data" app.py`
   - Windows (use `;` instead of `:`): `pyinstaller --onefile --windowed --add-data "index.html;." --add-data "styles.css;." --add-data "data;data" app.py`

The packaged build embeds the `/data` directory, so JSON overrides load without any CORS hassles. Browser mode still works for lightweight hosting or sharing the raw HTML.

---

## 1. High-level vision

You play the undead “middle manager” running a compact dungeon for a sinister corporation, balancing EU budgets, trap investments, and minion staffing against increasingly bold heroes, with a light, humorous corporate-parody tone.

---

## 2. Core game loop

[Planning Phase]
• Income & upkeep
• Buy/repair/salvage; assign traps/minions; secure phylactery
• Optional project (research/upgrade)

→ [Fighting Heroes]
• Generate party (from Threat)
• For each room on path:
Trap Step → Skirmish Step → Room Outcome

→ [Raid Resolution]
• Loot, payouts & penalties; adjust Threat and Reputation
• Repairs, salvage, and reporting

→ back to Planning


The original prep → incursion → aftermath cadence is preserved but made fully procedural for solo play.

---

## 3. World & resources

### 3.1 Currency — EU (Evil Units)
- **EU** is the universal currency for purchases, upgrades, services, and bribes.
- Sources include **base budgets**, **performance bonuses**, **loot**, and **salvage** (partial refund on retired assets).

### 3.2 Threat & Reputation
- **Threat** indicates dungeon heat and drives **funding** and **party difficulty/composition**.
- **Reputation** tracks notoriety and influences **events** and **who shows up**.

### 3.3 Dungeon map & rooms
- The dungeon is a small graph/list of rooms. Each room has **capacity** (minion slots), **trap slots**, and may be **special** (e.g., Vault, Hidden Sanctum, Ambush-Friendly Corridor).

### 3.4 Phylactery (loss state & upgrades)
- The **phylactery** is your life anchor; losing it is defeat.
- It can be upgraded (hidden nooks, anti-divination wards, embedded traps); it typically resides in the **Sanctum**.

---

## 4. Systems overview

### 4.1 Dice & resolution model
- **Single engine:** roll **2d6** + modifiers (bell-curve reliability).
- **Outcome bands:** **10+** strong success; **7–9** mixed; **6−** failure.
- **Modifiers** are small (−3…+3), derived from Tiers, roles, and context, to keep outcomes readable and fast.

### 4.2 Traps (stats & tiers)
- **Tier:** 1–4 (Low/Medium/High/Legendary intensity).
- **Stats:**  
  - **Subtlety** (harder to detect)  
  - **Complexity** (harder to disarm)  
  - **Lethality** (damage scale)  
  - **Reliability** (swing dampener: ± to damage/secondary effects)
- **Lifecycle:** **Build → Arm → Fire/Inert → Repair/Salvage** (repairs cheaper than new; salvage refunds ~50% of base EU).

**Trap Step (per armed trap in the room)**  
1) **Detect**: roll **2d6 + best party Perception + party Tier bonus** vs **TN = 8 + Trap Subtlety**.  
   - **10+**: detected cleanly → may attempt **Disarm**.  
   - **7–9**: detected with risk → **Disarm** at **−1**.  
   - **6−**: missed → **Trap Triggers**.  
2) **Disarm** (if detected): roll **2d6 + best Perception (+mods)** vs **TN = 8 + Trap Complexity**.  
   - **10+**: safely disabled (becomes **Inert**; repairable later).  
   - **7–9**: disabled but **minor blowback** (e.g., −1 to next Skirmish or 1d6 to the lead hero).  
   - **6−**: botch → **Trap Triggers**.  
3) **Trigger**: party takes **damage = Lethality × d6 + Reliability**; apply riders (e.g., **Shaken**: −1 to next Skirmish).

> **Party Tier bonus (guideline):** +0 to +2 depending on composition. Suggested simple rule: `max(0, sum(hero Tiers) − party size)` capped at +2.

### 4.3 Minions (roles & synergies)
- **Tier:** 1–4; baseline **HP** by Tier: T1=6, T2=8, T3=12, T4=18. (A “unit” can be a group token sharing HP.)
- **Roles:** frontline, ambusher, ranged, caster, support.
- **Synergies:**  
  - +1 if ≥2 distinct roles in a room  
  - +1 if **Ambushers** in an **Ambush-Friendly** room  
  - +1 if **Caster** supports **Frontline**  
  - +1 per **Elite** property (rare)
- Upgrades and training can add minor perks (e.g., once-per-raid +2 to a Skirmish roll, or conditional immunities).

### 4.4 Heroes & parties
- **Archetypes** (e.g., Fighter, Rogue, Cleric, Mage) each have **Tier**, **HP**, **Perception**, and **PR bonus** hooks.
- **Party generation** draws a party whose total **Tier ≈ Threat budget** (see §7).  
- **Compositional synergies** add **PR** (Party Rating), e.g.:  
  - +1 if **Healer** present  
  - +1 if **Rogue** present (trap game)  
  - +1 if **Caster + Frontline** mix  
  - +1 if **Defender + Ranged** mix

### 4.5 Skirmish (fast group combat)
- **MR (Minion Rating)** = sum of minion **Tiers** in room + role synergies + room/trap situational modifiers.  
- **PR (Party Rating)** = sum of hero **Tiers** + composition synergies + transient conditions.  
- **Skirmish Roll:** roll **2d6 + (MR − PR) + situational mods**.

**Skirmish Outcome Table**
- **≤4** Catastrophe: defenders routed/destroyed; party takes **0–1d6** damage.  
- **5–6** Break: defenders lose a unit or suffer heavy wounds; party takes **1d6** damage.  
- **7–9** Bloody exchange: defenders lose ~half HP (or one unit); party takes **2d6** damage.  
- **10–11** Solid defense: weakest hero downed **or** party takes **2d6+2**; defenders minor harm.  
- **12+** Crushing defense: party takes **3d6+3** and gains a **Condition** (e.g., **Exhausted**: −1 next room); defenders intact.

> One roll per room keeps solo pacing tight without a GM, while still reflecting your tactical prep fantasy.

---

## 5. Phases in detail

### 5.1 Planning Phase
1) **Income:** Gain **Base EU** from Threat + any **performance bonus** from the prior raid; convert **loot**; apply **salvage** if scrapping assets.  
2) **Upkeep:** Pay upkeep on staffed minions/maintained traps; flag unpaid assets as **inactive**.  
3) **Build & Assign:** Buy/repair/place traps; hire/position minions; set room tactics; choose phylactery room and upgrades.  
4) **(Optional) Project:** Research a trap mod, minion training, or sanctum improvement (completes in N raids).

### 5.2 Fighting Heroes (per raid)
**Party Generation:** Based on **Threat**, assemble a party with **total Tier budget** (see §7) and apply synergy flags.  
**Pathing:** From **Entry** to **Goal** (Vault/Sanctum), heroes select among adjacent rooms using this **temptation heuristic** (higher score is chosen; tie → random):
- **+3** if room is **Vault** or is **closer to the goal**  
- **+1** if **unexplored**  
- **+1** if **recent sound of combat**  
- **−2** if a **trap was just detected**  
- **−2** if party is **Exhausted**  
- **−1** per **downed hero**

**Room Resolution:** For each room encountered, resolve **Trap Step → Skirmish Step → Outcome** (conditions, casualties, loot/toll interactions).

### 5.3 Raid Resolution
1) **Loot & EU accounting:** EU from hero valuables; **performance bonuses** (e.g., defended Vault; wiped party).  
2) **Adjust Threat & Reputation:**  
   - **Threat +1** if victory was decisive (wiped party, spectacle); **−1** if heroes reached the phylactery or plundered the Vault.  
   - **Reputation +1** for humiliations/trickery or themed triumphs; **−1** for paying bribes or conceding major plunder.  
3) **Repairs & Salvage:** Repair damaged traps/minions cheaper than replacement; **salvage** retired assets for partial EU.

---

## 6. Data definitions (design-facing)

> Implementation is up to you; this section defines the **design contract** (fields and intended meaning).

**Room**
- `id`, `name`, `capacity` (minion slots), `trapSlots`, `tags` (Entry, Corridor, Vault, Sanctum, AmbushFriendly).

**Trap**
- `tier(1–4)`, `subtlety(0–4)`, `complexity(0–4)`, `lethality(1–4)`, `reliability(−1…+1)`, `riders` (e.g., Shaken −1 next Skirmish), `euCost`, `upkeep`.

**Minion**
- `tier(1–4)`, `role` (frontline/ambusher/ranged/caster/support), `hp` (by tier baseline), `perks` (small conditional +1s), `euCost`, `upkeep`.

**Hero**
- `archetype`, `tier(1–4)`, `perception(0–3)`, `hp`, `lootValue`, `synergyTags` (healer, rogue, mage, defender, ranged, etc.).

**Budgets (by Threat)**
- `threat`, `baseEU`, `partyTierSum`, `roomsPerRaid`.

---

## 7. Progression & pacing (default targets)

| Threat | Base EU | Party Tier Sum | Rooms per Raid | Expected Win Rate* |
|---:|---:|---:|---:|---:|
| 1 | 150 | 2 | 3 | 65–75% |
| 2 | 180 | 3 | 3 | 60–70% |
| 3 | 210 | 4 | 4 | 55–65% |
| 4 | 240 | 5 | 4 | 50–60% |
| 5 | 270 | 6 | 5 | 45–55% |

\*Before meta upgrades; tune to taste.

---

## 8. Conditions & keywords

- **Shaken**: −1 to next Skirmish roll.  
- **Exhausted**: −1 to room-choice heuristic and Skirmish until rested.  
- **Wounded**: unit starts next room at half HP (round up).  
- **Inert (Trap)**: detected/disabled; requires repair to rearm.  
- **Sanctum**: room housing the phylactery; can hold special defenses/bonuses.

---

## 9. Balance levers (designer notes)

- **Trap DCs:** Raising **Subtlety/Complexity** by +1 shifts detection/disarm odds by ~8–12% each (on 2d6).  
- **MR–PR delta:** Each point shifts the Skirmish curve ~8–9% toward the advantaged side.  
- **Reliability (Traps):** Use ±1 as a feel knob—stabilize lethality or add swingy spice.  
- **Upkeep:** 2–20% of base cost per raid keeps asset counts in check; **repairs** < new; **salvage** ~50% EU refund.

---

## 10. Events & meta (optional tables; solo-friendly)

- **Evil HR Audit**: +EU stipend but impose a temporary constraint (e.g., no new Ambushers this Planning Phase).  
- **Hero Rumors**: Next party gains a synergy tag but becomes **Overconfident** (−1 first Skirmish).  
- **Vendor Sale**: −20% EU on one trap family this Planning Phase.  
- **Named Rivals**: If Reputation ≥ X, a named hero party spawns with a bespoke synergy and bonus loot.

---

## 11. UX & accessibility

- **Readable log**: Every roll prints inputs, target, and result (e.g., “Rogue disarms: 2d6+2 = 9 vs 10 → partial”).  
- **Toggle verbosity**: Compact summary vs. detailed raid log.  
- **Color-agnostic feedback**: Icons and labels for states/conditions.  
- **Speed controls**: Animation on/off; per-room pause or “resolve to end”.

---

## 12. Example turn (worked, for designers)

- **Room:** Twisting Corridor (**Ambush-Friendly**).  
- **Trap:** Poison Darts (T2; Subtlety 2; Complexity 2; Lethality 2; Reliability 0).  
- **Minions:** Skeleton (T1 **Frontline**), Imp (T1 **Ambusher**).  
- **Party:** Rogue (T1, Perception 2), Fighter (T2, Perception 1).  
  - **PR** seed: 1+2 + synergy(+1 for Rogue) = **4** (plus any other tags).  
- **Trap Detect:** 2d6 + best Perception (2) + party Tier bonus (likely 0) vs **TN 10** → result **<10**: **Trigger** → damage = 2d6 (avg ~7).  
- **Skirmish:** **MR** = 1+1 + roles(+1) + ambush room(+1) = **4**; **PR** ≈ **4** → roll **2d6 + 0**.  
  - On **7–9**: **Bloody exchange** (party 2d6; defenders lose ~half HP).

---

## 13. Testing plan (solo balance)

Run **20 simulated raids per Threat band** using T1–T2 assets early; record: **rooms cleared**, **MR–PR deltas**, **trap fire/disarm rates**, **EU delta**, **breach rate**.  
- If **rooms cleared >80%** with low defender losses → add **+1 PR** synergy or **+1** to trap DCs.  
- If **EU delta < +20** on average → reduce upkeep **10–20%** or add **+5–10 EU** loot per T2+ hero.  
- If **breaches >35%** at Threat 2 → add **+1 MR** for mixed-role rooms or increase rooms per raid more slowly.

---

## 14. Content guidance

- **Traps:** physical (spikes, darts, pits), arcane (hex sigils, singularities), environmental (collapsing beams). Upgrades trade **Subtlety** vs **Lethality**.  
- **Minions:** cheap swarms (skeletons/imps), stable bruisers (ogres), rare casters (liches). Roles should invite synergy-building.  
- **Heroes:** classic quartet (fighter/rogue/cleric/mage) with simple perks (e.g., cleric once per raid reduces trap damage; rogue +1 detect/disarm).  
- **Rooms:** Entry (fixed), Corridors (ambush-friendly), Vault (objective magnet), Sanctum (phylactery room).

---

## 15. Victory & fail states

- **Victory (raid):** Party flees or is defeated before breaching the phylactery; you retain valuables and collect loot/bonuses.  
- **Defeat:** Phylactery compromised → game over or heavy penalty (long rebuild).

---

## 16. Tone & writing

Maintain the light, cheeky corporate memo style (Evil HR emails, budget reviews, compliance notices) in tooltips and event popups.

---

## 17. Glossary (select)

- **EU:** Evil Units; the game’s money.  
- **Threat:** Heat/danger that scales hero difficulty and funding.  
- **Reputation:** Notoriety affecting event types and challengers.  
- **Phylactery:** Your life anchor; protect or lose.  
- **MR/PR:** Minion/Party Rating; aggregate strength for Skirmish resolution.  
- **Shaken/Exhausted:** Temporary penalties that carry across rooms.
