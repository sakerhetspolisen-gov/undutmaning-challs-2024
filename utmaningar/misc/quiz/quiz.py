#!/usr/bin/env python
"""
Example of running a prompt_toolkit application in an asyncssh server.
"""
import asyncio
import logging

import asyncssh
from prompt_toolkit.contrib.ssh import PromptToolkitSSHServer, PromptToolkitSSHSession
from prompt_toolkit.shortcuts import ProgressBar, print_formatted_text
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.validation import Validator
import signal

signal.signal(signal.SIGINT, signal.SIG_IGN)


from typing import Any, Callable, Sequence, TypeVar

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import clear

# from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import Completer
from prompt_toolkit.eventloop import run_in_executor_with_context
from prompt_toolkit.filters import FilterOrBool
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import AnyContainer, HSplit
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.validation import Validator
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Label,
    TextArea,
    ValidationToolbar,
)


def create_app(dialog: AnyContainer, style: BaseStyle | None) -> Application[Any]:
    # Key bindings.
    bindings = KeyBindings()
    bindings.add("tab")(focus_next)
    bindings.add("s-tab")(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
        refresh_interval=0.5,
    )


def input_dialog(
    questions: list = [],
    cancel_text: str = "Avbryt",
    completer: Completer | None = None,
    password: FilterOrBool = False,
    style: BaseStyle | None = None,
) -> Application[str]:
    """
    Display a text input box.
    Return the given text, or None when cancelled.
    """

    def accept(buf: Buffer) -> bool:
        questions.pop(0)
        logging.debug(f"Len questions {len(questions)}")
        if len(questions) == 0:
            logging.debug("Exiting prompt")
            get_app().exit(result="Done")
        textfield.validator = get_validator()
        textfield.text = ""
        dialog.body = HSplit(
            [
                Label(text=get_question(), dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        )

        return True

    def return_none() -> None:
        "Button handler that returns None."
        get_app().exit()

    def get_question():
        return questions[0][0] if questions else ""

    def get_validator():
        return questions[0][1] if questions else ""

    cancel_button = Button(text=cancel_text, handler=return_none)

    textfield = TextArea(
        text="",
        multiline=False,
        password=password,
        completer=completer,
        validator=get_validator(),
        accept_handler=accept,
    )

    dialog = Dialog(
        title=HTML("<textcolor>Fråga</textcolor>"),
        body=HSplit(
            [
                Label(text=get_question(), dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        ),
        buttons=[cancel_button],
        with_background=True,
    )

    return create_app(dialog, style)


# Custom color scheme.
example_style = Style.from_dict(
    {
        "dialog": "bg:#212529",
        "textcolor": "#b5e853",
        "text-area": "#000000",
        "text-area.prompt": "#000000",
        "button": "bg:#212529",
        "dialog frame-label": "bg:#ffffff #000000",
        "dialog.body": "bg:#000000 #b5e853",
    }
)


def validate_fork(string: str):
    guess = string.strip().lower().rstrip("_sys")
    return "fork" == guess or "vfork" == guess or "clone" == guess or "clone3" == guess


validator_fork = Validator.from_callable(
    lambda answer: validate_fork(answer),
    error_message="Fel svar",
    move_cursor_to_end=True,
)


def validate_vim(string: str):
    guess = string
    return (
        ":q" == guess
        or ":q!" == guess
        or ":wq" == guess
        or "ZZ" == guess
        or "ZQ" == guess
        or ":qa" == guess
        or ":x" == guess
    )


validator_vim = Validator.from_callable(
    lambda answer: validate_vim(answer),
    error_message="Fel svar",
    move_cursor_to_end=True,
)


def easy_validator(*solutions):
    all(type(solution) == str for solution in solutions)
    return Validator.from_callable(
        lambda answer: any(
            solution == answer.strip().lower() for solution in solutions
        ),
        error_message="Fel svar",
        move_cursor_to_end=True,
    )


questions = []
questions.append(
    ("Vilket år hölls Undutmaning för första gången?\n", easy_validator("2022"))
)
questions.append(("Vilket år upptäcktes viruset Stuxnet?\n", easy_validator("2010")))
questions.append(
    (
        "Vad står förkortning RAT för (inom området skadlig mjukvara)?\n",
        easy_validator("remote access trojan"),
    )
)
questions.append(
    (
        "Vilket port används som standard för server-delen av Secure Shell (SSH)?\n",
        easy_validator("22"),
    )
)
questions.append(
    (
        "Vilket år blev SÄPO en egen myndighet?\n",
        easy_validator("2015"),
    )
)
questions.append(
    (
        "Enligt OSI-modellen, vilket lager (ange i nummer) ligger TCP på?\n",
        easy_validator("4"),
    )
)
questions.append(
    (
        "På Linux, vilket heltal/integer används för STDOUTs file-descriptor?\n",
        easy_validator("1"),
    )
)
questions.append(
    (
        "Du har råkat öppna vim, vad ska du skriva för att komma ur det?\n",
        easy_validator(":q", ":q!", ":wq", "ZZ", "ZQ", ":qa", ":x"),
    )
)

questions.append(
    (
        "What står förkortningen LPE för (inom området cybersäkerhet)?\n",
        easy_validator("local privilege escalation"),
    )
)

questions.append(
    (
        "På linux, vad är ett av syscall:en som används som kan användas för att skapa en ny process?\n",
        validator_fork,
    )
)
questions.append(
    (
        "Vilken funktion kallas på i Linux-kärnan (v6 och framåt) av syscalls* som används för att skapa en ny process?\n  * T.ex. vfork, fork, clone, clone3\nHint: Googla linux/kernel/fork.c\n\n",
        easy_validator("kernel_clone", "kernel clone"),
    )
)


async def quiz(ssh_session: PromptToolkitSSHSession) -> None:
    """
    The application interaction.

    This will run automatically in a prompt_toolkit AppSession, which means
    that any prompt_toolkit application (dialogs, prompts, etc...) will use the
    SSH channel for input and output.
    """
    try:
        q = 0

        def get_rprompt_text():
            return [
                ("", " "),
                ("underline", f"<Fråga {q}>"),
                ("", " "),
            ]

        prompt_session = PromptSession(rprompt=get_rprompt_text)

        # Alias 'print_formatted_text', so that 'print' calls go to the SSH client.
        print = print_formatted_text
        print("Välkommen till Undutmaning 2024")
        # Simple progress bar.
        # with ProgressBar() as pb:
        #     for i in pb(range(15)):
        #         await asyncio.sleep(0.1)

        res = await input_dialog(
            questions=questions.copy(), style=example_style
        ).run_async()
        clear()
        if res:
            ssh_session.stdout.write("Flaggan är undut{Kul_att_du_ville_tävla!}\n")

    except BaseException as E:
        logging.error(E, exc_info=True)


async def main(port=22):
    # Set up logging.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    await asyncssh.create_server(
        lambda: PromptToolkitSSHServer(quiz),
        "",
        port,
        server_host_keys=["/etc/ssh/ssh_host_ecdsa_key"],
    )

    # Run forever.
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
