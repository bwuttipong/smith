# User Preference: Essentials Morning Brief Format

Updated: 2026-05-24
Session: Morning briefing refinement

User (Jeff/Best Wuttipong) prefers the morning briefing to be concise and essential-only by default.

**Preferred Format:**
- Weather (current conditions for Bangkok)
- Top 3 Todoist tasks only

**Rationale:**
- Reduces cognitive load
- Focuses on actionable items
- Avoids information overload
- Full detailed briefing available on request via --full flag

**Implementation Notes:**
- The morning-briefing.sh script should default to essentials format
- Add --full flag to output the previously detailed format (weather, calendar, email, tasks, notes, stocks)
- Essentials format should be faster to generate and easier to scan