"""The single external tool used by the Day 1 assessment."""
from config import COURSE_FEES


def get_course_fee(course_code: str) -> str:
    """Return the college's current fee for one course code."""
    normalized_code = course_code.strip().upper()
    fee = COURSE_FEES.get(normalized_code)
    if fee is None:
        return f"Unknown course code: {normalized_code}"
    return f"{normalized_code}: Rs. {fee:,}"


TOOL = {
    "type": "function",
    "function": {
        "name": "get_course_fee",
        "description": "Look up the current tuition fee in rupees for a college course code.",
        "parameters": {
            "type": "object",
            "properties": {
                "course_code": {
                    "type": "string",
                    "description": "Course code, for example AI202",
                }
            },
            "required": ["course_code"],
        },
    },
}


if __name__ == "__main__":
    print(get_course_fee("AI202"))