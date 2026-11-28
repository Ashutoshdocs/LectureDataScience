from dask import delayed


@delayed
def square(number: int) -> int:
    return number * number


@delayed
def cube(number: int) -> int:
    return number * number * number


@delayed
def summarize(values):
    return {
        "count": len(values),
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
        "total": sum(values),
        "average": sum(values) / len(values) if values else None,
    }
