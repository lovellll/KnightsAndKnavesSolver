#!/usr/bin/env python
"""Module for converting raw knights and knaves puzzles into a standard format."""

from __future__ import print_function

from symbolizer import symbolize

templates = set([])


def parse(puzzle):
    """Parse puzzles of form {name: claim} into symbolized form."""
    def templatize(names, claim):
        """Transform a claim into a regex-capable template."""
        for name in names:
            while name in claim:
                claim = claim.replace(name, "name")

        while "knave" in claim:
            claim = claim.replace("knave", "k_id")

        while "knight" in claim:
            claim = claim.replace("knight", "k_id")

        while " am " in claim:
            claim = claim.replace(" am ", " is ")

        return claim.lower()

    # Replace instances of "I" with name of speaker
    puzzle = {name: claim.replace(" I ", " " + name + " ").replace("I ", name + " ").replace(" I", " " + name)
              for name, claim in puzzle.iteritems()}

    names = puzzle.keys()
    for claim in puzzle.values():

        # transform given claim into a template
        template = templatize(names, claim)

        symbolic_claim = symbolize(claim, template)

        print (symbolic_claim)
        """
        if (validate(claim, template)):
            print (validate(claim, template))

        if not validate(claim, template):
            if "Only" not in claim and "only" not in claim:
                pass  # print (claim)

        global templates
        templates.add(claim)
        """


def clean(puzzle):
    """Format a given puzzle into the form {name: claim}."""
    def clean_claim(claim):
        """Strip uninformative leading words from a given claim."""
        rm_claims_comma = lambda x: x.split("claims, ")[1] if "claims, " in x else x
        rm_claims_that = lambda x: x.split("claims that ")[1] if "claims that " in x else x
        rm_says_comma = lambda x: x.split("says, ")[1] if "says, " in x else x
        rm_says_that = lambda x: x.split("says that ")[1] if "says that " in x else x
        rm_tells_you_comma = lambda x: x.split("tells you, ")[1] if "tells you, " in x else x
        rm_tells_you_that = lambda x: x.split("tells you that ")[1] if "tells you that " in x else x
        rm_trail_apo = lambda x: x[:-1] if x[-1] == "\'" else x
        rm_lead_backtick = lambda x: x[1:] if x[0] == "`" else x

        func_list = [rm_claims_comma, rm_claims_that, rm_says_comma,
                     rm_says_that, rm_tells_you_comma, rm_tells_you_that,
                     rm_trail_apo, rm_lead_backtick]

        parsed_claim = reduce(lambda c, func: func(c), func_list, claim)

        return parsed_claim

    rm_lead_apo = lambda x: x[1:] if x[0] == '\'' else x
    rm_ws = lambda x: x.strip()

    lines = puzzle.split(".")
    lines, name_line = lines[1:], lines[0]

    sub_comma_for_and = lambda x: x.replace("and", ",")
    make_names = lambda x: map(rm_ws, x.split(":")[1].split(","))

    names = make_names(sub_comma_for_and(name_line))
    claims = {}

    for line in lines:
        if len(line) > 1:
            formatted_line = rm_ws(rm_lead_apo(line))
            name = formatted_line[:formatted_line.find(" ")]
            claim = formatted_line[formatted_line.find(" ") + 1:]

            if name not in names:
                raise ValueError("Badly formatted puzzle")
            else:
                claims[name] = clean_claim(claim)

    return claims


def process(puzzle):
    """Process an individual knights and knaves problem."""
    puzzle = clean(puzzle)
    parse(puzzle)
    # print("=" * 50)


def main():
    """Entry point."""
    puzzles = []

    with open("raw.txt", "r") as f:
        for line in f:
            puzzles = line[:-2].split("###")

    for puzzle in puzzles:
        process(puzzle)
        # break

    global templates
    templates = sorted(list(templates))
    for template in templates:
        pass  # print (template)

if __name__ == "__main__":
    main()
