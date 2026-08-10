"""Project Redoubt sample release component."""


def health() -> dict[str, str]:
    return {
        "service": "restech-release-component",
        "status": "healthy",
    }


if __name__ == "__main__":
    print(health())
