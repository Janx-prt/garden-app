"""
Garden advice CLI

- Prompts for a season and plant type (or accepts them via function call)
- Validates and normalizes inputs
- Looks up tips from data dictionaries
- Recommends plants for the chosen season
"""

from typing import Optional, Tuple

# Canonical season keys: "spring", "summer", "autumn", "winter"
SEASON_ALIASES = {
    "spring": "spring",
    "summer": "summer",
    "autumn": "autumn",
    "fall": "autumn",      # treat "fall" as "autumn"
    "winter": "winter",
}

# Canonical plant keys: "flower", "vegetable"
PLANT_ALIASES = {
    "flower": "flower",
    "flowers": "flower",
    "vegetable": "vegetable",
    "veg": "vegetable",
    "vegetables": "vegetable",
}

# Advice dictionary: advice[season][plant_type] -> list of lines to print
ADVICE = {
    "spring": {
        "flower": [
            "Deadhead early blooms and add a balanced fertiliser.",
            "Divide overcrowded perennials."
        ],
        "vegetable": [
            "Start cool-season crops and harden off seedlings.",
            "Prepare beds with compost."
        ],
    },
    "summer": {
        "flower": [
            "Water in the morning and mulch to retain moisture.",
            "Pinch leggy annuals to encourage new blooms."
        ],
        "vegetable": [
            "Water consistently and watch for pests (aphids, beetles).",
            "Harvest frequently to keep plants productive."
        ],
    },
    "autumn": {
        "flower": [
            "Plant spring-flowering bulbs.",
            "Cut back spent annuals and tidy beds."
        ],
        "vegetable": [
            "Sow/plant cool-season crops; protect from early frosts.",
            "Add leaf mulch to improve soil."
        ],
    },
    "winter": {
        "flower": [
            "Protect tender perennials with covers in frost-prone areas.",
            "Plan next year’s colour scheme."
        ],
        "vegetable": [
            "Clean and oil tools; plan crop rotation.",
            "Start seeds indoors where appropriate."
        ],
    },
}

# Seasonal plant recommendations
RECOMMENDATIONS = {
    "spring": ["Snapdragon", "Lettuce", "Radish"],
    "summer": ["Zinnia", "Tomato", "Basil"],
    "autumn": ["Crocus (bulbs)", "Kale", "Spinach"],
    "winter": ["Hellebore (mild climates)", "Microgreens", "Garlic (in mild regions)"],
}


def normalize(text: str) -> str:
    """Lowercase, trim whitespace, collapse internal spaces."""
    # Remove leading/trailing spaces, lowercase, and collapse multiple spaces
    return " ".join(text.strip().lower().split())


def parse_inputs(
    raw_season: Optional[str] = None,
    raw_plant: Optional[str] = None
) -> Tuple[Optional[str], Optional[str], list]:
    """
    Parse and normalize season and plant type.
    Returns (season_key, plant_key, errors).
    season_key in {"spring","summer","autumn","winter"} or None if invalid.
    plant_key  in {"flower","vegetable"} or None if invalid.
    """
    errors = []  # Collect validation errors
    season_key = None
    plant_key = None

    if raw_season is not None:
        s = normalize(raw_season)  # Normalize user input
        season_key = SEASON_ALIASES.get(s)  # Map to canonical key
        if season_key is None:
            errors.append(
                f"Unknown season: '{raw_season}'. Try spring/summer/autumn(winter) or 'fall'.")
    if raw_plant is not None:
        p = normalize(raw_plant)  # Normalize user input
        plant_key = PLANT_ALIASES.get(p)  # Map to canonical key
        if plant_key is None:
            errors.append(
                f"Unknown plant type: '{raw_plant}'. Try 'flower' or 'vegetable'.")

    return season_key, plant_key, errors  # Return normalized keys and errors


def get_advice(season_key: str, plant_key: str) -> str:
    """
    Build the advice text for a valid (season, plant) pair.
    Falls back gracefully if a combination is missing.
    """
    lines = []

    # Get advice for the season
    season_bucket = ADVICE.get(season_key, {})
    # Get advice for the plant type within the season
    plant_lines = season_bucket.get(plant_key, [])

    if not plant_lines:
        # Default message if no advice found
        lines.append("No specific tips for this combination yet.")
    else:
        lines.extend(plant_lines)

    # Add a recommendation footer
    recs = RECOMMENDATIONS.get(season_key, [])
    if recs:
        lines.append("")  # Blank line before recommendations
        lines.append(
            f"Suggested {plant_key}s for {season_key}: " + ", ".join(recs))

    return "\n".join(lines)  # Combine all lines into a single string


def ask_user(prompt: str) -> str:
    """Wrapper over input() to keep main() tidy and make testing easier."""
    return input(prompt)  # Prompt user for input


def main() -> None:
    """Interactive entrypoint."""
    # Prompt user for season and plant type
    season_input = ask_user(
        "Pick a season (spring, summer, autumn/fall, winter): ")
    plant_input = ask_user("Pick a plant type (flower or vegetable): ")

    # Validate inputs
    season_key, plant_key, errors = parse_inputs(season_input, plant_input)
    if errors:
        # Print validation errors and exit
        print("\n".join(errors))
        return

    # Generate and print advice
    text = get_advice(season_key, plant_key)
    print("\n" + text)


if __name__ == "__main__":
    main()
