import json

# TODO: Automate this script to run on when the data file changes.

def main():
    generator = MarkdownTableGenerator(filename="data.json")
    markdown_table = generator.create_markdown_table()
    # TODO: Import from a file.
    print("# Presentations")
    print("## Evan Kohilas")
    print("")
    print("If you would like me to speak at your event, please get in touch!")
    print()
    print("`evan (at) nohumanerrors.com`")
    print()
    print(markdown_table)


class MarkdownTableGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.table = []
        self.header_names = (
            "Title",
            "Event",
            "Location",
            "Date",
            "Length",
            "Links",
        )

    def create_markdown_table(self):
        presentation_data = self._load_data()
        return self._generate_markdown_table(presentation_data)

    def _load_data(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("presentations", [])

    def _generate_markdown_table(self, presentations):
        self._add_header(self.header_names)

        for presentation in sorted(
            presentations, key=lambda x: x.get("date", ""), reverse=True
        ):
            self._create_presentation_row(presentation)

        return "\n".join(self.table)

    def create_emoji_markdown_link(self, text: str, url: str) -> str:
        if not url:
            return ""
        return f"[{text}]({url})"

    def create_markdown_link(self, text: str, url: str) -> str:
        if not url:
            return text
        return f"[{text}]({url})"

    def _add_header(self, header_values: list[str]):
        self._add_row(header_values)
        self._add_row(["---"] * len(header_values))

    def _add_row(self, values: list[str]):
        self.table.append("| " + " | ".join(values) + " |")

    def _create_presentation_row(self, presentation):
        title = presentation.get("title", "")
        event_name = self.create_markdown_link(
            text=presentation.get("event_name", ""),
            url=presentation.get("event_link", ""),
        )
        location = presentation.get("location", "")
        date = presentation.get("date", "")
        length = presentation.get("length", "")
        links = " ".join(
            [
                self.create_emoji_markdown_link(
                    text="🎞️", url=presentation.get("slide_link", "")
                ),
                self.create_emoji_markdown_link(
                    text="📺", url=presentation.get("video_link", "")
                ),
                self.create_emoji_markdown_link(
                    text="ℹ️", url=presentation.get("session_link", "")
                ),
                self.create_emoji_markdown_link(
                    text="🗃️", url=presentation.get("repository_link", "")
                ),
            ]
        )

        values = [
            title,
            event_name,
            location,
            date,
            length,
            links,
        ]
        self._add_row(values)


if __name__ == "__main__":
    main()
