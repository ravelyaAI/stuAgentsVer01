# Ravelya Synthetic Student Agents

Version 0.1.0 · October 22, 2026 · Prepared for Dennis Mohle and Aimee Jacobs.

Five configurable Python student agents for **When Trust Becomes Attachment:
Social Connection and Error Reporting in AI-Assisted Programming**. Includes
the optional moderate baseline specified in the shared project charter.

**These are exploratory LLM role simulations, not validated human student
emulators. No human findings or live model results are bundled.** The five
domains are dimensions of a personality model, not five exhaustive human types.

## Start in two minutes

Clone this repository or download and unzip it. Open the folder in PyCharm and run `launch.py`, or open Terminal there:

```bash
python3 launch.py
```

Choose **1** to preview all six configurations under both conditions, without an
API key or internet. It opens a local HTML report containing the exact prompts.
Python 3.10 or later is required. No pip installation is needed.

Choose **2** for a live smoke test (four API requests) or **3** for the full
charter rehearsal (24 requests). Enter an OpenAI API key locally when prompted,
and specify a model ID your API project can use that supports Responses API
structured outputs. The hidden key prompt holds the key only in the process.
If your IDE cannot hide input, use Terminal or a local `.env` file instead.
API billing is separate from a ChatGPT subscription. No paid API calls were
made while building this package.

For persistent local settings, copy `.env.example` to `.env` and fill it in.
Do not share or commit `.env`. There is deliberately no silently selected model.

## The profiles

| Key | Elevated domain | Other four domains |
|---|---|---|
| `extraversion` | Extraversion | Moderate |
| `agreeableness` | Agreeableness | Moderate |
| `conscientiousness` | Conscientiousness | Moderate |
| `negative_emotionality` | Negative Emotionality | Moderate |
| `open_mindedness` | Open-Mindedness | Moderate |
| `baseline` (optional) | None | All moderate |

Each profile includes the three facets belonging to each domain (15 total).
High/moderate settings are researcher-authored experimental configurations,
not BFI-2 test scores, percentiles, diagnoses, or empirically calibrated agents.
All configurations have the same intermediate Python proficiency and no
assigned demographic identity. The scripts do not prescribe whether any
profile notices or reports an error, or becomes attached to the assistant.

## Run from Terminal

```bash
# Five agents, two conditions, no model responses
python3 agents.py --preview

# Include the charter's moderate baseline
python3 agents.py --preview --baseline

# Once .env contains your key and model, run one matched pair
python3 agents.py --profile conscientiousness

# Full charter rehearsal: six configurations x two conditions x three repeats
# 36 trials / up to 72 API calls. Repeats are NOT independent human participants.
python3 agents.py --baseline --repeats 3 --seed 42

# Inspect all personality configurations
python3 agents.py --list

# Software verification (no API calls)
python3 -m unittest discover -s tests -v
```

The order seed controls only randomized trial order. It does not make the
model deterministic. Use a fixed model snapshot where available. Temperature
is omitted by default for compatibility; specify `--temperature` only when
supported and hold it fixed across conditions. The selected model, returned
model, settings, timestamps, response IDs, usage, prompt and configuration
hashes, and full messages are logged. No automatic model fallback or retry
occurs. A failed trial stops the run and preserves completed stages.

## Experimental sequence

1. Create fresh history for each profile/condition/repeat.
2. Present an assignment and the same assistant-written Python solution.
   Only the social introduction differs across conditions.
3. Collect a private correctness assessment, noticed issue, proposed check,
   confidence, and brief explanation. No execution tool is provided; a proposed
   check is not observed verification behavior.
4. Preserve that response, then ask whether to submit a private error report
   to the researcher. Also collect a prototype 1–7 perceived-connection item.
5. Export exact transcripts, a CSV, and a local HTML review report.

The reporting stage sees its own recognition response. Other trials never do.
The task answer key and coding rubric remain outside the model prompts.
The task is a proposed simple boundary-error example; it was not already frozen
in the source charter. The technical solution and assignment are identical
across social and neutral conditions.

## Files produced

Every run creates a new directory under `runs/`; existing trials are not overwritten.

- `manifest.json`: model/settings, randomized schedule, planned call count, hashes.
- `task_snapshot.json` and `profiles_snapshot.json`: exact configuration used.
- `trial_###.json`: prompts, available responses, provider metadata, status.
- `results.csv`: measures plus blank human-coding fields.
- `report.html`: expandable transcripts for the morning meeting.

Preview rows are explicitly marked `preview` and contain no invented responses.
Tests use fixtures marked TEST_ONLY in temporary directories; those outputs
are not research data and are not bundled as results.

## Interpretation and review with Aimee

- The recognition assessment is a model self-report. A human coder must inspect
  the issue description against the rubric and complete
  `recognition_verified_by_human` (yes/no/uncertain). Do not equate saying
  "incorrect" with identifying the intended error.
- Calculate reporting among verified recognizers only after coding. Show the
  denominator, uncertain decisions, failures, and missing responses separately.
- The proposed social script is brief warmth, not a sustained personalized
  relationship. Revise or expand it before making strong ELIZA-effect claims.
- A private recognition question may prime later reporting. Decide whether
  this is acceptable for your intended design before freezing the protocol.
- The easy boundary bug may cause ceiling effects. Evaluate task difficulty
  without selecting only examples that produce the desired result.
- A model's numeric connection response is generated text; it does not show
  actual attachment. The single item is not a validated social-connection scale.
- High trait prompts can create stereotypes or demand effects. Test fidelity
  independently using unrelated situations and blinded ratings. Do not use
  the study's reporting outcome to define whether a profile is faithful.
- Five high-trait configurations and a baseline cannot identify all interactions
  or represent a student population. Add low levels and mixed profiles later
  only with a recorded design revision.
- The original charter leaves either direction of the reporting effect plausible.
  This code does too. Do not treat repeated model calls as a human sample or
  use their counts as evidence of a causal effect in students.
- Keep synthetic runs and the eventual classroom pilot in separate datasets.
  The charter calls for an institutional ethics determination before recruitment.

**Meeting decisions:** confirm the task, social manipulation, report recipient,
recognition coding, connection measure, model/settings, repetitions, and what
counts as a successful protocol rehearsal. This package is ready for that review,
not a substitute for it.

## Sources and provenance

The implementation draws on the following papers and project charter.

1. Soto, C. J., & John, O. P. (2017). The next Big Five Inventory (BFI-2):
   Developing and assessing a hierarchical model with 15 facets to enhance
   bandwidth, fidelity, and predictive power. *Journal of Personality and Social
   Psychology, 113*(1), 117–143. https://doi.org/10.1037/pspp0000096
   Author PDF (corrected version):
   https://www.colby.edu/wp-content/uploads/2013/08/Soto_John_2017.pdf
2. Soto, C. J., & John, O. P. (2017). Short and extra-short forms of the Big Five
   Inventory–2: The BFI-2-S and BFI-2-XS. *Journal of Research in Personality, 68*,
   69–81. https://doi.org/10.1016/j.jrp.2017.02.004
   https://www.colby.edu/wp-content/uploads/2013/08/Soto_John_2017b.pdf
3. Shared charter: *When Trust Becomes Attachment: Social Connection and Error
   Reporting in AI-Assisted Programming*; version label October 16, 2026,
   Drive modification October 21, 2026; read October 22, 2026.
4. OpenAI Responses structured-output API:
   https://developers.openai.com/api/docs/guides/structured-outputs

The papers supply the personality framework and measurement context. They do
not supply these agent prompts or demonstrate that LLM personas emulate human
students. This package does not reproduce the BFI-2 questionnaire or implement
its scoring. Prompts, task, and simulation design are prototype engineering
choices for this project.

Prepared by Astra / Codex for review.
