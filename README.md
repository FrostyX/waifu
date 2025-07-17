# Waifu

Start your day with a gentle reminder what work needs to be done.

This tool queries all GitHub issues from a specified project that are assigned
to you. Then it uses ChatGPT to summarize them, and ElevenLabs' text-to-speech
functionality to read them out loud.

To make this more fun, it features various characters with different
personalities and voices.


## Usage

```
poetry run python3 main.py \
    --character random \
    --user FrostyX \
    --project fedora-copr/copr
```

## Characters

- `professional` - Safe for work
- `sergeant` - Military drill sergant
- `cowboy` - Watched Yellowstone once ...
- `waifu` - I know you want this option, you absolute degenerate
- `random` - Randomly choose one of the previous characters


## Configuration

Create `.env` file in this directory.

```
OPENAI_API_KEY=...
ELEVENLABS_API_KEY=...
```

# Goals

At this moment, the reliance on ChatGPT and ElevenLabs is hardcoded, but the
goal is to allow any LLM for summarization and any text-to-speech
provider. Ideally local ones, so this can be used for private issues.

At this moment, GitHub is the only supported issue tracker, but the goal is to
support JIRA as well.
