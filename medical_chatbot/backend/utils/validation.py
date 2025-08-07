from medical_chatbot.backend.models.schemas import UserInfo
from typing import List

def is_user_info_complete(user: UserInfo) -> bool:
    return all([
        user.first_name,
        user.last_name,
        user.id_number and len(user.id_number) == 9,
        user.gender in {"male", "female", "זכר", "נקבה"},
        user.age and isinstance(user.age, int) and 0 <= user.age <= 120,
        user.hmo in {"מכבי", "מאוחדת", "כללית"},
        user.card_number and user.card_number.isdigit() and len(user.card_number) == 9,
        user.membership_tier in {"זהב", "כסף", "ארד"}
    ])




def validate_user_info(user: UserInfo) -> List[str]:
    errors = []

    if user.first_name and not user.first_name.isalpha():
        errors.append("First name must contain only letters.")
    if user.last_name and not user.last_name.isalpha():
        errors.append("Last name must contain only letters.")
    if user.id_number and (not user.id_number.isdigit() or len(user.id_number) != 9):
        errors.append("ID number must be a 9-digit number.")
    if user.card_number and (not user.card_number.isdigit() or len(user.card_number) != 9):
        errors.append("Card number must be a 9-digit number.")

    return errors


