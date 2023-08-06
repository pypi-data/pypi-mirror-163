"""Render singing signals from mutwo data via `ISiS <https://forum.ircam.fr/projects/detail/isis/>`_.

ISiS (IRCAM Singing Synthesis) is a `"command line application for singing
synthesis that can be used to generate singing signals by means of synthesizing
them from melody and lyrics."
<https://isis-documentation.readthedocs.io/en/latest/Intro.html#the-isis-command-line>`_.
"""

import configparser
import os
import typing

from mutwo import core_converters
from mutwo import core_constants
from mutwo import core_events
from mutwo import isis_converters
from mutwo import isis_utilities
from mutwo import music_parameters

__all__ = ("EventToIsisScore", "EventToSingingSynthesis")

ConvertableEventUnion = typing.Union[
    core_events.SimpleEvent,
    core_events.SequentialEvent[core_events.SimpleEvent],
]
ExtractedDataDict = dict[
    # duration, consonants, vowel, pitch, volume
    str,
    typing.Any,
]


class EventToIsisScore(core_converters.abc.EventConverter):
    """Class to convert mutwo events to a `ISiS score file. <https://isis-documentation.readthedocs.io/en/latest/score.html>`_

    :param simple_event_to_pitch: Function to extract an instance of
        :class:`mutwo.music_parameters.abc.Pitch` from a simple event.
    :param simple_event_to_volume:
    :param simple_event_to_vowel:
    :param simple_event_to_consonant_tuple:
    :param is_simple_event_rest:
    :param tempo: Tempo in beats per minute (BPM). Defaults to 60.
    :param global_transposition: global transposition in midi numbers. Defaults to 0.
    :param n_events_per_line: How many events the score shall contain per line.
        Defaults to 5.
    """

    _extracted_data_dict_rest = {
        "consonant_tuple": tuple([]),
        "vowel": "_",
        "pitch": music_parameters.WesternPitch(
            "c",
            -1,
            concert_pitch=440,
            concert_pitch_octave=4,
            concert_pitch_pitch_class=9,
        ),
        "volume": music_parameters.DirectVolume(0),
    }

    def __init__(
        self,
        simple_event_to_pitch: typing.Callable[
            [core_events.SimpleEvent], music_parameters.abc.Pitch
        ] = lambda simple_event: simple_event.pitch_list[  # type: ignore
            0
        ],
        simple_event_to_volume: typing.Callable[
            [core_events.SimpleEvent], music_parameters.abc.Volume
        ] = lambda simple_event: simple_event.volume,  # type: ignore
        simple_event_to_vowel: typing.Callable[
            [core_events.SimpleEvent], str
        ] = lambda simple_event: simple_event.vowel,  # type: ignore
        simple_event_to_consonant_tuple: typing.Callable[
            [core_events.SimpleEvent], tuple[str, ...]
        ] = lambda simple_event: simple_event.consonant_tuple,  # type: ignore
        is_simple_event_rest: typing.Callable[
            [core_events.SimpleEvent], bool
        ] = lambda simple_event: not (
            hasattr(simple_event, "pitch_list")
            and simple_event.pitch_list  # type: ignore
        ),
        tempo: core_constants.Real = 60,
        global_transposition: int = 0,
        default_sentence_loudness: typing.Union[core_constants.Real, None] = None,
        n_events_per_line: int = 5,
    ):
        self._tempo = tempo
        self._global_transposition = global_transposition
        self._default_sentence_loudness = default_sentence_loudness
        self._n_events_per_line = n_events_per_line
        self._is_simple_event_rest = is_simple_event_rest

        self._extraction_function_dict = {
            "consonant_tuple": simple_event_to_consonant_tuple,
            "vowel": simple_event_to_vowel,
            "pitch": simple_event_to_pitch,
            "volume": simple_event_to_volume,
        }

    # ###################################################################### #
    #                           private methods                              #
    # ###################################################################### #

    def _add_lyric_section(
        self,
        score_config_file: configparser.ConfigParser,
        extracted_data_dict_per_event_tuple: tuple[ExtractedDataDict, ...],
    ):
        score_config_file[isis_converters.constants.SECTION_LYRIC_NAME] = {
            "xsampa": " ".join(
                map(
                    lambda extracted_data: " ".join(
                        extracted_data["consonant_tuple"] + (extracted_data["vowel"],)
                    ),
                    extracted_data_dict_per_event_tuple,
                )
            )
        }

    def _add_score_section(
        self,
        score_config_file: configparser.ConfigParser,
        extracted_data_dict_per_event_tuple: tuple[ExtractedDataDict, ...],
    ):
        score_section = {
            "globalTransposition": self._global_transposition,
            "tempo": self._tempo,
        }
        for parameter_name, lambda_function in (
            (
                "midiNotes",
                lambda extracted_data: str(extracted_data["pitch"].midi_pitch_number),
            ),
            (
                "rhythm",
                lambda extracted_data: str(extracted_data["duration"]),
            ),
            (
                "loud_accents",
                lambda extracted_data: str(extracted_data["volume"].amplitude),
            ),
        ):
            score_section.update(
                {
                    parameter_name: ", ".join(
                        map(lambda_function, extracted_data_dict_per_event_tuple)
                    )
                }
            )
        score_config_file[isis_converters.constants.SECTION_SCORE_NAME] = score_section

    def _convert_simple_event(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        _: core_constants.DurationType,
    ) -> tuple[ExtractedDataDict]:
        duration = simple_event_to_convert.duration.duration_in_floats
        extracted_data_dict: dict[str, typing.Any] = {"duration": duration}
        for (
            extracted_data_name,
            extraction_function,
        ) in self._extraction_function_dict.items():
            try:
                extracted_information = extraction_function(simple_event_to_convert)
            except AttributeError:
                return (dict(duration=duration, **self._extracted_data_dict_rest),)

            extracted_data_dict.update({extracted_data_name: extracted_information})

        return (extracted_data_dict,)

    def _convert_simultaneous_event(
        self,
        _: core_events.SimultaneousEvent,
        __: core_constants.DurationType,
    ):
        raise isis_utilities.MonophonicSynthesizerError()

    # ###################################################################### #
    #                             public api                                 #
    # ###################################################################### #

    def convert(self, event_to_convert: ConvertableEventUnion, path: str) -> None:
        """Render ISiS score file from the passed event.

        :param event_to_convert: The event that shall be rendered to a ISiS score
            file.
        :type event_to_convert: typing.Union[core_events.SimpleEvent, core_events.SequentialEvent[core_events.SimpleEvent]]
        :param path: where to write the ISiS score file
        :type path: str

        **Example:**

        >>> from mutwo import core_events
        >>> from mutwo import music_events
        >>> from mutwo import music_parameters
        >>> from mutwo import isis_converters
        >>> notes = core_events.SequentialEvent(
        >>>    [
        >>>         music_events.NoteLike(music_parameters.WesternPitch(pitch_name), 0.5, 0.5)
        >>>         for pitch_name in 'c f d g'.split(' ')
        >>>    ]
        >>> )
        >>> for consonants, vowel, note in zip([[], [], ['t'], []], ['a', 'o', 'e', 'a'], notes):
        >>>     note.vowel = vowel
        >>>     note.consonants = consonants
        >>> event_to_isis_score = isis.EventToIsisScore('my_singing_score')
        >>> event_to_isis_score.convert(notes)
        """

        # ISiS can't handle two sequental rests, therefore we have to tie two
        # adjacent rests together.
        if isinstance(event_to_convert, core_events.abc.ComplexEvent):
            event_to_convert = event_to_convert.tie_by(
                lambda event0, event1: self._is_simple_event_rest(event0)
                and self._is_simple_event_rest(event1),
                event_type_to_examine=core_events.SimpleEvent,
                mutate=False,  # type: ignore
            )

        extracted_data_dict_per_event_tuple = self._convert_event(event_to_convert, 0)

        # ":" delimiter is used in ISiS example score files
        # see https://isis-documentation.readthedocs.io/en/latest/score.html#score-example
        score_config_file = configparser.ConfigParser(delimiters=":")

        self._add_lyric_section(score_config_file, extracted_data_dict_per_event_tuple)
        self._add_score_section(score_config_file, extracted_data_dict_per_event_tuple)

        with open(path, "w") as f:
            score_config_file.write(f)


class EventToSingingSynthesis(core_converters.abc.Converter):
    """Generate audio files with `ISiS <https://forum.ircam.fr/projects/detail/isis/>`_.

    :param isis_score_converter: The :class:`EventToIsisScore` that shall be used
        to render the ISiS score file from a mutwo event.
    :param *flag: Flag that shall be added when calling ISiS. Several of the supported
        ISiS flags can be found in :mod:`mutwo.isis_converters.constants`.
    :param remove_score_file: Set to True if :class:`EventToSingingSynthesis` shall remove the
        ISiS score file after rendering. Defaults to False.
    :param isis_executable_path: The path to the ISiS executable (binary file). If not
        specified the value of
        :const:`mutwo.isis_converters.configurations.DEFAULT_ISIS_EXECUTABLE_PATH`
        will be used.

    **Disclaimer:** Before using the :class:`EventToSingingSynthesis`, make sure ISiS has been
    correctly installed on your system.
    """

    def __init__(
        self,
        isis_score_converter: EventToIsisScore,
        *flag: str,
        remove_score_file: bool = False,
        isis_executable_path: typing.Optional[str] = None,
    ):
        if not isis_executable_path:
            isis_executable_path = (
                isis_converters.configurations.DEFAULT_ISIS_EXECUTABLE_PATH
            )

        self.flags = flag
        self.isis_score_converter = isis_score_converter
        self.remove_score_file = remove_score_file
        self._isis_executable_path = isis_executable_path

    def convert(
        self,
        event_to_convert: ConvertableEventUnion,
        path: str,
        score_path: typing.Optional[str] = None,
    ) -> None:
        """Render sound file via ISiS from mutwo event.

        :param event_to_convert: The event that shall be rendered.
        :param path: The path / filename of the resulting sound file
        :param score_path: The path where the score file shall be written to.

        **Disclaimer:** Before using the :class:`EventToSingingSynthesis`, make sure
        `ISiS <https://forum.ircam.fr/projects/detail/isis/>`_ has been
        correctly installed on your system.
        """

        if not score_path:
            score_path = f"{path.split('.')[0]}.isis_score.cfg"

        self.isis_score_converter.convert(event_to_convert, score_path)
        command = "{} -m {} -o {}".format(
            self._isis_executable_path,
            score_path,
            path,
        )
        for flag in self.flags:
            command += " {} ".format(flag)

        os.system(command)

        if self.remove_score_file:
            os.remove(score_path)
