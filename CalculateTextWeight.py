from PIL import ImageFont, ImageDraw, Image


def generate_and_print_calculate_text_weight(font_path_intake, font_size_intake):
    # Define the font and size
    font = ImageFont.truetype(font_path_intake, font_size_intake)

    # Measure character widths
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\,.<>/? "
    widths = {}
    for char in characters:
        image = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), char, font=font)
        width = bbox[2] - bbox[0]
        if width > 0:
            if width not in widths:
                widths[width] = ""
            widths[width] += char

    # Sort characters by width
    sorted_widths = sorted(widths.items(), key=lambda item: item[0])

    # Prepare weight groups
    weight_groups = []
    for width, chars in sorted_widths:
        weight_groups.append({"Characters": chars, "Weight": width})

    # Create the CalculateTextWeight function as a string
    function_str = """
CalculateTextWeight(TextInput: Text): Number =
    With(
        {
            splitText: Split(TextInput, ""),
            weightGroups: Table(
"""

    # Add weight groups to the function string
    for idx, group in enumerate(weight_groups):
        if idx == len(weight_groups) - 1:
            function_str += f"                {{Characters: \"{group['Characters']}\", Weight: {group['Weight']}}}\n"
        else:
            function_str += f"                {{Characters: \"{group['Characters']}\", Weight: {group['Weight']}}},\n"

    function_str += """
            )
        },
        Sum(
            AddColumns(
                splitText,
                Weight,
                LookUp(
                    weightGroups,
                    Find(Value, Characters) > 0,
                    Weight
                )
            ),
            Weight
        )
    );
"""

    # Print the entire function string
    print(function_str)


if __name__ == "__main__":
    font_path = "Montserrat-SemiBold.ttf"
    font_size = 16
    generate_and_print_calculate_text_weight(font_path, font_size)
