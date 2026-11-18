"""Helper routines and catalog data for routine planner."""

from models.air_quality import AirQualityData
from models.routine_plan import IndoorHack, RoutineItem
from models.user_profile import ExerciseHabit, UserProfile


def generate_time_routines(
    aqi_data: AirQualityData,
    profile: UserProfile,
    is_hi: bool,
) -> list[RoutineItem]:
    """Create morning, afternoon, and evening routines based on AQI."""
    is_poor = aqi_data.aqi > 150
    high_risk = profile.has_vulnerable_members or profile.has_asthma_or_respiratory

    # Morning Slot
    if is_poor or high_risk or profile.exercise_habit == ExerciseHabit.INDOOR:
        m_act = "घर के अंदर प्राणायाम/हल्का व्यायाम करें" if is_hi else "Shift workout indoors"
        m_why = (
            "सुबह जमीनी हवा में PM2.5 सबसे सघन होता है"
            if is_hi
            else "Morning inversion traps heavy PM2.5 near ground"
        )
    else:
        m_act = (
            "सुबह 7-8 बजे के बाद ही बाहर निकलें"
            if is_hi
            else "Outdoor run safe before traffic peak"
        )
        m_why = "AQI मध्यम स्तर पर है" if is_hi else "AQI is currently moderate"

    # Afternoon Slot
    a_act = (
        "दोपहर 12 से 3 के बीच वेंटिलेशन करें" if is_hi else "Open windows between 12 PM - 3 PM"
    )
    a_why = (
        "धूप और हवा से दोपहर में जमीनी प्रदूषण कम होता है"
        if is_hi
        else "Thermal convection disperses surface particulates"
    )

    # Evening Slot
    e_act = (
        "शाम 6-9 बजे खिड़कियां बंद रखें व मास्क पहनें"
        if is_hi
        else "Seal windows & wear N95 during evening rush"
    )
    e_why = (
        "शाम के ट्रैफिक और ठंडी हवा से धुंध बढ़ती है"
        if is_hi
        else "Evening rush hour causes secondary pollution peak"
    )

    return [
        RoutineItem(
            slot="morning",
            action=m_act,
            why=m_why,
            exposure_impact="-35% PM2.5 peak exposure",
        ),
        RoutineItem(
            slot="afternoon",
            action=a_act,
            why=a_why,
            exposure_impact="-25% indoor stagnation",
        ),
        RoutineItem(
            slot="evening",
            action=e_act,
            why=e_why,
            exposure_impact="-40% rush-hour inhalation",
        ),
    ]


def generate_indoor_hacks(is_hi: bool) -> list[IndoorHack]:
    """Return actionable evidence-based indoor air quality hacks."""
    return [
        IndoorHack(
            category="ventilation",
            title="दुपहर वेंटिलेशन नियम" if is_hi else "Afternoon Cross-Ventilation",
            description="दोपहर 12 से 3 बजे के बीच 20 मिनट के लिए खिड़कियां खोलें।"
            if is_hi
            else "Flush indoor CO2 by opening windows 20 mins between 12-3 PM when surface PM2.5 is lowest.",
            fact_check=None,
        ),
        IndoorHack(
            category="filtration",
            title="DIY कोर्सी-रोसेन्थाल बॉक्स" if is_hi else "DIY Corsi-Rosenthal Box",
            description="बॉक्स फैन और MERV-13 फिल्टर से ₹2500 में 90% PM2.5 फिल्टर करें।"
            if is_hi
            else "A box fan with 4 MERV-13 filters delivers CADR comparable to commercial HEPA at 1/5th cost.",
            fact_check=None,
        ),
        IndoorHack(
            category="cooking",
            title="रसोई वेंटिलेशन और कवर" if is_hi else "Cookware Lids & Range Hood",
            description="खाना बनाते समय ढक्कन लगाएं और एग्जॉस्ट फैन 10 मिनट बाद तक चलाएं।"
            if is_hi
            else "Frying creates ultrafine particles; lids and post-cook exhaust run reduce peaks by 65%.",
            fact_check=None,
        ),
        IndoorHack(
            category="cleaning",
            title="गीला पोछा vs सूखी झाड़ू" if is_hi else "Wet Mopping vs Dry Sweeping",
            description="सूखी झाड़ू से धूल के कण हवा में उड़ते हैं; गीले पोछे का प्रयोग करें।"
            if is_hi
            else "Dry sweeping aerosolizes settled PM10; microfiber wet mopping captures 85% of floor dust.",
            fact_check="पौधों का भ्रम: पौधे VOCs पर मामूली असर करते हैं, पर PM2.5 कम नहीं कर सकते (NASA अध्ययन बंद चैंबर पर था)।"
            if is_hi
            else "Myth Buster: Houseplants remove negligible PM2.5 in real homes; mechanical filters are required.",
        ),
    ]
