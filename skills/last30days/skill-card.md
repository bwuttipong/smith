## Description: <br>
Researches recent Reddit, X, and web discussion on a topic, synthesizes the findings, and drafts copy-paste-ready prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zats](https://clawhub.ai/user/zats) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to research recent community and web discussion on a topic, identify current patterns or recommendations, and produce a tailored prompt after the user shares their intended output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics may be sent to OpenAI, xAI, Reddit, or web search services when API keys or web search are used. <br>
Mitigation: Use web-only mode or avoid sensitive topics if external provider calls are not acceptable. <br>
Risk: OpenAI and xAI API keys can be configured in ~/.config/last30days/.env. <br>
Mitigation: Store keys with restricted file permissions, remove keys when they are no longer needed, and rotate them if exposure is suspected. <br>
Risk: The skill can keep local copies of reports and raw research data. <br>
Mitigation: Review and clear the local last30days cache or generated outputs after researching sensitive topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zats/last30days) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with research summaries, source statistics, inline shell commands, and copy-paste-ready prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web-only mode or optional OpenAI and xAI API keys for Reddit and X enrichment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
