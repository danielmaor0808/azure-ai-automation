from fastapi import APIRouter, HTTPException
from medical_chatbot.backend.models.schemas import ChatRequest, ChatResponse
from medical_chatbot.backend.services.openai_client import ask_openai
from medical_chatbot.backend.utils.validation import validate_user_info, is_user_info_complete
import re

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        confirmation_patterns = [
            # English affirmations
            r"\b(yes|yeah|yep|yup|y|ok(ay)?|sure|correct|right|confirmed|confirm|continue|go ahead|proceed|that('s| is) (right|correct)|looks good|all good|fine by me)\b",

            # Hebrew affirmations
            r"\b(כן|מאשר(?:ת)?|נכון|אישור|המשך|אפשר להמשיך|אפשר להתחיל|בסדר|ממשיכ(?:ה)?|הכל (בסדר|נכון|תקין)|כל (ה)?פרטים (נכונים|תקינים)|מאוש(?:ר|רת))\b"
        ]

        user_input = payload.message.strip().lower()

        # check for matches
        is_confirmation = (
                is_user_info_complete(payload.user_info) and
                any(re.search(pattern, user_input, re.IGNORECASE) for pattern in confirmation_patterns)
        )

        if payload.phase == "info_collection" and is_confirmation:
            payload.phase = "qa"

        if is_user_info_complete(payload.user_info):
            errors = validate_user_info(payload.user_info)
            if errors:
                raise HTTPException(status_code=400, detail=errors)

        # call openai bot
        answer = await ask_openai(payload)

        return ChatResponse(
            answer=answer,
            user_info=payload.user_info,
            phase=payload.phase
        )


    except Exception as e:
        print("❌ Exception occurred:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
