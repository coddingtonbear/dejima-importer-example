import argparse
from typing import List, Iterable, Tuple, Optional

from dejima.plugin import NoteField, SourcePlugin, CardTemplate, Note


__version__ = "0.1.0"


class SomeSource(SourcePlugin):
    # These can be named anything you want, and will become fields on
    # your notes in Anki.  Note that the templates in `get_card_templates`
    # below have to match the field names, though!
    Front = NoteField(unique=True, merge=True)
    Back = NoteField(unique=True, merge=True)

    # You could add more fields for storing other information like images
    # audio files or anything else you might find convenient to show
    # on a flash card.
    #
    # See https://github.com/coddingtonbear/dejima/blob/master/src/dejima/sources/lln.py
    # to get an idea of how media works in Anki.

    def get_card_templates(self) -> List[CardTemplate]:
        # Every Dejima "Source" gets its own card type in Anki; this allows
        # each source to define their own fields and have a little more
        # flexibility.  Below, we're defining the templates that will
        # be used by Anki for generating flash cards from your notes.
        #
        # If you want your flash cards to not have a reverse side (i.e.
        # where your question is the *Back* of the card, and you're
        # expected to answer with the *Front*), just remove the second
        # of these options.
        #
        # You can also make certain templates optionally generate a card
        # by carefully crafting the `front` field such that it is empty
        # in certain situations.  See https://github.com/coddingtonbear/dejima/blob/master/src/dejima/sources/boox.py
        # for an example of how to do that.
        return [
            CardTemplate(
                name="Card 1",
                front="<p>{{Front}}</p>",
                back="""
                    {{FrontSide}}
                    <hr id='answer' />
                    <p>
                        {{Back}}
                    </p>
                """,
            ),
            CardTemplate(
                name="Card 2",
                front="""
                    <p>
                        {{Back}}
                    </p>
                """,
                back="""
                    {{FrontSide}}
                    <hr id='answer' />
                    <p>
                        {{Front}}
                    </p>
                """,
            ),
        ]

    @classmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # You *probably* need to read your content from a file somewhere
        # if so, the following block is useful in that it'll open the
        # file you have specified for you and make it available under
        # `self.options.input`.
        #
        # If you do need to open a file -- just un-comment the following
        # statement:

        # parser.add_argument(
        #    "-i",
        #    "--input",
        #    nargs="?",
        #    type=argparse.FileType("r"),
        #    default=sys.stdin,
        #    help="File to read from (default: stdin)",
        # )

        return super().add_arguments(parser)

    def get_entries(self) -> Iterable[Tuple[Optional[str], Note]]:
        # Here is where you do the actual work of importing content
        # from whatever source and `yield`-ing `Note` instances that
        # will become entries in Anki.
        #
        # The below example is pretty useless, but will give you
        # a simple way of understanding how this works.
        flash_cards_i_want_to_create = [
            {"English": "hey there", "Russian": "привет"},
            {"English": "bye", "Russian": "пока"},
        ]

        for card in flash_cards_i_want_to_create:
            # Dejima handles making sure that any particular entry is
            # imported only once, no matter how many times it might
            # appear in an import (so you don't need to worry about
            # being careful not to import particular content more than
            # once), but to do that, you need to give it a "foreign key"
            # to use for identifying this partiuclar entry. Here, we're
            # just using the "English" text on the card.  If you were
            # sure you didn't want Dejima to prevent double-imports,
            # you can set this value to `None` and no double-import
            # checks will take place.
            #
            # If you want to skip those double-import checks for testing
            # or because you've deleted the relevant cards in Anki, you
            # can use the `--reimport` command-line argument.
            foreign_key = card["English"]

            # Now, we create our "Note" object -- the note object has
            # three properties:
            #
            # - fields: This is a dictionary having values for each of
            #   the field names you defined at the top of your class.
            # - tags: This is a list of strings allowing you to add
            #   tags to your card.  We're not adding any tags here,
            #   but it's easy to do that if you wanted to.
            # - media: A list of media objects to upload into Anki
            #   for use as images in flash cards or audio files.  We're
            #   not using those here either, but look at the importer
            #   here: https://github.com/coddingtonbear/dejima/blob/master/src/dejima/sources/lln.py
            #   to get an idea of how that works.
            #
            # You'll see that we're getting the field name via
            # `self.Fields.field_name` -- that's just a convenience
            # property -- you could just use "Front" or "Back", too,
            # if you wanted.  Using it the way shown below just makes
            # it easier in cases where the name of the attribute on
            # this class doesn't match the name of the field you
            # would like to create in Anki.
            note = Note(
                fields={
                    self.Front.field_name: card["English"],
                    self.Back.field_name: card["Russian"],
                }
            )

            yield foreign_key, note
