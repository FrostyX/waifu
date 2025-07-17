"""
What shall we do today?
"""

import os
import sys
import json
import random
import argparse
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import elevenlabs
from elevenlabs.client import ElevenLabs


PROMPT = """
Here is a JSON representing a GitHub issue and its issues.
Can you summarize it in one consize paragraph? At maximum 300 characters long.
When you encounter the name 'FrostyX' in the discussion, that's me.

{personality}

{issue}
"""


class Professional:
    def __init__(self):
        # Liam - TX3LPaxmHKxFdv7VOQHJ
        self.elevenlabs_voice_id = "TX3LPaxmHKxFdv7VOQHJ"
        self.personality = ""
        self.speed = 1.0


class Cowboy:
    def __init__(self):
        # Brian - nPczCjzI2devNBz1zQrb
        # Bill - pqHfZKP75CvOlQylNhV4
        self.elevenlabs_voice_id = "nPczCjzI2devNBz1zQrb"
        self.personality = "Say this in a words that cowboy would use."
        self.speed = 1.0


class Sergeant:
    def __init__(self):
        # Drill Sergeant - DGzg6RaUqxGRTHSBjfgF
        self.elevenlabs_voice_id = "DGzg6RaUqxGRTHSBjfgF"
        self.personality = (
            "Say this like you are a military drill sergeant."
        )
        self.speed = 1.1


class Waifu:
    def __init__(self):
        # Elli - MF3mGyEYCl7XYWbV9V6O
        # Hope - uYXf8XasLslADfZ2MB4u
        # Villain - WtA85syCrJwasGeHGH2p
        # Aurelia - thfYL0Elyru2qqTtNQsE
        # Serfaina - 4tRn1lSkEn13EVTuqb0g
        # Ivanna - 4NejU5DwQjevnR6mh3mb
        # Gigi - jBpfuIE2acCO8z3wKNLl
        # Nicole - piTKgcLEGmPE4e6mEKli
        self.elevenlabs_voice_id = "MF3mGyEYCl7XYWbV9V6O"
        self.personality = (
            "Say this while flirting with me in an anime waifu tone. "
            "Say this like love me."
        )
        self.speed = 1.0


def gh_issues(project: str, assignee: str) -> dict:
    cmd = [
        "gh", "search", "issues",
        "-R", project,
        "--assignee", assignee,
        "--state", "open",
        "--json", "number,title",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    return json.loads(proc.stdout.decode("utf-8"))


def gh_issue_json(project: str, number: int) -> dict:
    cmd = [
        "gh", "issue",
        "-R", project,
        "view", str(number),
        "--json", "title,body,state,author,comments",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    return json.loads(proc.stdout.decode("utf-8"))


def ask_chatgpt(question: str) -> str:
    """
    OpenAI model pricing:
    https://platform.openai.com/docs/pricing
    """
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=question,
    )
    return response.output_text


def read_out_loud(text: str, voice: str, speed: float = 1.0) -> None:
    """
    ElevenLabs API
    https://elevenlabs.io/docs/api-reference/text-to-speech/convert
    """
    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=(voice or "JBFqnCBsd6RMkjVDRZzb"),
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings={
            "speed": speed,
        }
    )
    elevenlabs.play(audio)


def cmdline_args():
    parser = argparse.ArgumentParser(
        prog="Waifu",
        description="What shall we do today?",
    )
    parser.add_argument("-c", "--character", default="professional")
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-p", "--project", required=True)
    return parser.parse_args()


def main() -> None:
    load_dotenv()

    args = cmdline_args()
    match args.character:
        case "random":
            character = random.choice([
                Professional(),
                Cowboy(),
                Sergeant(),
                Waifu(),
            ])
        case "professional":
            character = Professional()
        case "cowboy":
            character = Cowboy()
        case "sergeant":
            character = Sergeant()
        case "waifu":
            character = Waifu()
        case _:
            print("Unsupported character, see project readme")
            sys.exit(1)

    report = ""
    issues = gh_issues(args.project, args.user)
    for issue in issues:
        question = PROMPT.format(issue=issue, personality=character.personality)
        answer = ask_chatgpt(question)
        report += "Issue number {0} - {1}.\n".format(
            issue["number"], issue["title"])
        report += answer
        report += "\n\n"
        report += "<break time='3.0s' />"  # If this doesn't work, try ...
        report += "\n\n"

    print(report)
    try:
        read_out_loud(
            report,
            voice=character.elevenlabs_voice_id,
            speed=character.speed,
        )
    except elevenlabs.core.api_error.ApiError as ex:
        print("Failed to play through ElevenLabs:")
        print(json.dumps(ex.body, indent=4))
        sys.exit(1)
        breakpoint()

        pass


if __name__ == "__main__":
    main()
